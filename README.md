# NyaySahay: Multimodal AI Legal Assistant for Indian Cybercrime & Banking Fraud
**Submission for Kuku AI Generalist Assignment — Problem 2: Build an AI Lawyer**

NyaySahay is a production-ready, grounded AI legal assistant engineered to help everyday Indian citizens navigate online financial fraud, UPI scams, unauthorized bank deductions, and illegal loan app extortion.

It allows victims to converse in **Hindi, English, or Hinglish**, upload supporting transaction documents/screenshots, receive verifiable legal advice backed by the **Bharatiya Nyaya Sanhita (BNS) 2023**, **IT Act 2000**, and **RBI Master Directions**, and generate ready-to-submit formal legal notices in one click.

---

## 🌟 Key Features

1. **Multilingual & Code-Mixed Conversational Intelligence**:
   - Understands colloquial Hindi, English, and Hinglish queries (*"UPI se 50000 cut gaya, OTP nahi diya, bank mana kar raha hai"*).
   - Translates emotional, everyday stories into precise Indian statutory claims.
2. **Authoritative Knowledge Base & Hybrid Retrieval (BM25 + RRF)**:
   - Indexes verified provisions of:
     - **Information Technology Act, 2000**: Sections 43, 66, 66C (Identity theft/SIM swap), 66D (Cheating by personation/phishing), 66E (Privacy violation).
     - **Bharatiya Nyaya Sanhita (BNS), 2023**: Section 318 (Cheating), Section 319 (Cheating by personation), Section 316 (Criminal breach of trust).
     - **Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023**: Section 173 (Mandatory Zero FIR).
     - **RBI Master Circular RBI/2017-18/15**: Zero Customer Liability within 3 days; statutory burden of proof on the bank (Paragraph 12); mandatory 10-day shadow reversal.
     - **Reserve Bank - Integrated Ombudsman Scheme, 2021**: Escalation to CMS portal for rejection or deficiency in service, with compensation up to ₹1 Lakh for mental harassment.
     - **Judicial Precedents**: Kerala High Court (*SBI vs P.V. George*) and NCDRC (*PNB vs Leader Valves*).
3. **Multimodal Document Evidence Extractor**:
   - Upload bank statement PDFs, UPI transaction screenshots, payment receipts, or police acknowledgment slips.
   - Automatically extracts Disputed Amount, Transaction / UTR ID, Date, Bank Name, and Beneficiary VPAs.
4. **Automated Action Drafting Suite**:
   - **Bank Dispute & Zero-Liability Notice**: Formally demands shadow credit under RBI Circular Paragraph 6 & 12 within 10 working days.
   - **National Cyber Crime Reporting Portal Complaint (1930 / cybercrime.gov.in)**: Formatted for the Citizen Financial Cyber Fraud Reporting System.
   - **RBI Banking Ombudsman Escalation Petition**: Formatted for cms.rbi.org.in.
5. **Zero Hallucination Guardrails**:
   - Closed-book grounding: Every legal claim is linked directly to official government sources and URLs.
   - Clear distinction between statutory criminal law, regulatory directions, and emergency procedures.

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11 and 3.13)
- pip

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Launch the interactive Streamlit app:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

*(Optional)* To use OpenAI GPT-4o-mini for natural conversational responses, set your API key:
```bash
export OPENAI_API_KEY="your-api-key-here"  # Linux/macOS
set OPENAI_API_KEY=your-api-key-here      # Windows CMD
$env:OPENAI_API_KEY="your-api-key-here"   # Windows PowerShell
```
*Note: If no API key is provided, NyaySahay runs on its built-in deterministic Indian Legal Reasoning Engine with full statutory grounding!*

---

## 🌐 2-Minute Live Deployment Guide

The brief permits hosting on **Streamlit Community Cloud** or **Hugging Face Spaces** (both completely free):

### Option A: Streamlit Community Cloud (Recommended - 2 Minutes)
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New App"**, select this repository and set Main file path to `app.py`.
4. (Optional) In Advanced Settings, add `OPENAI_API_KEY` under Secrets.
5. Click **"Deploy"** — you receive a live public URL (e.g., `https://nyaysahay-legal-ai.streamlit.app`) to share in the assignment form!

### Option B: Hugging Face Spaces (2 Minutes)
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Select **Streamlit** as the Space SDK.
3. Push or upload these files to the Space.
4. The Space builds and runs automatically with a public URL.

---

## 📊 Evaluation & Verification

To run the automated benchmark across 5 realistic Indian fraud scenarios:
```bash
python test_cases/run_evaluation.py
```
Results and unedited raw outputs are automatically saved to `raw_outputs/`:
- `TEST_01_UPI_FRAUD_BANK_REJECTION_output.txt` (100% recall)
- `TEST_02_REMOTE_ACCESS_ANYDESK_output.txt` (100% recall)
- `TEST_03_SIM_SWAP_FRAUD_output.txt` (66.7% recall)
- `TEST_04_POLICE_JURISDICTION_REFUSAL_output.txt` (50% recall)
- `TEST_05_LOAN_APP_HARASSMENT_output.txt` (100% recall)

---

## 📁 Submission Deliverables Summary

| Item | Location in Repo |
| :--- | :--- |
| **Solution Doc (PDF)** | [`solution_doc.pdf`](./solution_doc.pdf) *(2 pages)* |
| **Solution Doc (Markdown)** | [`solution_doc.md`](./solution_doc.md) |
| **Raw Unedited Outputs** | [`raw_outputs/`](./raw_outputs/) |
| **Interactive Prototype** | [`app.py`](./app.py) |
| **Curated Legal Knowledge Base** | [`legal_kb/legal_database.json`](./legal_kb/legal_database.json) |
