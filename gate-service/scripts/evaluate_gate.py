import os
import sys

import requests


API_KEY = os.environ["GATE_API_KEY"]
GATE_URL = os.environ["GATE_URL"]


payload = {
    "service": "gate-service",
    "commit_sha": "abc123",
}

response = requests.post(
    f"{GATE_URL}/gate/evaluate",
    headers={
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=30,
)

response.raise_for_status()

decision = response.json()

print(decision)

if decision["allowed"]:
    sys.exit(0)

sys.exit(1)