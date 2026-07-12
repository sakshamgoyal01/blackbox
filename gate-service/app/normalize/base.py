from abc import ABC
from abc import abstractmethod

from app.contracts.finding import CanonicalFinding


class BaseAdapter(ABC):

    @abstractmethod
    def normalize(
        self,
        raw_json: dict,
        service: str,
        commit_sha: str,
        environment: str,
    ) -> list[CanonicalFinding]:
        """
        Convert scanner output into CanonicalFinding objects.
        """
        raise NotImplementedError