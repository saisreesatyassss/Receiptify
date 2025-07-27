# 🧾 Project Raseed – Your AI-powered Receipt & Financial Companion  

![Google Cloud](https://img.shields.io/badge/Built%20with-Google%20Cloud-blue?logo=googlecloud)  
![Hackathon](https://img.shields.io/badge/Google-Agentic%20AI%20Hackathon-orange?logo=google)  
![License](https://img.shields.io/badge/license-MIT-green)  

> **“Every purchase becomes a step toward better financial health.”**

---

## 🚀 What is Project Raseed?  

Project Raseed is a **revolutionary AI-powered personal finance assistant** that transforms how users **manage receipts, track expenses, and make smarter financial decisions** – all seamlessly integrated into **Google Wallet**.  

Built exclusively with **Google AI technologies (Gemini, Vertex AI Agent Builder, Google Wallet API, Firebase)**, it goes **beyond traditional receipt scanning** by offering:  

✅ Multimodal understanding (photo, voice, text)  
✅ Local language & code-mixed queries  
✅ Proactive financial insights & nudges  
✅ Interactive, live-updating Google Wallet passes  

---

## 🌟 Why is Raseed Different?  

- **More than OCR** → It doesn’t just scan receipts; it *understands* them, even if multilingual, messy, or incomplete.  
- **Always-on Agent** → Proactively monitors trends, detects anomalies, and gives insights *without being asked*.  
- **Google Wallet-First** → Insights, receipts & shopping lists delivered as live-updating Wallet passes.  
- **Local Language + Context Awareness** → Supports Hinglish, regional Indian languages & natural conversational queries.  
- **From Tracking → Transformation** → Builds a *real-time financial feedback loop* helping users improve spending habits.  

---

## 🛠 Tech Stack  

| **Technology** | **Purpose** |
|----------------|------------|
| **Gemini Vision API** | Extracts structured data (items, prices, taxes) from receipt images, even if damaged. |
| **Gemini Pro (Vertex AI)** | Multimodal reasoning for spending patterns, financial queries & recommendations. |
| **Vertex AI Agent Builder** | Conversational AI that understands context, behavior, & local language queries. |
| **Google Wallet API** | Creates & updates interactive Wallet passes (receipts, savings tips, shopping lists). |
| **Firebase Firestore** | Cloud database for receipts, spending history & transaction metadata. |
| **Firebase Cloud Messaging** | Push notifications for budget warnings, savings nudges & shopping list updates. |
| **Flutter Frontend** | Cross-platform mobile app for scanning receipts, chatting with the AI, and managing Wallet passes. |

---

## ✨ Core Features  

### ✅ 1. Multimodal Smart Ingestion  
- Scan receipts via **camera** (even poor lighting/damaged receipts)  
- Input via **voice** or **multilingual text**  
- Instantly extract **store name, total, taxes, items**  

### ✅ 2. Organized Cloud Storage  
- Auto-tag & categorize (Groceries, Fuel, Shopping…)  
- Securely stored in **Firestore**, fully searchable  

### ✅ 3. Conversational AI Assistant  
- Ask: *“Kal ka grocery kitna tha?”* or *“Did I overspend last week?”*  
- Supports Hinglish & regional languages  
- Understands intent & gives **context-aware responses**  

### ✅ 4. Spending Analysis & Predictive Insights  
- Detect **overspending**, track budgets, forecast future purchases  
- Identify **emotional spending** & risky spending patterns  
- Suggest **optimized shopping times & locations**  

### ✅ 5. Live Google Wallet Passes  
- Receipts, shopping lists & financial tips **as live Wallet passes**  
- Passes auto-update with **push notifications**  

### ✅ 6. Inventory-Aware Smart Lists  
- Detects **low-stock items** from purchase history  
- Creates **predictive shopping lists** merging inventory awareness + hyperlocal prices  

### ✅ 7. Gamified Financial Journey  
- Level up, unlock **savings achievements**, compete on leaderboards  
- Turn finance into an **RPG-style journey**  

---

## 🏗 Solution Architecture  

```mermaid
graph TD
    A[Flutter Mobile App] -->|Uploads receipt| B[Gemini Vision API]
    B -->|Extracted data| C[Firestore Database]
    A -->|Voice/Text query| D[Vertex AI Agent Builder]
    D -->|Insights & Suggestions| A
    C -->|Spend Analysis| E[Gemini Pro - Vertex AI]
    E -->|Predictions & Alerts| D
    D -->|Live Wallet Pass| F[Google Wallet API]
    F -->|Interactive passes| A
    E -->|Budget nudges| G[Firebase Cloud Messaging]
    G -->|Notifications| A

### Setup
1. Clone the repository:
    ⁠bash
   git clone https://github.com/saisreesatyassss/Receiptify.git
   cd Receiptify/receiptify_flutter_app
⁠ `

2. Install dependencies:

    ⁠bash
   flutter pub get
   
⁠ 3. Configure Firebase (replace `google-services.json` for Android and `GoogleService-Info.plist` for iOS).
4. Run the app:

    ⁠bash
   flutter run