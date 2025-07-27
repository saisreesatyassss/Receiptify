import os
from vertexai import init
from vertexai.generative_models import GenerativeModel

# 1️⃣ Authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/mohan/Programming/Receiptify/keys/Vertex-OCR-Keys.json"

# 2️⃣ Init Vertex AI
PROJECT_ID = "civic-glow-467108-r0"  # replace with your GCP project ID
LOCATION = "us-central1"        # Gemini available globally
init(project=PROJECT_ID, location=LOCATION)

# 3️⃣ Load Gemini Pro
model = GenerativeModel("gemini-2.5-flash")

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

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}  # enforce JSON mode
    )

    return response.text

if __name__ == "__main__":
    # Sample OCR text
    raw_ocr_text = """ROYAL MART
Invoice #12345
Date: 25-07-2025
Surf Excel 2L x3 600
Marie Biscuit 200g x2 30
TOTAL 457.50
Paid via UPI"""

    result_json = get_receipt_json(raw_ocr_text)
    print("Structured JSON:\n", result_json)
