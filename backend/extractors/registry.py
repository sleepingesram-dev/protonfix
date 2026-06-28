from evidence import Evidence
from extractors.base import EvidenceExtractor
from extractors.pattern import PatternEvidenceExtractor
from fingerprints.database import ERROR_PATTERNS


EXTRACTORS: list[EvidenceExtractor] = [
    PatternEvidenceExtractor(ERROR_PATTERNS),
]


def extract_all_evidence(log_text: str) -> list[Evidence]:
    evidence_items: list[Evidence] = []

    for extractor in EXTRACTORS:
        evidence_items.extend(extractor.extract(log_text))

    return evidence_items
