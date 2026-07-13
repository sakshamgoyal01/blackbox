import os
import sys
import requests

API_KEY = os.environ["GATE_API_KEY"]
GATE_URL = os.environ["GATE_URL"]

payload = {
    "service": os.environ["SERVICE_NAME"],
    "commit_sha": os.environ["COMMIT_SHA"],
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

sys.exit(0 if decision["allowed"] else 1)