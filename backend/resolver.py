from fingerprints.known_issues import KNOWN_ISSUES


def resolve_known_issues(parsed: dict) -> dict | None:
    fingerprints = parsed.get("fingerprints", [])

    for item in fingerprints:
        fingerprint = item.get("fingerprint")

        if fingerprint in KNOWN_ISSUES:
            issue = KNOWN_ISSUES[fingerprint]

            return {
                "used_known_issue": True,
                "known_issue_id": fingerprint,
                "summary": issue["summary"],
                "probable_cause": issue["probable_cause"],
                "confidence": issue["confidence"],
                "severity": issue["severity"],
                "detected_errors": parsed.get("errors", []),
                "fix_steps": issue["fix_steps"],
                "recommended_commands": issue["recommended_commands"],
                "extra_info_needed": [],
                "warnings": issue["warnings"],
            }

    return None
