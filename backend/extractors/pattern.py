from evidence import (
    Evidence,
    EvidenceKind,
    EvidenceSeverity,
    build_evidence_id,
    normalize_line,
)

from extractors.base import EvidenceExtractor

def classify_evidence_kind(pattern: str, info: dict) -> EvidenceKind:
    pattern_lower = pattern.lower()
    category = str(info.get("category", "")).lower()
    severity = str(info.get("severity", "")).lower()

    context_patterns = [
        "ge-proton",
        "proton: experimental",
        "steam linux runtime",
        "steam-runtime",
        "pressure-vessel",
        "dxvk",
        "vkd3d",
        "gamescope",
        "gamemode",
        "mangohud",
    ]

    error_words = [
        "error",
        "failed",
        "failure",
        "crash",
        "fault",
        "segmentation",
        "core dumped",
        "permission denied",
        "no space left",
        "read-only",
        "cannot allocate",
        "device lost",
    ]

    if any(word in pattern_lower for word in error_words):
        return EvidenceKind.ERROR

    if severity == "high":
        return EvidenceKind.ERROR

    if any(word in pattern_lower for word in context_patterns):
        return EvidenceKind.CONTEXT

    if category in {"proton version", "steam runtime"}:
        return EvidenceKind.VERSION

    if category in {"gamemode", "mangohud", "performance overlay"}:
        return EvidenceKind.CONFIGURATION

    return EvidenceKind.WARNING

def normalize_severity(value: str) -> EvidenceSeverity:
    value = value.lower()

    if value == "critical":
        return EvidenceSeverity.CRITICAL

    if value == "high":
        return EvidenceSeverity.HIGH

    if value == "medium":
        return EvidenceSeverity.MEDIUM

    if value == "low":
        return EvidenceSeverity.LOW

    return EvidenceSeverity.INFO

class PatternEvidenceExtractor(EvidenceExtractor):
    source = "proton_log"

    def __init__(self, error_patterns: dict[str, dict]):
        self.error_patterns = error_patterns

    def extract(self, log_text: str) -> list[Evidence]:
        evidence_items: list[Evidence] = []
        seen: set[str] = set()

        for line_number, line in enumerate(log_text.splitlines(), start=1):
            clean_line = normalize_line(line)
            lower_line = clean_line.lower()

            if not clean_line:
                continue

            for pattern, info in self.error_patterns.items():
                if pattern.lower() not in lower_line:
                    continue

                fingerprint = info.get("fingerprint")
                evidence_id = build_evidence_id(pattern, line_number)

                if evidence_id in seen:
                    continue

                evidence_items.append(
                    Evidence(
                        id=evidence_id,
                        line_number=line_number,
                        source=self.source,
                        raw_text=clean_line,
                        extracted_pattern=pattern,
                        kind=classify_evidence_kind(pattern, info),
                        severity=normalize_severity(str(info.get("severity", "low"))),
                        confidence=100,
                        supports=[fingerprint] if fingerprint else [],
                        contradicts=[],
                        metadata={
                            "fingerprint": fingerprint,
                            "category": info.get("category"),
                        },
                    )
                )

                seen.add(evidence_id)

        return evidence_items
