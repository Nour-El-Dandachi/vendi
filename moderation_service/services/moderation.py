from PIL import Image
from transformers import AutoProcessor, ShieldGemma2ForImageClassification
import torch

model_id = "google/shieldgemma-2-4b-it"

processor = AutoProcessor.from_pretrained(
    model_id,
    trust_remote_code=True
)

model = ShieldGemma2ForImageClassification.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto"
)

LABELS = ["No", "Yes"]

TEXT_REJECT_KEYWORDS = {
    "weapon", "gun", "knife", "bomb", "explosive", "drugs", "cocaine",
    "weed", "cannabis", "vape", "nicotine", "alcohol", "porn", "nude",
    "sex toy", "counterfeit", "fake", "hate", "nazi"
}

TEXT_FLAG_KEYWORDS = {
    "replica", "copy", "inspired", "adult", "18+", "smoking", "tobacco",
    "supplement", "military", "ammo"
}


def check_text_policy(name: str, description: str, category: str):
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


def check_image_policy(image_path: str | None):
    if not image_path:
        return {
            "result": "pending",
            "reason": "No image provided"
        }

    try:
        image = Image.open(image_path).convert("RGB")

        policies = ["sexual", "dangerous", "violence"]

        inputs = processor(
            images=[image],
            policies=policies,
            return_tensors="pt"
        ).to(model.device)

        with torch.no_grad():
            output = model(**inputs)

        probabilities = output.probabilities.detach().cpu().squeeze(0)

        policy_scores = {}
        failed_policies = []

        for i, policy in enumerate(policies):
            no_score = float(probabilities[i][0].item())
            yes_score = float(probabilities[i][1].item())

            policy_scores[policy] = {
                "no": round(no_score, 4),
                "yes": round(yes_score, 4),
            }

            # For ShieldGemma built-in policies, YES means compliant/safe
            if yes_score < 0.50:
                failed_policies.append(f"{policy} (yes={yes_score:.2f})")

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



def combine_results(text_check, image_check):
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


def moderate_product(name: str, description: str, category: str, image_path: str | None = None):
    text_check = check_text_policy(name, description, category)
    image_check = check_image_policy(image_path)
    final_result = combine_results(text_check, image_check)

    return {
        "text_result": text_check["result"],
        "text_reason": text_check["reason"],
        "image_result": image_check["result"],
        "image_reason": image_check["reason"],
        "moderation_status": final_result["moderation_status"],
        "moderation_reason": final_result["moderation_reason"],
    }


def moderate_product(name: str, description: str, category: str, image_path: str | None = None):
    print("Starting moderation...")
    text_check = check_text_policy(name, description, category)
    print("Text check done")

    image_check = check_image_policy(image_path)
    print("Image check done")

    final_result = combine_results(text_check, image_check)
    print("Combine done")

    return {
        "text_result": text_check["result"],
        "text_reason": text_check["reason"],
        "image_result": image_check["result"],
        "image_reason": image_check["reason"],
        "moderation_status": final_result["moderation_status"],
        "moderation_reason": final_result["moderation_reason"],
    }