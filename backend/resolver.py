from synthesizer import synthesize_diagnosis


def resolve_known_issues(parsed: dict) -> dict | None:
    """
    Delegate to synthesize_diagnosis so KNOWN_ISSUES lookups share the same
    evidence-based confidence logic and don't duplicate the resolution path.
    Returns None only when synthesize_diagnosis returns None (zero fingerprints).
    """
    return synthesize_diagnosis(parsed)
