from pathlib import Path
from parser import parse_log
from resolver import resolve_known_issues


SAMPLES_DIR = Path("../samples")


def analyze_sample(path: Path) -> dict:
    log_text = path.read_text(errors="ignore")
    parsed = parse_log(log_text)
    known_issue = resolve_known_issues(parsed)

    return {
        "file": str(path),
        "game": parsed.get("game"),
        "primary_fingerprint": (
            parsed.get("primary_fingerprint") or {}
        ).get("fingerprint"),
        "primary_hypothesis": parsed.get("primary_hypothesis"),
        "dependency_chain": parsed.get("dependency_chain", []),
        "fingerprints": [
            item.get("fingerprint")
            for item in parsed.get("fingerprints", [])
        ],
        "evidence_count": len(parsed.get("evidence", [])),
        "evidence": parsed.get("evidence", [])[:5],
        "hypotheses": parsed.get("hypotheses", {}),
        "known_issue": known_issue.get("known_issue_id") if known_issue else None,
    }


def main() -> None:
    log_files = list(SAMPLES_DIR.rglob("*.log")) + list(SAMPLES_DIR.rglob("*.txt"))

    if not log_files:
        print("No sample logs found.")
        return

    print(f"Found {len(log_files)} sample logs.\n")

    for path in sorted(log_files):
        result = analyze_sample(path)

        print("=" * 80)
        print(f"File: {result['file']}")
        print(f"Game: {result['game']}")
        print(f"Primary: {result['primary_fingerprint']}")

        primary_hypothesis = result.get("primary_hypothesis")

        if primary_hypothesis:
            print(
                f"Primary Hypothesis: {primary_hypothesis.get('node_id')} "
                f"score={primary_hypothesis.get('score')}"
            )
        else:
            print("Primary Hypothesis: None")
        print(f"Known Issue: {result['known_issue']}")
        print(f"Chain: {' -> '.join(result['dependency_chain']) or 'None'}")

        print(f"Evidence Count: {result['evidence_count']}")
        print("Evidence Preview:")

        for item in result["evidence"]:
            print(
                f"  - [{item.get('kind', 'unknown').upper()}] "
                f"line {item.get('line_number')}: "
                f"{item.get('extracted_pattern')} "
                f"supports {item.get('supports')}"
            )

        print("Top Hypotheses:")

        top_hypotheses = sorted(
            result["hypotheses"].values(),
            key=lambda item: item.get("score", 0),
            reverse=True,
        )[:5]

        for hypothesis in top_hypotheses:
            print(
                f"  - {hypothesis.get('node_id')} "
                f"score={hypothesis.get('score')} "
                f"support={hypothesis.get('supporting_evidence_count')} "
                f"direct={hypothesis.get('direct_support_count')} "
                f"propagated={hypothesis.get('propagated_support_count')} "
                f"contradict={hypothesis.get('contradictory_evidence_count')}"
            )

        print("Fingerprints:")

        for fingerprint in result["fingerprints"]:
            print(f"  - {fingerprint}")

        print()


if __name__ == "__main__":
    main()
