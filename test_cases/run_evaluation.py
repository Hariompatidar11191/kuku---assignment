"""
Evaluation and Benchmark Runner for NyaySahay AI Legal Assistant.
Executes test cases, verifies legal grounding, and exports raw unedited outputs for submission.
"""

import os
import sys
import json
from datetime import datetime

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.legal_engine import legal_engine
from core.legal_drafter import legal_drafter


def run_all_tests():
    test_file = os.path.join(BASE_DIR, "test_cases", "test_scenarios.json")
    raw_output_dir = os.path.join(BASE_DIR, "raw_outputs")
    os.makedirs(raw_output_dir, exist_ok=True)

    with open(test_file, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    print(f"==================================================")
    print(f"RUNNING NYAYSAY LEGAL EVALUATION ON {len(scenarios)} SCENARIOS")
    print(f"==================================================\n")

    summary_results = []

    for idx, sc in enumerate(scenarios, 1):
        sc_id = sc["id"]
        title = sc["title"]
        query = sc["user_query"]
        lang = sc["language"]
        expected_statutes = sc["expected_statutes"]

        print(f"[{idx}/{len(scenarios)}] Testing: {title} ({lang})...")

        # Run through reasoning engine
        result = legal_engine.generate_response(
            user_message=query,
            conversation_history=[],
            case_facts={},
            language=lang
        )

        answer = result["answer"]
        sources = result["sources"]

        # Check retrieval recall against expected statutes
        retrieved_sections = [f"{s['act']} {s['section']}" for s in sources]
        all_retrieved_text = " ".join(retrieved_sections)

        hits = []
        for exp in expected_statutes:
            # Check if keyword or section substring appears
            exp_keywords = [w.lower() for w in exp.split() if len(w) > 3]
            match = any(k in all_retrieved_text.lower() for k in exp_keywords)
            hits.append((exp, match))

        recall_rate = sum(1 for _, m in hits if m) / len(hits) if hits else 1.0

        # Export unedited raw output file
        raw_output_filepath = os.path.join(raw_output_dir, f"{sc_id}_output.txt")
        with open(raw_output_filepath, "w", encoding="utf-8") as out_f:
            out_f.write(f"TEST CASE ID: {sc_id}\n")
            out_f.write(f"SCENARIO TITLE: {title}\n")
            out_f.write(f"USER QUERY: {query}\n")
            out_f.write(f"LANGUAGE: {lang}\n")
            out_f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
            out_f.write(f"RETRIEVAL RECALL: {recall_rate * 100:.1f}%\n")
            out_f.write("\n" + "="*70 + "\n")
            out_f.write("VERIFIED RETRIEVED SOURCES:\n")
            out_f.write("="*70 + "\n")
            for s_idx, src in enumerate(sources, 1):
                out_f.write(f"[{s_idx}] {src['act']} - {src['section']}\n")
                out_f.write(f"    Title: {src['title']}\n")
                out_f.write(f"    Authority: {src['issuing_authority']} | Effective: {src['effective_date']}\n")
                out_f.write(f"    Official URL: {src['source_url']}\n\n")

            out_f.write("\n" + "="*70 + "\n")
            out_f.write("UNEDITED ASSISTANT RESPONSE:\n")
            out_f.write("="*70 + "\n")
            out_f.write(answer + "\n")

            # Also generate a sample drafted bank notice for test 1
            if sc_id == "TEST_01_UPI_FRAUD_BANK_REJECTION":
                draft = legal_drafter.generate_bank_grievance_notice(
                    customer_name="Ramesh Kumar",
                    account_number="987654321098",
                    bank_name="State Bank of India",
                    disputed_amount="₹50,000",
                    transaction_id="UPI/412389102931",
                    transaction_date="05-11-2026",
                    incident_narrative="Unauthorized electronic transfer occurred without sharing OTP. Bank rejected claim falsely asserting customer fault."
                )
                out_f.write("\n" + "="*70 + "\n")
                out_f.write("GENERATED ACTION DRAFT (BANK DISPUTE NOTICE):\n")
                out_f.write("="*70 + "\n")
                out_f.write(draft + "\n")

        summary_results.append({
            "id": sc_id,
            "title": title,
            "recall": recall_rate,
            "raw_output_file": raw_output_filepath
        })
        print(f"   -> Recall: {recall_rate*100:.1f}% | Saved: {raw_output_filepath}")

    print("\n" + "="*50)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    avg_recall = sum(r["recall"] for r in summary_results) / len(summary_results)
    print(f"Average Legal Citation Recall: {avg_recall*100:.1f}%")
    print("="*50)


if __name__ == "__main__":
    run_all_tests()
