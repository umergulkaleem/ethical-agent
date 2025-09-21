import argparse
import os
import sys
import json
import time
from core.input_handler import normalize_input
from core.utils import split_sentences
from dotenv import load_dotenv
import tempfile
import traceback

try:
    client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key=os.environ["AIML_API_KEY"],
    )
except Exception:
    print("ERROR: Could not initialize API client")
    traceback.print_exc()
    raise


# ✅ Load environment variables from .env if present
load_dotenv()

# ✅ AI/ML API client setup (API key MUST be set as an environment variable)
from openai import OpenAI
client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=os.environ["AIML_API_KEY"],  # read ONLY from environment
)

# ✅ Writable path for Hugging Face Spaces / cross-platform
REPORT_PATH = os.path.join(tempfile.gettempdir(), "last_report.json")
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)  # Ensure directory exists

# --- Compliance Check Wrappers ---
def call_model(prompt: str) -> str:
    """Generic wrapper to call AI/ML API with a prompt"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI compliance checker."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API error: {str(e)}"

def check_safety(text: str):
    return {"safety_report": call_model(f"Check this text for harmful or unsafe content:\n\n{text}")}

def check_bias(text: str):
    return {"bias_report": call_model(f"Check this text for bias or stereotypes:\n\n{text}")}

def check_hallucinations(text: str):
    return {"hallucination_report": call_model(f"Check this text for possible factual inaccuracies or hallucinations:\n\n{text}")}

def check_policies(text: str):
    return {"policy_report": call_model(f"Check this text against ethical and legal compliance policies:\n\n{text}")}

# --- Input Helpers ---
def read_stdin():
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if data and data.strip():
            return data
    return None

def load_input(args):
    piped = read_stdin()
    if piped:
        return normalize_input(piped)
    if args.input_file:
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(args.input_file)
        with open(args.input_file, 'r', encoding='utf-8') as f:
            return normalize_input(f.read())
    if args.text:
        return normalize_input(args.text)
    return {'text': ''}

# --- Core Logic ---
def run_checks(text: str):
    reports = {}
    reports['safety'] = check_safety(text)
    try:
        reports['bias'] = check_bias(text)
    except Exception as e:
        reports['bias'] = {'error': str(e)}
    try:
        reports['hallucination'] = check_hallucinations(text)
    except Exception as e:
        reports['hallucination'] = {'error': str(e)}
    try:
        reports['policy'] = check_policies(text)
    except Exception as e:
        reports['policy'] = {'error': str(e)}
    return reports

def make_agg(results: dict):
    return {
        'agent': 'ethical-compliance-agent',
        'version': '0.3.0',
        'timestamp': int(time.time()),
        'results': results
    }

def save_report(data: dict):
    """Save the report to a writable location."""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)  # Ensure directory exists
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- Entry Point ---
def main():
    parser = argparse.ArgumentParser(description="Ethical Compliance Agent - Coral-ready (AI/ML API-powered)")
    parser.add_argument('--text', type=str, help='Text to check')
    parser.add_argument('--input-file', type=str, help='Path to input file (.txt or .json)')
    parser.add_argument('--mode', choices=['cli', 'server'], default='cli', help='Mode to run')
    args = parser.parse_args()

    # ✅ Server Mode (FastAPI for Hugging Face deployment)
    if args.mode == 'server':
        from fastapi import FastAPI, Request
        import uvicorn

        # Explicitly enable docs & redoc for HF Spaces
        app = FastAPI(
            title="Ethical Compliance Agent",
            description="API for bias, safety, hallucination & policy compliance checks.",
            version="0.3.0",
            docs_url="/docs",     # Swagger UI
            redoc_url="/redoc"    # ReDoc
        )

        @app.get("/")  # Health check endpoint
        async def root():
            return {
                "status": "FastAPI is running",
                "docs": "/docs",
                "check_endpoint": "/check"
            }

        @app.post("/check")
        async def check(req: Request):
            payload = await req.json()
            inp = normalize_input(payload)
            text = inp.get('text', '')
            results = run_checks(text)
            agg = make_agg(results)
            save_report(agg)
            return agg

        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
        return

    # ✅ CLI Mode
    inp = load_input(args)
    text = inp.get('text', '')
    results = run_checks(text)
    agg = make_agg(results)

    print(json.dumps(agg, indent=2))
    save_report(agg)
    sys.exit(0)


if __name__ == '__main__':
    main()
