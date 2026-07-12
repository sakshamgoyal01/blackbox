from app.normalize.adapters.gitleaks import GitleaksAdapter
from app.normalize.adapters.semgrep import SemgrepAdapter
from app.normalize.adapters.syft import SyftAdapter
from app.normalize.adapters.trivy import TrivyAdapter

REGISTRY = {
    "trivy": TrivyAdapter(),
    "semgrep": SemgrepAdapter(),
    "gitleaks": GitleaksAdapter(),
    "syft": SyftAdapter(),
}


def get_adapter(name: str):
    adapter = REGISTRY.get(name)

    if adapter is None:
        raise ValueError(f"Unsupported scanner: {name}")

    return adapter