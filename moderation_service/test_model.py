from transformers import AutoProcessor, ShieldGemma2ForImageClassification

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

print("Model loaded successfully")