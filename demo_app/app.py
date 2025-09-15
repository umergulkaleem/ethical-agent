import sys, os
import streamlit as st
import requests
import json

# --- Make sure project root is in sys.path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now imports will work if needed
from core.input_handler import normalize_input

API_URL = "http://localhost:8000/check"

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
                # Call your running FastAPI backend
                payload = {"text": user_text}
                res = requests.post(API_URL, json=payload)
                if res.status_code == 200:
                    result = res.json()

                    # Show JSON
                    st.subheader("📄 Raw JSON Report")
                    st.json(result)

                    # Nicely formatted results
                    st.subheader("✅ Compliance Breakdown")
                    results = result.get("results", {})
                    for key, val in results.items():
                        st.write(f"### {key.capitalize()}")
                        st.write(val)

                    # Save report for download
                    st.download_button(
                        "Download Report (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name="compliance_report.json",
                        mime="application/json",
                    )
                else:
                    st.error(f"API Error: {res.status_code} {res.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
