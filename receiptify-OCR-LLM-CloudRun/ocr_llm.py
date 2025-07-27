import os
import io
from google.cloud import vision
from vertexai import init
from vertexai.generative_models import GenerativeModel

# ✅ 1. Set Google Service Account Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/mohan/Programming/Receiptify/keys/Vertex-OCR-Keys.json"

# ✅ 2. Project Config
PROJECT_ID = "civic-glow-467108-r0"  # your actual project ID
LOCATION = "us-central1"

# ✅ 3. Initialize Vertex AI
init(project=PROJECT_ID, location=LOCATION)

# ✅ 4. Setup Gemini Model (use flash for cost/speed, pro for better reasoning)
gemini_model = GenerativeModel("gemini-2.5-flash")

# ✅ OCR function
def ocr_extract_text(image_path):
    vision_client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    return texts[0].description if texts else ""

# ✅ Gemini JSON extraction function
def get_receipt_json(ocr_text: str):
    prompt = f"""
You are a receipt parsing assistant.
I will give you the OCR text from a shopping receipt.

Your task:
- Extract vendor name
- Extract purchase date (if missing, use today's date)
- Extract total cost
- Extract all line items with name, quantity, price, size, and measure type
- Predict if purchase was ONLINE or OFFLINE
- Categorize purchase (groceries, entertainment, health, travel, etc.)
- Add any extra info in "additionalAttributes"
- Generate a one-line human-readable summary as "note"

Return ONLY valid JSON in this schema:

{{
  "master": {{
    "receiptId": "",
    "userId": null,
    "itemsList": [],
    "totalCost": 0,
    "vendorName": "",
    "mode": "",
    "category": "",
    "date": "",
    "additionalAttributes": {{
      "note": "",
      "paymentMethod": "",
      "taxAmount": 0
    }}
  }},
  "items": [
    {{
      "itemId": "",
      "itemName": "",
      "itemPrice": 0,
      "itemQuantity": 0,
      "measureType": "",
      "measureSize": 0
    }}
  ]
}}

Now here is the receipt text:
{ocr_text}

Return ONLY JSON. No explanation.
"""

    response = gemini_model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}  # enforce JSON output
    )
    return response.text

# ✅ Main pipeline
if __name__ == "__main__":
    sample_image = "/Users/mohan/Programming/Receiptify/sample_images/parking-receipt-twentyone.png"

    print("🔍 Running OCR...")
    ocr_text = ocr_extract_text(sample_image)
    print("\n📄 OCR Result:\n", ocr_text)

    print("\n🤖 Sending OCR text to Gemini for JSON parsing...")
    result_json = get_receipt_json(ocr_text)

    print("\n✅ Final Structured JSON:\n", result_json)
