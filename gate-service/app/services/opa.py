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
    )

    print("\n================ OPA QUERY ================")
    print(query)

    print("\n================ STDOUT ===================")
    print(result.stdout)

    print("\n================ STDERR ===================")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    output = json.loads(result.stdout)

    if "errors" in output:
        raise RuntimeError(
            json.dumps(output["errors"], indent=2)
        )

    if "result" not in output:
        return False if query.endswith(".allow") else []

    expressions = output["result"][0]["expressions"]

    if not expressions:
        return None

    return expressions[0].get("value")


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

    violations = (
        _opa_eval(
            "data.blackbox.violations",
            input_file,
        )
        or []
    )

    return allow, violations