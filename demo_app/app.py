import sys, os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env if present
load_dotenv()

import streamlit as st
import json

# --- Make sure project root is in sys.path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now imports will work if needed
from core.input_handler import normalize_input
from main_agent import run_checks, make_agg # Import run_checks and make_agg

st.set_page_config(page_title="Ethical Compliance Agent", layout="wide")
st.title("🛡️ Ethical Compliance Agent")
st.write("Paste text below to check for **bias, safety, hallucinations, and policy compliance**.")

# Input box
user_text = st.text_area("Enter text to analyze:", height=200)

if st.button("Run Compliance Check"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        with st.spinner("Running compliance checks..."):
            try:
                # Directly call the compliance check functions
                results = run_checks(user_text)
                result = make_agg(results)

                # Show JSON
                st.subheader("📄 Raw JSON Report")
                st.json(result)

                # Nicely formatted results
                st.subheader("✅ Compliance Breakdown")
                results_breakdown = result.get("results", {})
                for key, val in results_breakdown.items():
                    st.write(f"### {key.capitalize()}")
                    st.write(val)

                # Save report for download
                st.download_button(
                    "Download Report (JSON)",
                    data=json.dumps(result, indent=2),
                    file_name="compliance_report.json",
                    mime="application/json",
                )
            except Exception as e:
                st.error(f"An error occurred during compliance checks: {e}")
