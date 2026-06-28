from evidence import Evidence
from extractors.base import EvidenceExtractor
from extractors.context import ContextEvidenceExtractor
from extractors.pattern import PatternEvidenceExtractor
from fingerprints.database import ERROR_PATTERNS


EXTRACTORS: list[EvidenceExtractor] = [
    PatternEvidenceExtractor(ERROR_PATTERNS),
]

_CONTEXT_EXTRACTOR = ContextEvidenceExtractor()


def extract_all_evidence(log_text: str) -> list[Evidence]:
    evidence_items: list[Evidence] = []

    for extractor in EXTRACTORS:
        evidence_items.extend(extractor.extract(log_text))

    return evidence_items


def extract_context_evidence(metadata: dict) -> list[Evidence]:
    """Convert pre-parsed metadata fields into Evidence objects."""
    return _CONTEXT_EXTRACTOR.extract_from_metadata(metadata)
