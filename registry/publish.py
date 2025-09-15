# registry/publish.py
import json
import yaml
from pathlib import Path

REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "author",
    "inputs",
    "outputs",
    "runtime",
]

def validate_agent_yaml(yaml_path="registry/agent.yaml"):
    """Load and validate agent.yaml structure."""
    p = Path(yaml_path)
    if not p.exists():
        print("❌ agent.yaml missing")
        return None, False

    try:
        spec = yaml.safe_load(p.read_text())
    except Exception as e:
        print(f"❌ Failed to parse YAML: {e}")
        return None, False

    print("🔍 Validating agent.yaml...")
    ok = True
    for field in REQUIRED_FIELDS:
        if field not in spec:
            print(f"❌ Missing required field: {field}")
            ok = False
    if ok:
        print("✅ agent.yaml looks valid")
    return spec, ok

def simulate_publish(yaml_path="registry/agent.yaml"):
    spec, valid = validate_agent_yaml(yaml_path)
    if not valid:
        print("⚠️ Publish aborted due to validation errors.")
        return

    print("\n📦 Simulating publish to Coral Registry...")
    manifest = {
        "name": spec.get("name"),
        "version": spec.get("version"),
        "published": True,
    }
    out_path = Path("registry/publish_manifest.json")
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"✅ Wrote {out_path}")

if __name__ == "__main__":
    simulate_publish()
