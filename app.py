"""
NyaySahay: Multimodal AI Legal Assistant for Indian Cybercrime & Banking Fraud
Production-ready Streamlit Application for Kuku AI Generalist Assignment (Problem 2)
"""

import streamlit as st
import os
import json
from datetime import datetime
from legal_kb.retriever import legal_retriever
from core.doc_processor import doc_processor
from core.legal_drafter import legal_drafter
from core.legal_engine import legal_engine

# Page Configuration
st.set_page_config(
    page_title="NyaySahay | AI Legal Assistant for Indian Cybercrime & Banking Fraud",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Professional Legal Tech Theme: Obsidian & Gold)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        color: #f8fafc;
    }
    .header-title {
        font-size: 26px;
        font-weight: 700;
        color: #f59e0b;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
    }
    .emergency-banner {
        background: #450a0a;
        border: 1px solid #dc2626;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #fecaca;
        font-size: 13px;
    }
    .emergency-btn {
        background: #dc2626;
        color: white;
        padding: 5px 14px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: none;
        font-size: 12px;
    }
    .citation-card {
        background: #1e293b;
        border-left: 4px solid #f59e0b;
        border-radius: 6px;
        padding: 12px 14px;
        margin-top: 8px;
        margin-bottom: 8px;
        font-size: 13px;
    }
    .citation-title {
        color: #fbbf24;
        font-weight: 600;
    }
    .statute-tag {
        background: #334155;
        color: #e2e8f0;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
    }
    .extracted-fact-box {
        background: #064e3b;
        border: 1px solid #059669;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 15px;
        color: #d1fae5;
        font-size: 13px;
    }
    .timeline-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "case_facts" not in st.session_state:
    st.session_state.case_facts = {
        "disputed_amount": None,
        "transaction_id": None,
        "transaction_date": None,
        "detected_bank": None,
        "vpa_beneficiary": None,
        "complaint_ref_no": None,
        "uploaded_filename": None
    }


# =====================================================================
# SIDEBAR: Language, Document Upload, Case Facts, Action Drafting
# =====================================================================
with st.sidebar:
    st.markdown("### ⚙️ Language & Controls")
    lang_choice = st.selectbox(
        "Preferred Response Language",
        options=["auto", "hinglish", "hindi", "english"],
        format_func=lambda x: {
            "auto": "🌐 Auto-Detect (Hindi / Hinglish / English)",
            "hinglish": "🗣️ Hinglish (Conversational Roman Hindi)",
            "hindi": "🇮🇳 हिंदी (Hindi Devanagari)",
            "english": "🇬🇧 English"
        }[x]
    )

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # API Key Configuration (Free-Tier & Paid Supported)
    with st.expander("🔑 AI Provider & Free API Key (Optional)", expanded=False):
        ai_provider = st.selectbox(
            "Select AI Provider",
            options=["local", "groq", "gemini", "openai"],
            format_func=lambda x: {
                "local": "🖥️ Built-in Engine (Free - No Key Needed)",
                "groq": "⚡ Groq (100% Free Tier - Llama 3.3)",
                "gemini": "✨ Google Gemini (Free Tier)",
                "openai": "🤖 OpenAI (GPT-4o-mini)"
            }[x]
        )

        if ai_provider == "local":
            st.caption("✅ Runs 100% locally on hybrid BM25 and 122 Indian legal knowledge chunks. Zero cost.")
            legal_engine.configure_provider("local", "")
        elif ai_provider == "groq":
            st.caption("👉 Get your instant free key from [console.groq.com/keys](https://console.groq.com/keys)")
            groq_key = st.text_input("Enter Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
            if groq_key:
                legal_engine.configure_provider("groq", groq_key)
                st.success("Groq Free API connected!")
        elif ai_provider == "gemini":
            st.caption("👉 Get your free key from [aistudio.google.com](https://aistudio.google.com)")
            gemini_key = st.text_input("Enter Google Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
            if gemini_key:
                legal_engine.configure_provider("gemini", gemini_key)
                st.success("Google Gemini Free API connected!")
        elif ai_provider == "openai":
            st.caption("👉 Enter your OpenAI key from [platform.openai.com](https://platform.openai.com)")
            openai_key = st.text_input("Enter OpenAI Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
            if openai_key:
                legal_engine.configure_provider("openai", openai_key)
                st.success("OpenAI API connected!")

    st.markdown("---")
    st.markdown("### 📄 Evidence Document Upload")
    st.caption("Upload Bank Statement PDFs, UPI Screenshots, FIR Copies, or Cyber Complaints.")
    
    uploaded_file = st.file_uploader(
        "Choose PDF or Image file",
        type=["pdf", "txt", "png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if st.session_state.case_facts.get("uploaded_filename") != uploaded_file.name:
            with st.spinner("Analyzing document and extracting case facts..."):
                parsed = doc_processor.parse_uploaded_file(uploaded_file)
                facts = parsed["facts"]
                st.session_state.case_facts.update({
                    "disputed_amount": facts.get("disputed_amount"),
                    "transaction_id": facts.get("transaction_id"),
                    "transaction_date": facts.get("transaction_date"),
                    "detected_bank": facts.get("detected_bank"),
                    "vpa_beneficiary": facts.get("vpa_beneficiary"),
                    "complaint_ref_no": facts.get("complaint_ref_no"),
                    "uploaded_filename": uploaded_file.name
                })
                st.toast("✅ Evidence facts extracted successfully!")

    # Display Extracted Case Facts Card
    cf = st.session_state.case_facts
    if any([cf["disputed_amount"], cf["transaction_id"], cf["detected_bank"], cf["transaction_date"]]):
        st.markdown(f"""
        <div class="extracted-fact-box">
            <b>📋 Extracted Evidence Facts:</b><br>
            • <b>Amount:</b> {cf['disputed_amount'] or 'Not detected'}<br>
            • <b>Txn / UTR ID:</b> {cf['transaction_id'] or 'Not detected'}<br>
            • <b>Bank/App:</b> {cf['detected_bank'] or 'Not detected'}<br>
            • <b>Date:</b> {cf['transaction_date'] or 'Not detected'}<br>
            • <b>Beneficiary:</b> {cf['vpa_beneficiary'] or 'N/A'}<br>
            • <b>Complaint Ref:</b> {cf['complaint_ref_no'] or 'N/A'}
        </div>
        """, unsafe_allow_html=True)
        if st.button("Reset Facts", use_container_width=True):
            st.session_state.case_facts = {
                "disputed_amount": None,
                "transaction_id": None,
                "transaction_date": None,
                "detected_bank": None,
                "vpa_beneficiary": None,
                "complaint_ref_no": None,
                "uploaded_filename": None
            }
            st.rerun()

    st.markdown("---")
    all_statutes = legal_retriever.get_all_statutes()
    st.info(f"🧠 **Knowledge Base Active:** {len(all_statutes)} chunks indexed from 42 authoritative files in `kuku data` (IT Act, BNS 2023, RBI Circulars, Supreme Court & High Court cases).")


# =====================================================================
# MAIN WORKSPACE (TABBED INTERFACE)
# =====================================================================

# Header
st.markdown("""
<div class="main-header">
    <div class="header-title">
        ⚖️ NyaySahay | AI Legal Assistant for Indian Cybercrime & Banking Fraud
    </div>
    <div class="header-subtitle">
        Empowering Indian citizens with grounded legal guidance under Bharatiya Nyaya Sanhita (BNS) 2023, IT Act 2000, and RBI Limited Customer Liability Regulations.
    </div>
</div>
""", unsafe_allow_html=True)

# Emergency Golden Hour Alert
st.markdown("""
<div class="emergency-banner">
    <div>
        🚨 <b>Golden Hour Alert:</b> Financial cyber fraud within the last 2 hours? Dial <b>1930</b> immediately or visit <b>cybercrime.gov.in</b> to freeze scammer accounts!
    </div>
    <a href="https://cybercrime.gov.in" target="_blank" class="emergency-btn">Visit 1930 Portal</a>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_drafts, tab_timeline, tab_kb = st.tabs([
    "💬 AI Legal Chat",
    "📝 1-Click Notice & Petition Drafter",
    "📊 Case Facts & Evidence Matrix",
    "📚 Browse Knowledge Base (122 Chunks)"
])

# ---------------------------------------------------------------------
# TAB 1: AI LEGAL CHAT
# ---------------------------------------------------------------------
with tab_chat:
    # Quick Prompt Starters (if conversation empty)
    if not st.session_state.messages:
        st.markdown("##### 💡 Select a realistic test scenario or type your own case below:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💸 'Mere account se ₹50,000 UPI fraud ho gaya. OTP nahi bataya. Bank reject kar raha hai.'", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Mere account se ₹50,000 UPI ke through fraud ho gaya. Maine kisi ko OTP nahi bataya. Bank meri complaint reject kar raha hai. Ab main kya kar sakta hoon?"})
                st.rerun()
            if st.button("📞 'Fake customer care ne AnyDesk download karwaya aur paise cut gaye.'", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Ek fake customer care number par call kiya tha, unhone AnyDesk install karwaya aur mere bank se 1 lakh nikal gaye. Kaunsa kanoon lagega?"})
                st.rerun()
        with col2:
            if st.button("📱 'SIM band ho gaya aur mere bank account se paise nikal gaye (SIM Swap Fraud).'", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Mera mobile SIM achanak band ho gaya, aur 2 ghante baad pata chala ki net banking se saara balance transfer ho chuka hai. Kya mujhe refund milega?"})
                st.rerun()
            if st.button("🚔 'Police station bola ki cyber fraud ka case yahan nahi likhenge.'", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Local police station ne bola ki fraud dusre state se hua hai isliye wo FIR nahi likhenge. Kya police mana kar sakti hai?"})
                st.rerun()

    # Render Conversation History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="⚖️" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
            
            # Show verified citations accordion under assistant message
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("📖 Verified Legal Citations & Official Authorities", expanded=False):
                    for src in msg["sources"]:
                        source_label = f"📁 Source: `{src.get('source_file')}` | " if src.get('source_file') else ""
                        st.markdown(f"""
                        <div class="citation-card">
                            <div class="citation-title">{src['act']} — {src['section']}</div>
                            <div><b>{src['title']}</b></div>
                            <div><i>{source_label}Issuing Authority:</i> {src['issuing_authority']} | <i>Effective Date:</i> {src['effective_date']}</div>
                            <div><b>Official Source:</b> <a href="{src['source_url']}" target="_blank">{src['source_url']}</a></div>
                            <div style="margin-top:6px; color:#cbd5e1;">{src['summary']}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # Handle New Chat Input
    user_input = st.chat_input("Type your legal issue or reply to the assistant in Hindi, English, or Hinglish...")

    # Determine if a prompt was triggered (via button or text input)
    new_user_prompt = None
    if user_input:
        new_user_prompt = user_input
        st.session_state.messages.append({"role": "user", "content": new_user_prompt})
        st.rerun()

    # If the last message is from the user, generate the assistant's reply
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        latest_user_query = st.session_state.messages[-1]["content"]

        with st.chat_message("assistant", avatar="⚖️"):
            with st.spinner("Analyzing case facts, asking clarifying questions, and retrieving statutes..."):
                history_tuples = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
                
                result = legal_engine.generate_response(
                    user_message=latest_user_query,
                    conversation_history=history_tuples,
                    case_facts=st.session_state.case_facts,
                    language=lang_choice
                )
                
                response_text = result["answer"]
                sources = result["sources"]
                
                st.markdown(response_text)
                
                if sources:
                    with st.expander("📖 Verified Legal Citations & Official Authorities", expanded=True):
                        for src in sources:
                            source_label = f"📁 Source: `{src.get('source_file')}` | " if src.get('source_file') else ""
                            st.markdown(f"""
                            <div class="citation-card">
                                <div class="citation-title">{src['act']} — {src['section']}</div>
                                <div><b>{src['title']}</b></div>
                                <div><i>{source_label}Issuing Authority:</i> {src['issuing_authority']} | <i>Effective Date:</i> {src['effective_date']}</div>
                                <div><b>Official Source:</b> <a href="{src['source_url']}" target="_blank">{src['source_url']}</a></div>
                                <div style="margin-top:6px; color:#cbd5e1;">{src['summary']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sources": sources
                })
                st.rerun()

# ---------------------------------------------------------------------
# TAB 2: LEGAL ACTION DRAFTER
# ---------------------------------------------------------------------
with tab_drafts:
    st.markdown("### 📝 Ready-to-Submit Formal Legal Petitions")
    st.caption("Auto-populated from evidence extracted from your uploaded documents.")

    doc_tab1, doc_tab2, doc_tab3 = st.tabs(["🏦 Bank Dispute Notice", "🚔 Cybercrime 1930 Portal", "⚖️ RBI Ombudsman Petition"])
    cf = st.session_state.case_facts

    with doc_tab1:
        st.markdown("#### Bank Dispute Notice (Zero Customer Liability)")
        st.info("💡 Invokes Paragraph 6 & 12 of RBI Master Circular RBI/2017-18/15. Demands shadow credit within 10 working days.")
        col_a, col_b = st.columns(2)
        with col_a:
            c_name = st.text_input("Customer Name", value="Ramesh Kumar", key="d_name")
            c_acc = st.text_input("Account Number", value="XXXXXX1234", key="d_acc")
            c_bank = st.text_input("Bank Name", value=cf["detected_bank"] or "State Bank of India", key="d_bank")
        with col_b:
            c_amt = st.text_input("Disputed Amount", value=cf["disputed_amount"] or "₹50,000", key="d_amt")
            c_utr = st.text_input("Transaction / UTR ID", value=cf["transaction_id"] or "UPI/412389102931", key="d_utr")
            c_date = st.text_input("Transaction Date", value=cf["transaction_date"] or datetime.now().strftime("%d-%m-%Y"), key="d_date")

        bank_notice_txt = legal_drafter.generate_bank_grievance_notice(
            customer_name=c_name,
            account_number=c_acc,
            bank_name=c_bank,
            disputed_amount=c_amt,
            transaction_id=c_utr,
            transaction_date=c_date,
            incident_narrative="Unauthorized electronic transfer occurred from my account. I did not share credentials or OTP with anyone.",
            notified_within_3_days=True
        )
        st.text_area("Preview Draft Notice", bank_notice_txt, height=260)
        st.download_button(
            label="📥 Download Bank Dispute Notice (.txt)",
            data=bank_notice_txt,
            file_name=f"Bank_Dispute_Notice_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with doc_tab2:
        st.markdown("#### National Cyber Crime Reporting Portal Complaint")
        st.info("💡 Formatted for submission on https://cybercrime.gov.in and Helpline 1930. Automatically cites IT Act Section 66D and BNS Section 318.")
        v_phone = st.text_input("Complainant Mobile", value="9876543210", key="cp_vphone")
        v_suspect = st.text_input("Suspect UPI / Mobile / Link", value=cf["vpa_beneficiary"] or "scammer@okaxis / 9876500000", key="cp_vsuspect")

        cyber_complaint_txt = legal_drafter.generate_cybercrime_complaint(
            victim_name=c_name,
            victim_phone=v_phone,
            disputed_amount=c_amt,
            transaction_id=c_utr,
            transaction_date=c_date,
            suspect_details=v_suspect,
            incident_narrative="Online financial cheating and unauthorized debit via UPI fraud."
        )
        st.text_area("Preview Cyber Complaint", cyber_complaint_txt, height=260)
        st.download_button(
            label="📥 Download Cybercell Complaint (.txt)",
            data=cyber_complaint_txt,
            file_name=f"Cyber_Complaint_1930_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with doc_tab3:
        st.markdown("#### RBI Integrated Ombudsman Scheme Petition")
        st.info("💡 For escalation on https://cms.rbi.org.in when bank fails to resolve within 30 days or rejects without proving customer fault. Claims refund + ₹1,00,000 for mental agony.")
        c_ticket = st.text_input("Bank Grievance Ticket ID", value=cf["complaint_ref_no"] or "BANK-GRIEVANCE-98124", key="om_ticket")

        ombuds_txt = legal_drafter.generate_ombudsman_petition(
            customer_name=c_name,
            bank_name=c_bank,
            account_number=c_acc,
            complaint_ticket_no=c_ticket,
            rejection_date=datetime.now().strftime("%d-%m-%Y"),
            disputed_amount=c_amt,
            summary_of_rejection="Bank summarily rejected dispute asserting OTP was entered, violating RBI burden of proof mandate."
        )
        st.text_area("Preview Ombudsman Petition", ombuds_txt, height=260)
        st.download_button(
            label="📥 Download Ombudsman Petition (.txt)",
            data=ombuds_txt,
            file_name=f"RBI_Ombudsman_Complaint_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---------------------------------------------------------------------
# TAB 3: CASE FACTS & TIMELINE
# ---------------------------------------------------------------------
with tab_timeline:
    st.markdown("### 📊 Case Evidence & Facts Matrix")
    st.caption("Extracted metadata from uploaded bank statements, payment receipts, and chat narrative.")
    
    cf = st.session_state.case_facts
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div class="timeline-card">
            <h4>📋 Disputed Transaction Summary</h4>
            <table style="width:100%; border-collapse: collapse;">
                <tr><td style="padding:6px; color:#94a3b8;">Disputed Amount:</td><td style="padding:6px; font-weight:bold; color:#f59e0b;">{cf['disputed_amount'] or '₹50,000 (Sample)'}</td></tr>
                <tr><td style="padding:6px; color:#94a3b8;">Transaction / UTR ID:</td><td style="padding:6px; font-weight:bold;">{cf['transaction_id'] or 'UPI/412389102931'}</td></tr>
                <tr><td style="padding:6px; color:#94a3b8;">Detected Bank:</td><td style="padding:6px; font-weight:bold;">{cf['detected_bank'] or 'State Bank of India'}</td></tr>
                <tr><td style="padding:6px; color:#94a3b8;">Transaction Date:</td><td style="padding:6px; font-weight:bold;">{cf['transaction_date'] or datetime.now().strftime("%d-%m-%Y")}</td></tr>
                <tr><td style="padding:6px; color:#94a3b8;">Beneficiary VPA:</td><td style="padding:6px; font-weight:bold;">{cf['vpa_beneficiary'] or 'N/A'}</td></tr>
                <tr><td style="padding:6px; color:#94a3b8;">Uploaded Source:</td><td style="padding:6px; font-style:italic;">{cf['uploaded_filename'] or 'User Input / Chat'}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown(f"""
        <div class="timeline-card">
            <h4>⏱️ Recommended Escalation Timeline</h4>
            <ol style="margin-left: 15px; color:#cbd5e1; line-height: 1.8;">
                <li><b>Hours 0 – 2 (Golden Hour):</b> Dial 1930 or submit on cybercrime.gov.in to initiate inter-bank lien marking.</li>
                <li><b>Days 1 – 3 (RBI Zero Liability Window):</b> Serve formal written dispute notice to bank branch manager.</li>
                <li><b>Day 10:</b> Mandatory Shadow Reversal credit by bank under RBI Paragraph 9.</li>
                <li><b>Day 30:</b> If unresolved or rejected, escalate directly to RBI Banking Ombudsman (cms.rbi.org.in).</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# TAB 4: KNOWLEDGE BASE EXPLORER
# ---------------------------------------------------------------------
with tab_kb:
    st.markdown("### 📚 Authoritative Knowledge Base Explorer")
    st.caption("Browse all 122 indexed legal chunks extracted from Indian statutes, RBI circulars, and the 42 files in `kuku data`.")
    
    kb_col1, kb_col2 = st.columns([1, 2])
    with kb_col1:
        kb_categories = list(dict.fromkeys(s.get("category", "General") for s in all_statutes))
        selected_cat = st.selectbox("Filter by Category", options=["All"] + kb_categories, key="tab_kb_filter")
    with kb_col2:
        search_kw = st.text_input("Search in Knowledge Base (e.g. 'SIM swap', 'Shaurya', 'AnyDesk', 'Ombudsman')", key="tab_kb_search")

    filtered = all_statutes if selected_cat == "All" else [s for s in all_statutes if s.get("category") == selected_cat]
    if search_kw:
        filtered = [s for s in filtered if search_kw.lower() in (s.get("act", "") + s.get("summary", "") + s.get("title", "")).lower()]

    st.markdown(f"**Showing {len(filtered)} results:**")
    for statute in filtered[:30]:
        with st.expander(f"📌 {statute['title']} ({statute.get('category')})", expanded=False):
            st.markdown(f"**Act / Reference:** `{statute['act']}` | **Section / Part:** `{statute['section']}`")
            if statute.get("source_file"):
                st.caption(f"📁 Extracted from: `{statute['source_file']}` | Authority: {statute['issuing_authority']}")
            else:
                st.caption(f"Authority: {statute['issuing_authority']} | [Official Link]({statute['source_url']})")
            st.write(statute['summary'])
            if statute.get("practical_application"):
                st.info(f"💡 Practical Application: {statute['practical_application']}")
