from evidence import Evidence, EvidenceKind, EvidenceSeverity


KIND_WEIGHTS = {
    EvidenceKind.ERROR: 100,
    EvidenceKind.WARNING: 40,
    EvidenceKind.CONTEXT: 10,
    EvidenceKind.CONFIGURATION: 20,
    EvidenceKind.VERSION: 15,
    EvidenceKind.ENVIRONMENT: 25,
    EvidenceKind.HARDWARE: 35,
    EvidenceKind.SUCCESS: -20,
}


SEVERITY_WEIGHTS = {
    EvidenceSeverity.INFO: 5,
    EvidenceSeverity.LOW: 15,
    EvidenceSeverity.MEDIUM: 35,
    EvidenceSeverity.HIGH: 70,
    EvidenceSeverity.CRITICAL: 100,
}


def evidence_weight(evidence: Evidence) -> int:
    return (
        KIND_WEIGHTS[evidence.kind]
        + SEVERITY_WEIGHTS[evidence.severity]
    )
