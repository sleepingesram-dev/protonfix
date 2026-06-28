from fingerprints.known_issues import KNOWN_ISSUES
from fingerprints.metadata import get_fingerprint_metadata


def _score_to_confidence(score: int) -> str:
    if score >= 140:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def _fingerprint_confidence_to_label(raw: int) -> str:
    if raw >= 90:
        return "high"
    if raw >= 60:
        return "medium"
    return "low"


def synthesize_diagnosis(parsed: dict) -> dict | None:
    """
    Build a deterministic diagnosis from parsed fingerprint and hypothesis data.

    Flow:
    1. KNOWN_ISSUES entry for the primary fingerprint — hand-crafted, highest quality.
    2. Auto-synthesis from the fingerprint's explanation, known_fix, and safe_commands.
    3. Returns None only when zero fingerprints were detected, triggering the AI fallback.

    Confidence is derived from the hypothesis score produced by inference.py, not from
    fixed strings baked into KNOWN_ISSUES entries.
    """
    fingerprints = parsed.get("fingerprints", [])
    if not fingerprints:
        return None

    primary = parsed.get("primary_fingerprint")
    if not primary:
        return None

    fingerprint_id = primary.get("fingerprint")
    hypotheses = parsed.get("hypotheses", {})

    # Get the hypothesis for the primary fingerprint specifically
    hyp = hypotheses.get(fingerprint_id)
    if hyp:
        confidence = _score_to_confidence(hyp.get("score", 0))
    else:
        confidence = _fingerprint_confidence_to_label(
            int(primary.get("confidence", 50) or 50)
        )

    # --- Path 1: hand-crafted KNOWN_ISSUES entry ---
    if fingerprint_id in KNOWN_ISSUES:
        issue = KNOWN_ISSUES[fingerprint_id]
        return {
            "used_known_issue": True,
            "known_issue_id": fingerprint_id,
            "summary": issue["summary"],
            "probable_cause": issue["probable_cause"],
            "confidence": confidence,
            "severity": issue["severity"],
            "detected_errors": parsed.get("errors", []),
            "fix_steps": issue["fix_steps"],
            "recommended_commands": issue["recommended_commands"],
            "extra_info_needed": [],
            "warnings": issue.get("warnings", []),
        }

    # --- Path 2: auto-synthesize from fingerprint metadata ---
    metadata = get_fingerprint_metadata(fingerprint_id)
    fix_steps = primary.get("known_fix") or []
    safe_commands = primary.get("safe_commands") or []
    explanation = primary.get("explanation") or metadata.get(
        "short_description", f"{fingerprint_id} detected."
    )

    secondary_ids = [
        f.get("fingerprint")
        for f in fingerprints[1:4]
        if f.get("fingerprint") and f.get("fingerprint") != fingerprint_id
    ]

    short_desc = metadata.get("short_description", f"{fingerprint_id} detected.")
    if secondary_ids:
        summary = (
            f"{short_desc} Related issues also detected: {', '.join(secondary_ids)}."
        )
    else:
        summary = short_desc

    if not fix_steps:
        fix_steps = [
            "Review the log for earlier errors that may explain this issue.",
            "Try a different Proton version.",
            "Verify game files in Steam.",
            "Disable overlays and custom launch options while testing.",
        ]

    return {
        "used_known_issue": False,
        "known_issue_id": None,
        "summary": summary,
        "probable_cause": explanation,
        "confidence": confidence,
        "severity": primary.get("severity", "medium"),
        "detected_errors": parsed.get("errors", []),
        "fix_steps": fix_steps,
        "recommended_commands": safe_commands,
        "extra_info_needed": [],
        "warnings": [],
    }
