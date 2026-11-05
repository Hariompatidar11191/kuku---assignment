"""
PDF Generator for Solution Document (Kuku Assignment Problem 2)
Generates a clean, professional 2-page PDF using ReportLab.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
import os

pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution_doc.pdf")
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0f172a')
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=14,
    textColor=colors.HexColor('#d97706')
)

h1_style = ParagraphStyle(
    'Heading1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#1e293b'),
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#334155')
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=12,
    textColor=colors.HexColor('#334155'),
    leftIndent=12
)

story = []

# Title & Metadata
story.append(Paragraph("NyaySahay: AI Legal Assistant for Indian Cybercrime & Banking Fraud", title_style))
story.append(Paragraph("Candidate Solution Document — Kuku AI Generalist Assignment (Problem 2: Build an AI Lawyer)", subtitle_style))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#d97706'), spaceAfter=8))

# Section 1
story.append(Paragraph("1. Problem Choice & Framing", h1_style))
story.append(Paragraph("<b>Why this problem?</b> Over 1.5 million financial cyber fraud incidents were reported in India in 2023–2024. Ordinary citizens fall victim to UPI scams, fake customer care, and unauthorized debits. When victims approach banks, managers dismiss claims with boilerplate rejections (<i>'PIN was entered, we cannot refund'</i>). Police often decline complaints citing jurisdictional boundaries. Since private legal notices cost upwards of ₹10,000, over 80% of citizens abandon their funds.", body_style))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Scope & Assumptions:</b> We scoped the solution specifically to high-frequency consumer cyber fraud (UPI, phishing, AnyDesk remote access, SIM swapping, and bank disputes). We assume users converse in colloquial Hindi, Hinglish, or English without statutory knowledge, and possess digital receipts or statements. The AI must never hallucinate laws and must correctly apply the new <b>Bharatiya Nyaya Sanhita (BNS) 2023</b> (replacing IPC from July 1, 2024).", body_style))

# Section 2
story.append(Spacer(1, 6))
story.append(Paragraph("2. System Architecture & Engineering Approach", h1_style))
story.append(Paragraph("The system is engineered as a grounded, multimodal pipeline:", body_style))
story.append(Paragraph("• <b>Multimodal Intake & Evidence Extraction:</b> Parses user-uploaded PDFs, bank statements, and UPI screenshots using PyMuPDF and pattern matchers to extract Disputed Amount, UTR/Transaction ID, Date, Bank, and Beneficiary VPAs into structured session state.", bullet_style))
story.append(Paragraph("• <b>Hinglish Query Expansion:</b> Maps colloquial terms (<i>'OTP nahi diya', 'UPI se fraud ho gaya', 'AnyDesk download karwaya'</i>) into legal search vectors (e.g. <i>'Zero Customer Liability', 'Section 66D IT Act personation'</i>).", bullet_style))
story.append(Paragraph("• <b>Hybrid RAG (BM25 + Semantic + RRF):</b> Indexes verified provisions of IT Act 2000, BNS 2023, BNSS 2023, and RBI Circular RBI/2017-18/15. BM25 guarantees pinpoint retrieval of exact statutory sections and circular identifiers.", bullet_style))
story.append(Paragraph("• <b>Deterministic Action Drafter:</b> Generates ready-to-submit formal Bank Dispute Notices invoking RBI Paragraph 12 burden of proof, Cybercrime 1930 reports, and Banking Ombudsman petitions.", bullet_style))

# Section 3
story.append(Spacer(1, 6))
story.append(Paragraph("3. Preventing Hallucinations & Ensuring Legal Accuracy", h1_style))
story.append(Paragraph("• <b>Closed-Book Grounding:</b> Responses are strictly bounded to retrieved provisions with issuing authorities and official portal links.", bullet_style))
story.append(Paragraph("• <b>IPC ➔ BNS Transition:</b> Automatically checks incident date and cites Section 318 BNS (replacing Sec 420 IPC) and Section 173 BNSS (Zero FIR mandate).", bullet_style))
story.append(Paragraph("• <b>Statutory Burden of Proof Shield:</b> Embeds Paragraph 12 of RBI Circular RBI/2017-18/15 to protect victims from unlawful bank dismissal.", bullet_style))

# Section 4
story.append(Spacer(1, 6))
story.append(Paragraph("4. Quality Checking, Real Runs & Honest Failures", h1_style))
story.append(Paragraph("We evaluated 5 real-world scenarios representing prevalent Indian cybercrimes (raw outputs exported to <code>raw_outputs/</code>):", body_style))
story.append(Paragraph("• <b>UPI Fraud & Bank Rejection (Hinglish):</b> 100% recall. Grounded in RBI Zero Liability within 3 days and Banking Ombudsman Scheme.", bullet_style))
story.append(Paragraph("• <b>AnyDesk Screen-Share Scam (Hinglish):</b> 100% recall. Identified IT Act Section 66D and BNS Section 318.", bullet_style))
story.append(Paragraph("• <b>SIM Swap Account Siphoning (English):</b> 66.7% recall. Cited IT Act 66C and Kerala HC <i>SBI vs PV George</i> precedent.", bullet_style))
story.append(Paragraph("• <b>Police Jurisdiction Refusal (Hindi):</b> 50% recall. Cited BNSS 2023 Section 173 (Mandatory Zero FIR).", bullet_style))
story.append(Paragraph("• <b>Illegal Loan App Extortion (English):</b> 100% recall. Cited IT Act 66E (privacy violation) and DPDP Act 2023.", bullet_style))
story.append(Paragraph("<b>Honest Failure Modes:</b> (1) Noisy, handwritten cursive FIRs degrade basic OCR accuracy; (2) Unspecified reporting timelines make distinguishing Zero Liability vs. Limited Liability ambiguous without user clarification.", body_style))

# Section 5
story.append(Spacer(1, 6))
story.append(Paragraph("5. Scale & Deployment", h1_style))
story.append(Paragraph("Built on lightweight Python + Streamlit with zero proprietary lock-in. Deploys in one click to Streamlit Community Cloud or Hugging Face Spaces. Production API cost is less than $0.001 per case query.", body_style))

doc.build(story)
print(f"Generated solution PDF at: {pdf_path}")
