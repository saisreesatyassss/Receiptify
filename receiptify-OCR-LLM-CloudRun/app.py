import os
import io
import json
from flask import Flask, request, jsonify
from google.cloud import vision
from vertexai import init
from vertexai.generative_models import GenerativeModel
from pyzbar.pyzbar import decode  # ✅ for QR/barcode decoding
from PIL import Image  # ✅ needed for pyzbar

# ✅ Path to Service Account JSON
SERVICE_KEY_PATH = "/app/keys/Vertex-OCR-Keys.json"
if os.path.exists("keys/Vertex-OCR-Keys.json"):
    SERVICE_KEY_PATH = "keys/Vertex-OCR-Keys.json"  # local dev fallback

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_KEY_PATH

# ✅ Google Cloud Config
PROJECT_ID = "civic-glow-467108-r0"
LOCATION = "us-central1"

# ✅ Initialize Vertex AI + Vision API clients
init(project=PROJECT_ID, location=LOCATION)
vision_client = vision.ImageAnnotatorClient()
gemini_model = GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

# ✅ OCR Helper
def ocr_extract_text_from_bytes(image_bytes):
    image = vision.Image(content=image_bytes)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

# ✅ QR/Barcode Helper using pyzbar
def detect_qr_from_bytes(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        decoded_objects = decode(img)

        for obj in decoded_objects:
            if obj.data:
                return obj.data.decode("utf-8")  # ✅ return first QR/barcode text
        return ""  # ✅ blank if none found
    except Exception as e:
        print("QR decode error:", e)
        return ""  # ✅ fail-safe blank

# ✅ Gemini JSON extraction Helper
def get_receipt_json(ocr_text: str):
    prompt = f"""
You are a receipt parsing assistant. I will give you OCR text from a shopping receipt.

Your task:
- Extract all purchased items.
- For each item: return itemName, itemTotalPrice, itemQuantity, and itemUnitSize (like 1L, 2kg, 1 pack, etc.).
- Predict totalCost as the sum of all itemTotalPrice values.
- Extract vendorName (store name) if present.
- Predict if purchase was ONLINE or OFFLINE.
- Categorize the receipt (groceries, entertainment, health, travel, fitness, bills, passes etc.).
- Extract receiptDate from the receipt in format YYYY-MM-DD. and ensure it's a billing date and not any other date. If missing, use today’s date 2025-07-27.
- Optionally predict a receiptExpiry if relevant (like 30 days later).
- Generate additionalAttributes with:
  - note: a one-line human-readable summary or insight about this purchase
  - any other useful details like paymentMethod, location, taxAmount or anything you think is relevant for the context to give insights later.

Return ONLY valid JSON in EXACTLY this schema (nothing else):

{{
  "items": [
    {{
      "itemName": "",
      "itemTotalPrice": 0,
      "itemQuantity": 0,
      "itemUnitSize": ""
    }}
  ],
  "receipt": {{
    "totalCost": 0,
    "vendorName": "",
    "mode": "",
    "receiptDate": "",
    "category": "",
    "receiptExpiry": "",
    "additionalAttributes": {{
      "note": "",
      "paymentMethod": ""
    }}
  }}
}}

Here is the receipt text:
{ocr_text}

Return ONLY the JSON object, no explanations, no extra fields other than inside additionalAttributes.
"""

    response = gemini_model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    # Parse the text as JSON safely
    try:
        parsed = json.loads(response.text)
        return parsed
    except json.JSONDecodeError:
        print("Gemini JSON decode failed:", response.text)
        return {
            "items": [],
            "receipt": {
                "totalCost": 0,
                "vendorName": "",
                "mode": "",
                "receiptDate": "",
                "category": "",
                "receiptExpiry": "",
                "additionalAttributes": {
                    "note": "LLM failed to parse JSON",
                    "paymentMethod": "",
                    "qrCode": ""
                }
            }
        }

@app.route("/")
def health_check():
    return "✅ OCR + Gemini API with QR support is running!", 200

@app.route("/process-receipt", methods=["POST"])
def process_receipt():
    if "receipt" not in request.files:
        return jsonify({"error": "No receipt file uploaded"}), 400

    file = request.files["receipt"].read()

    # 1️⃣ Run OCR
    ocr_text = ocr_extract_text_from_bytes(file)
    if not ocr_text:
        return jsonify({"error": "No text detected in receipt"}), 400

    # 2️⃣ Run QR/Barcode detection → get first QR text or blank
    qr_code_value = detect_qr_from_bytes(file)

    # 3️⃣ Run Gemini parsing → get structured JSON
    parsed_json = get_receipt_json(ocr_text)

    # 4️⃣ Inject single QR code into additionalAttributes
    if isinstance(parsed_json, dict) and "receipt" in parsed_json:
        if "additionalAttributes" not in parsed_json["receipt"]:
            parsed_json["receipt"]["additionalAttributes"] = {}
        parsed_json["receipt"]["additionalAttributes"]["qrCode"] = qr_code_value  # ✅ blank if not found

    return jsonify(parsed_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
