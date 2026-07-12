import json
import subprocess
import tempfile


def _opa_eval(query: str, input_file: str):
    result = subprocess.run(
        [
            "opa",
            "eval",
            "-f",
            "json",
            "-d",
            "/app/policy/gate.rego",
            "-i",
            input_file,
            query,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = json.loads(result.stdout)

    return output["result"][0]["expressions"][0]["value"]


def evaluate_policy(
    tier: str,
    findings: list[dict],
):

    payload = {
        "tier": tier,
        "findings": findings,
    }

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
    ) as f:
        json.dump(payload, f)
        input_file = f.name

    allow = _opa_eval(
        "data.blackbox.allow",
        input_file,
    )

    violations = _opa_eval(
        "data.blackbox.violations",
        input_file,
    )

    return allow, violations