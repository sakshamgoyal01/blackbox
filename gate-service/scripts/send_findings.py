import json
import os

import requests


API_KEY = os.environ["GATE_API_KEY"]
GATE_URL = os.environ["GATE_URL"]


def main():

    with open("normalized-findings.json") as f:
        findings = json.load(f)

    payload = {
        "findings": findings,
    }

    response = requests.post(
        f"{GATE_URL}/findings",
        headers={
            "X-API-Key": API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    print(response.status_code)
    print(response.text)

    response.raise_for_status()


if __name__ == "__main__":
    main()
