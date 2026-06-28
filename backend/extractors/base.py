from abc import ABC, abstractmethod
from evidence import Evidence


class EvidenceExtractor(ABC):
    source: str = "unknown"

    @abstractmethod
    def extract(self, log_text: str) -> list[Evidence]:
        pass
