from dataclasses import dataclass, field
from typing import Any
from enum import Enum

class EvidenceKind(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    CONTEXT = "context"
    CONFIGURATION = "configuration"
    VERSION = "version"
    ENVIRONMENT = "environment"
    HARDWARE = "hardware"
    SUCCESS = "success"


class EvidenceSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass(frozen=True)
class Evidence:
    id: str
    line_number: int | None
    source: str

    raw_text: str
    extracted_pattern: str

    kind: EvidenceKind
    severity: EvidenceSeverity
    confidence: int

    supports: list[str] = field(default_factory=list)
    contradicts: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_line(line: str) -> str:
    return line.strip()


def build_evidence_id(pattern: str, line_number: int | None) -> str:
    safe_pattern = (
        pattern.lower()
        .replace(" ", "_")
        .replace(":", "")
        .replace("/", "_")
        .replace("-", "_")
    )

    if line_number is None:
        return f"evidence_{safe_pattern}"

    return f"evidence_{safe_pattern}_line_{line_number}"



def evidence_to_dict(evidence: Evidence) -> dict[str, Any]:
    return {
        "id": evidence.id,
        "line_number": evidence.line_number,
        "source": evidence.source,
        "raw_text": evidence.raw_text,
        "extracted_pattern": evidence.extracted_pattern,
        "kind": evidence.kind.value,
        "severity": evidence.severity.value,
        "confidence": evidence.confidence,
        "supports": evidence.supports,
        "contradicts": evidence.contradicts,
        "metadata": evidence.metadata,
    }


def evidence_list_to_dicts(evidence_items: list[Evidence]) -> list[dict[str, Any]]:
    return [evidence_to_dict(item) for item in evidence_items]
