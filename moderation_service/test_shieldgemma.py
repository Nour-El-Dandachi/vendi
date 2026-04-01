"""
Run this script DIRECTLY with: python test_shieldgemma.py
Do NOT run through FastAPI/uvicorn.
This is a pure reproduction of the official HuggingFace example.
"""

import torch
import requests
from PIL import Image
from transformers import AutoProcessor, ShieldGemma2ForImageClassification

print("Torch version:", torch.__version__)
print("Transformers version:", __import__('transformers').__version__)

model_id = "google/shieldgemma-2-4b-it"

print("\nLoading model...")
processor = AutoProcessor.from_pretrained(model_id)
model = ShieldGemma2ForImageClassification.from_pretrained(
    model_id,
    torch_dtype=torch.float32
).eval()

print("Model dtype:", next(model.parameters()).dtype)
print("Model device:", next(model.parameters()).device)

# ── Test 1: Official bee image from HuggingFace docs ──────────────────────────
print("\n--- Test 1: Official bee image (should be SAFE) ---")
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"
bee_image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
print("Image size:", bee_image.size, "Mode:", bee_image.mode)

inputs = processor(images=[bee_image], return_tensors="pt")
with torch.inference_mode():
    output = model(**inputs)

print("RAW probabilities tensor:", output.probabilities)
print("Shape:", output.probabilities.shape)

probs = output.probabilities.squeeze(0)
policies = ["sexual", "dangerous", "violence"]
for i, policy in enumerate(policies):
    print(f"  {policy}: no={probs[i][0]:.4f}, yes={probs[i][1]:.4f}")

# ── Test 2: Your local image ──────────────────────────────────────────────────
import sys
if len(sys.argv) > 1:
    local_path = sys.argv[1]
    print(f"\n--- Test 2: Your local image ({local_path}) ---")
    local_image = Image.open(local_path).convert("RGB")
    print("Image size:", local_image.size, "Mode:", local_image.mode)

    inputs2 = processor(images=[local_image], return_tensors="pt")
    with torch.inference_mode():
        output2 = model(**inputs2)

    print("RAW probabilities tensor:", output2.probabilities)
    probs2 = output2.probabilities.squeeze(0)
    for i, policy in enumerate(policies):
        print(f"  {policy}: no={probs2[i][0]:.4f}, yes={probs2[i][1]:.4f}")