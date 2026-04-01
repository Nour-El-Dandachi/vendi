from PIL import Image
from transformers import AutoProcessor, ShieldGemma2ForImageClassification
import torch

model_id = "google/shieldgemma-2-4b-it"

processor = AutoProcessor.from_pretrained(model_id)
model = ShieldGemma2ForImageClassification.from_pretrained(
    model_id,
    device_map="cpu",           # ← force CPU, MPS is broken for this model
    torch_dtype=torch.float32
).eval()

TEXT_REJECT_KEYWORDS = {
    "weapon", "gun", "knife", "bomb", "explosive", "drugs", "cocaine",
    "weed", "cannabis", "vape", "nicotine", "alcohol", "porn", "nude",
    "sex toy", "counterfeit", "fake", "hate", "nazi"
}

TEXT_FLAG_KEYWORDS = {
    "replica", "copy", "inspired", "adult", "18+", "smoking", "tobacco",
    "supplement", "military", "ammo"
}

# The model always outputs exactly 3 policies in this fixed order:
#   index 0 → sexual
#   index 1 → dangerous
#   index 2 → violence
# For each policy: probabilities[policy_idx][0] = No (safe), [1] = Yes (violation)
POLICY_ORDER = ["sexual", "dangerous", "violence"]

VIOLATION_THRESHOLDS = {
    "sexual":    0.35,
    "dangerous": 0.40,
    "violence":  0.40,
}


def check_text_policy(name: str, description: str, category: str) -> dict:
    content = f"{name} {description} {category}".lower()

    reject_matches = [word for word in TEXT_REJECT_KEYWORDS if word in content]
    if reject_matches:
        return {
            "result": "rejected",
            "reason": f"Text contains prohibited terms: {', '.join(reject_matches)}"
        }

    flag_matches = [word for word in TEXT_FLAG_KEYWORDS if word in content]
    if flag_matches:
        return {
            "result": "flagged",
            "reason": f"Text contains suspicious terms: {', '.join(flag_matches)}"
        }

    return {
        "result": "approved",
        "reason": "Text passed moderation"
    }


def check_image_policy(image_path: str | None) -> dict:
    if not image_path:
        return {
            "result": "pending",
            "reason": "No image provided"
        }

    try:
        image = Image.open(image_path).convert("RGB")
        print("MODEL DTYPE:", next(model.parameters()).dtype)
        print("DEVICE:", next(model.parameters()).device)

        # ✅ Do NOT pass policies= — the model has them baked in
        inputs = processor(images=[image], return_tensors="pt")  # no .to(model.device)

        with torch.inference_mode():
            output = model(**inputs)

        # output.probabilities shape: [1, 3, 2]
        # dim 1 → policy index (0=sexual, 1=dangerous, 2=violence)
        # dim 2 → [No (safe), Yes (violation)]
        probs = output.probabilities.detach().cpu().squeeze(0)  # → [3, 2]

        policy_scores = {}
        failed_policies = []

        for i, policy in enumerate(POLICY_ORDER):
            no_score  = float(probs[i][0].item())  # safe
            yes_score = float(probs[i][1].item())  # violates policy

            policy_scores[policy] = {
                "no":  round(no_score,  4),
                "yes": round(yes_score, 4),
            }

            threshold = VIOLATION_THRESHOLDS[policy]
            if yes_score >= threshold:
                failed_policies.append(f"{policy} (yes={yes_score:.2f}, threshold={threshold})")

        print("policy_scores:", policy_scores)

        if failed_policies:
            return {
                "result": "flagged",
                "reason": f"Failed policies: {', '.join(failed_policies)}"
            }

        return {
            "result": "approved",
            "reason": f"Image passed moderation: {policy_scores}"
        }

    except Exception as e:
        return {
            "result": "pending",
            "reason": f"Image moderation failed: {str(e)}"
        }


def combine_results(text_check: dict, image_check: dict) -> dict:
    if text_check["result"] == "rejected":
        return {
            "moderation_status": "rejected",
            "moderation_reason": text_check["reason"]
        }

    if image_check["result"] == "rejected":
        return {
            "moderation_status": "rejected",
            "moderation_reason": image_check["reason"]
        }

    if text_check["result"] == "flagged" or image_check["result"] == "flagged":
        return {
            "moderation_status": "flagged",
            "moderation_reason": f"{text_check['reason']} | {image_check['reason']}"
        }

    if text_check["result"] == "pending" or image_check["result"] == "pending":
        return {
            "moderation_status": "pending",
            "moderation_reason": f"{text_check['reason']} | {image_check['reason']}"
        }

    return {
        "moderation_status": "approved",
        "moderation_reason": "Text and image passed moderation"
    }


def moderate_product(name: str, description: str, category: str, image_path: str | None = None) -> dict:
    print("Starting moderation...")

    text_check = check_text_policy(name, description, category)
    print(f"Text check done: {text_check['result']}")

    image_check = check_image_policy(image_path)
    print(f"Image check done: {image_check['result']}")

    final_result = combine_results(text_check, image_check)
    print(f"Final result: {final_result['moderation_status']}")

    return {
        "text_result":       text_check["result"],
        "text_reason":       text_check["reason"],
        "image_result":      image_check["result"],
        "image_reason":      image_check["reason"],
        "moderation_status": final_result["moderation_status"],
        "moderation_reason": final_result["moderation_reason"],
    }