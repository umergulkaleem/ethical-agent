# tests/test_agent_cli.py
import subprocess
import sys, json

PY = sys.executable

def test_agent_runs_cli():
    cmd = [PY, 'main_agent.py', '--text', 'In 2023, city X had 1,000,000 residents. Women are worse drivers than men.']
    out = subprocess.check_output(cmd, universal_newlines=True, timeout=30)
    data = json.loads(out)
    assert 'results' in data
    # safety and policy keys should exist
    assert 'safety' in data['results'] or 'safety' in data
