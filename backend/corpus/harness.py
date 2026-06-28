#!/usr/bin/env python3
"""
ProtonFix Validation Harness

Runs the deterministic pipeline against a growing corpus of real-world and
synthetic logs, compares results to declared expectations, and reports:

  • Incorrect diagnoses   — wrong primary FP, wrong confidence, bad AI/det split
  • Missing fingerprints  — expected FP not detected; unexpected FP present
  • Pattern overlaps      — shorter pattern always fires with longer one (cross-FP)
  • Uncovered fingerprints — defined in DEFINITION_MAP but never triggered
  • AI fallback opportunities — unmatched error lines in logs that hit the AI path

Usage:
  python corpus/harness.py                    # run all cases, terminal report
  python corpus/harness.py --json             # machine-readable JSON to stdout
  python corpus/harness.py --tag vulkan       # only cases with this tag
  python corpus/harness.py --scaffold FILE    # print a scaffolded case JSON

Case format (JSON files in corpus/cases/):
  {
    "id": "apex_vulkan_missing",
    "description": "...",
    "log_path": "../../samples/apex/apex_failed_launch.log",  // relative to corpus/
    "log": "...",           // OR inline log text (alternative to log_path)
    "tags": ["vulkan", "amd"],
    "expected": {
      "primary_fingerprint": "VULKAN_DRIVER_MISSING",     // omit to skip check
      "fingerprints": {
        "required": ["VULKAN_DRIVER_MISSING"],            // must all be detected
        "forbidden": []                                   // must none be detected
      },
      "confidence": ["medium", "high"],   // acceptable values (omit = any)
      "ai_should_invoke": false,          // false = expect deterministic path
      "fix_steps_contain": ["vulkan"],    // keywords that must appear
      "warnings_contain": []
    }
  }
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── path setup ────────────────────────────────────────────────────────────────
CORPUS_DIR = Path(__file__).parent
BACKEND_DIR = CORPUS_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

from parser import parse_log
from synthesizer import synthesize_diagnosis
from fingerprints.database import ERROR_PATTERNS
from fingerprints.known_issues import KNOWN_ISSUES
from fingerprints.registry import DEFINITION_MAP


# ══════════════════════════════════════════════════════════════════════════════
# Data types
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class CaseResult:
    case_id: str
    description: str
    tags: list[str]
    source_file: str

    actual_primary: Optional[str]
    actual_fingerprints: list[str]
    actual_confidence: Optional[str]
    actual_ai_invoked: bool     # True when synthesize_diagnosis() returned None
    actual_fix_steps: list[str]
    actual_warnings: list[str]

    failures: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.failures) == 0


@dataclass
class PatternOverlap:
    shorter: str
    shorter_fp: str
    longer: str
    longer_fp: str
    kind: str   # "exact_ci" | "substring"


@dataclass
class AIOpportunity:
    case_id: str
    description: str
    unmatched_lines: list[str]   # error-like lines that match no known pattern
    suggestion: str


# ══════════════════════════════════════════════════════════════════════════════
# Case loading
# ══════════════════════════════════════════════════════════════════════════════

def _cases_dir() -> Path:
    return CORPUS_DIR / "cases"


def load_cases(tag_filter: Optional[str] = None) -> list[dict]:
    cases = []
    for f in sorted(_cases_dir().glob("*.json")):
        try:
            case = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"[WARN] Skipping {f.name}: {e}", file=sys.stderr)
            continue
        case["_source_file"] = str(f)
        if tag_filter and tag_filter not in case.get("tags", []):
            continue
        cases.append(case)
    return cases


def load_log_text(case: dict) -> str:
    if "log" in case:
        return case["log"]
    if "log_path" in case:
        path = Path(case["log_path"])
        if not path.is_absolute():
            path = CORPUS_DIR / path
        return path.read_text()
    raise ValueError(f"Case {case.get('id', '?')} has neither 'log' nor 'log_path'")


# ══════════════════════════════════════════════════════════════════════════════
# Validation
# ══════════════════════════════════════════════════════════════════════════════

def run_case(case: dict) -> CaseResult:
    case_id = case.get("id", "unknown")
    expected = case.get("expected", {})

    log_text = load_log_text(case)
    parsed = parse_log(log_text)
    diagnosis = synthesize_diagnosis(parsed)

    actual_primary = (parsed.get("primary_fingerprint") or {}).get("fingerprint")
    actual_fps = [
        f.get("fingerprint")
        for f in parsed.get("fingerprints", [])
        if f.get("fingerprint")
    ]
    actual_confidence = diagnosis.get("confidence") if diagnosis else None
    actual_ai_invoked = diagnosis is None
    actual_fix_steps  = (diagnosis or {}).get("fix_steps", [])
    actual_warnings   = (diagnosis or {}).get("warnings", [])

    failures: list[str] = []
    notices:  list[str] = []

    if "primary_fingerprint" in expected and expected["primary_fingerprint"]:
        exp = expected["primary_fingerprint"]
        if actual_primary != exp:
            failures.append(
                f"primary_fingerprint: expected {exp!r}, got {actual_primary!r}"
            )

    for fp in expected.get("fingerprints", {}).get("required", []):
        if fp not in actual_fps:
            failures.append(f"fingerprint {fp!r} not detected (required)")

    for fp in expected.get("fingerprints", {}).get("forbidden", []):
        if fp in actual_fps:
            failures.append(f"fingerprint {fp!r} detected (forbidden)")

    allowed_conf = expected.get("confidence", [])
    if allowed_conf and actual_confidence not in allowed_conf:
        failures.append(
            f"confidence: expected one of {allowed_conf!r}, got {actual_confidence!r}"
        )

    if "ai_should_invoke" in expected:
        expect_ai = expected["ai_should_invoke"]
        if expect_ai is False and actual_ai_invoked:
            failures.append(
                "AI fallback invoked but expected a deterministic diagnosis "
                "(synthesize_diagnosis() returned None — zero fingerprints detected)"
            )
        elif expect_ai is True and not actual_ai_invoked:
            notices.append(
                "Expected AI fallback but the engine produced a deterministic diagnosis "
                f"({actual_primary}) — this is better than expected, update the case."
            )

    fix_text  = " ".join(actual_fix_steps).lower()
    warn_text = " ".join(actual_warnings).lower()

    for kw in expected.get("fix_steps_contain", []):
        if kw.lower() not in fix_text:
            failures.append(f"fix_steps missing keyword {kw!r}")

    for kw in expected.get("warnings_contain", []):
        if kw.lower() not in warn_text:
            failures.append(f"warnings missing keyword {kw!r}")

    return CaseResult(
        case_id=case_id,
        description=case.get("description", ""),
        tags=case.get("tags", []),
        source_file=case.get("_source_file", ""),
        actual_primary=actual_primary,
        actual_fingerprints=actual_fps,
        actual_confidence=actual_confidence,
        actual_ai_invoked=actual_ai_invoked,
        actual_fix_steps=actual_fix_steps,
        actual_warnings=actual_warnings,
        failures=failures,
        notices=notices,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Pattern overlap analysis
# ══════════════════════════════════════════════════════════════════════════════

def analyze_pattern_overlaps() -> list[PatternOverlap]:
    """
    Returns overlapping pattern pairs where the two patterns target DIFFERENT
    fingerprints.  Two kinds:

    • exact_ci   — the patterns are identical when lowercased (case-insensitive
                   duplicate — both will always fire together)
    • substring  — the shorter pattern is a substring of the longer one; any
                   log that triggers the longer also triggers the shorter
    """
    items = list(ERROR_PATTERNS.items())
    overlaps: list[PatternOverlap] = []
    seen: set[tuple] = set()

    for i, (pa, ia) in enumerate(items):
        fa = ia.get("fingerprint", "")
        for pb, ib in items[i + 1:]:
            fb = ib.get("fingerprint", "")
            if fa == fb:
                continue    # same FP — overlap is intentional redundancy

            la, lb = pa.lower(), pb.lower()

            # exact case-insensitive duplicate
            if la == lb:
                key = (min(pa, pb), max(pa, pb))
                if key not in seen:
                    seen.add(key)
                    overlaps.append(PatternOverlap(pa, fa, pb, fb, "exact_ci"))
                continue

            # substring containment
            if la in lb:
                shorter, sfp, longer, lfp = pa, fa, pb, fb
            elif lb in la:
                shorter, sfp, longer, lfp = pb, fb, pa, fa
            else:
                continue

            key = (shorter, sfp, longer, lfp)
            if key not in seen:
                seen.add(key)
                overlaps.append(PatternOverlap(shorter, sfp, longer, lfp, "substring"))

    # Sort: exact_ci first, then by shorter pattern length (shortest = highest risk)
    overlaps.sort(key=lambda o: (0 if o.kind == "exact_ci" else 1, len(o.shorter)))
    return overlaps


# ══════════════════════════════════════════════════════════════════════════════
# AI fallback opportunity analysis
# ══════════════════════════════════════════════════════════════════════════════

# Lowercase set of all known pattern strings — built once at import time
_KNOWN_PATS_LOWER = frozenset(p.lower() for p in ERROR_PATTERNS)

_ERROR_SIGNALS = re.compile(
    r"\b(err(?:or)?:|failed|failure|crash(?:ed)?|fatal|critical|"
    r"exception|cannot|unable to|not found|no such|denied)\b",
    re.IGNORECASE,
)

# Hard-coded candidates for new rules — things commonly seen in unhandled logs
_RULE_HINTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"denuvo", re.I),            "Add DENUVO_DRM_FAILURE fingerprint (DRM license errors)"),
    (re.compile(r"steamwebhelper.*crash|crash.*steamwebhelper", re.I),
                                             "Add STEAM_WEBHELPER_CRASH fingerprint"),
    (re.compile(r"vcruntime|msvcp\d+\.dll|msvcr\d+\.dll", re.I),
                                             "Add VISUAL_CPP_MISSING fingerprint (MSVC runtime absent)"),
    (re.compile(r"libopenal|openal.*fail", re.I),
                                             "Add OPENAL_MISSING fingerprint (audio backend)"),
    (re.compile(r"mono.*not found|could not load mono", re.I),
                                             "Add MONO_RUNTIME_MISSING fingerprint"),
    (re.compile(r"physx|nvphysx", re.I),    "Add PHYSX_RELATED fingerprint"),
    (re.compile(r"xna framework|monogame.*crash", re.I),
                                             "Add XNA_RELATED fingerprint"),
    (re.compile(r"couldn.t connect to steam|steam.*timeout", re.I),
                                             "Add STEAM_CONNECTION_FAILURE fingerprint"),
    (re.compile(r"\.net.*exception|clr.*failed|dotnet.*crash", re.I),
                                             "Add DOTNET_RUNTIME_FAILURE fingerprint"),
    (re.compile(r"gstreamer.*error|gst_element_", re.I),
                                             "Add GSTREAMER_FAILURE fingerprint (media pipeline)"),
]


def _unmatched_error_lines(log_text: str) -> list[str]:
    """Return lines that look like errors but match no known pattern."""
    unmatched = []
    for line in log_text.splitlines():
        stripped = line.strip()
        if not stripped or not _ERROR_SIGNALS.search(stripped):
            continue
        lower = stripped.lower()
        if not any(p in lower for p in _KNOWN_PATS_LOWER):
            unmatched.append(stripped)
    return unmatched[:8]


def analyze_ai_opportunities(cases: list[dict], results: list[CaseResult]) -> list[AIOpportunity]:
    case_by_id = {c.get("id"): c for c in cases}
    opps = []

    for r in results:
        if not r.actual_ai_invoked:
            continue

        case = case_by_id.get(r.case_id, {})
        try:
            log_text = load_log_text(case)
        except Exception:
            log_text = ""

        unmatched = _unmatched_error_lines(log_text)

        hints = []
        for pattern, hint in _RULE_HINTS:
            if pattern.search(log_text):
                # extract the actual matching line
                for line in log_text.splitlines():
                    if pattern.search(line):
                        hints.append(f"{hint}  (matched: \"{line.strip()[:80]}\")")
                        break

        suggestion = (
            "; ".join(hints) if hints
            else "Review unmatched lines below — recurring patterns suggest a new rule"
        )

        opps.append(AIOpportunity(
            case_id=r.case_id,
            description=r.description,
            unmatched_lines=unmatched,
            suggestion=suggestion,
        ))

    return opps


# ══════════════════════════════════════════════════════════════════════════════
# Coverage
# ══════════════════════════════════════════════════════════════════════════════

def coverage_summary(results: list[CaseResult]) -> tuple[set[str], set[str], set[str], set[str]]:
    """
    Returns:
      (all_defined_fps, triggered_fps, all_known_issues, triggered_ki)
    """
    all_fps = set(DEFINITION_MAP.keys())
    all_ki  = set(KNOWN_ISSUES.keys())
    triggered_fps: set[str] = set()
    triggered_ki:  set[str] = set()

    for r in results:
        triggered_fps.update(r.actual_fingerprints)
        if r.actual_primary and r.actual_primary in all_ki:
            triggered_ki.add(r.actual_primary)

    return all_fps, triggered_fps, all_ki, triggered_ki


# ══════════════════════════════════════════════════════════════════════════════
# Scaffold mode
# ══════════════════════════════════════════════════════════════════════════════

def scaffold_case(log_path: str) -> dict:
    """Generate a starter case JSON from a log file."""
    log_text = Path(log_path).read_text()
    parsed   = parse_log(log_text)
    diag     = synthesize_diagnosis(parsed)

    primary  = (parsed.get("primary_fingerprint") or {}).get("fingerprint")
    fps      = [f.get("fingerprint") for f in parsed.get("fingerprints", []) if f.get("fingerprint")]
    conf     = diag.get("confidence") if diag else None

    stem = Path(log_path).stem
    return {
        "id": stem,
        "description": f"Auto-scaffolded from {Path(log_path).name} — update description",
        "log_path": log_path,
        "tags": [],
        "expected": {
            "primary_fingerprint": primary,
            "fingerprints": {
                "required": fps[:5],
                "forbidden": [],
            },
            "confidence": [conf] if conf else [],
            "ai_should_invoke": diag is None,
            "fix_steps_contain": [],
            "warnings_contain": [],
        },
        "_note": "Scaffolded from current engine output — verify before committing",
    }


# ══════════════════════════════════════════════════════════════════════════════
# Report
# ══════════════════════════════════════════════════════════════════════════════

_W = 72


def _bar(char="─"):
    return char * _W


def _h1(title: str, count: int = -1):
    label = f" {title}" + (f" ({count})" if count >= 0 else "")
    print(_bar())
    print(label)
    print(_bar())


def print_terminal_report(
    results:     list[CaseResult],
    overlaps:    list[PatternOverlap],
    opps:        list[AIOpportunity],
    all_fps:     set[str],
    trig_fps:    set[str],
    all_ki:      set[str],
    trig_ki:     set[str],
):
    passed     = sum(1 for r in results if r.passed)
    failed     = len(results) - passed
    ai_count   = sum(1 for r in results if r.actual_ai_invoked)
    uncov_fps  = all_fps - trig_fps
    uncov_ki   = all_ki  - trig_ki

    exact_ci_count = sum(1 for o in overlaps if o.kind == "exact_ci")
    substr_count   = len(overlaps) - exact_ci_count

    print()
    print("═" * _W)
    print("  ProtonFix Validation Harness")
    print("═" * _W)
    print(f"  Corpus     : {len(results)} cases  |  {passed} passed  |  {failed} failed")
    print(f"  AI fallback: {ai_count} case(s) would invoke AI")
    print(f"  FP coverage: {len(trig_fps)}/{len(all_fps)} fingerprints exercised  "
          f"({len(uncov_fps)} never triggered)")
    print(f"  KI coverage: {len(trig_ki)}/{len(all_ki)} KNOWN_ISSUES exercised  "
          f"({len(uncov_ki)} never served)")
    print(f"  Overlaps   : {exact_ci_count} exact-CI  |  {substr_count} substring")
    print()

    # ── Failures ─────────────────────────────────────────────────────────────
    if failed:
        _h1("FAILURES", failed)
        for r in results:
            if r.passed:
                continue
            print(f"\n  [FAIL] {r.case_id}")
            if r.description:
                print(f"         {r.description}")
            for f in r.failures:
                print(f"         ✗  {f}")
            if r.actual_fingerprints:
                print(f"         Detected : {', '.join(r.actual_fingerprints[:8])}")
            if r.actual_primary:
                print(f"         Primary  : {r.actual_primary}  conf={r.actual_confidence}")
        print()

    # ── Passed ────────────────────────────────────────────────────────────────
    _h1("PASSED", passed)
    for r in results:
        if not r.passed:
            continue
        ai_tag   = " [AI]" if r.actual_ai_invoked else ""
        fp_tag   = f"  →  {r.actual_primary}" if r.actual_primary else ""
        conf_tag = f"  conf={r.actual_confidence}" if r.actual_confidence else ""
        print(f"  [PASS] {r.case_id}{ai_tag}{fp_tag}{conf_tag}")
        for n in r.notices:
            print(f"         ℹ  {n}")
    print()

    # ── AI fallback opportunities ─────────────────────────────────────────────
    if opps:
        _h1("AI FALLBACK OPPORTUNITIES", len(opps))
        print("  Logs that hit the AI path. Unmatched error lines suggest new rules.\n")
        for opp in opps:
            print(f"  {opp.case_id}: {opp.description}")
            print(f"  Suggestion: {opp.suggestion}")
            if opp.unmatched_lines:
                print("  Unmatched error lines:")
                for line in opp.unmatched_lines[:5]:
                    print(f"    >  {line[:88]}")
            print()

    # ── Exact case-insensitive pattern duplicates ─────────────────────────────
    exact_ci = [o for o in overlaps if o.kind == "exact_ci"]
    if exact_ci:
        _h1("EXACT CASE-INSENSITIVE PATTERN DUPLICATES", len(exact_ci))
        print("  Two keys lower to the same string — BOTH always fire together.\n")
        for o in exact_ci:
            print(f"  \"{o.shorter}\"  →  {o.shorter_fp}")
            print(f"  \"{o.longer}\"   →  {o.longer_fp}")
            print(f"  Risk: both FPs will appear in every log that matches either one.")
            print()

    # ── Substring overlaps ────────────────────────────────────────────────────
    substr_overlaps = [o for o in overlaps if o.kind == "substring"]
    if substr_overlaps:
        # Bucket by risk: short patterns (< 8 chars) are noisier
        high   = [o for o in substr_overlaps if len(o.shorter) < 8]
        medium = [o for o in substr_overlaps if 8 <= len(o.shorter) < 15]
        low    = [o for o in substr_overlaps if len(o.shorter) >= 15]

        _h1(f"SUBSTRING PATTERN OVERLAPS ({len(substr_overlaps)})")
        print("  When a log triggers the longer pattern, the shorter fires too.\n")

        if high:
            print(f"  ── HIGH RISK (shorter < 8 chars, {len(high)} pairs) ──")
            for o in high:
                print(f"    \"{o.shorter}\" ({o.shorter_fp})  ⊂  \"{o.longer}\" ({o.longer_fp})")
            print()

        if medium:
            print(f"  ── MEDIUM RISK (8–14 chars, {len(medium)} pairs) ──")
            for o in medium[:10]:
                print(f"    \"{o.shorter}\" ({o.shorter_fp})  ⊂  \"{o.longer}\" ({o.longer_fp})")
            if len(medium) > 10:
                print(f"    ... and {len(medium)-10} more")
            print()

        if low:
            print(f"  ── LOW RISK (≥ 15 chars, {len(low)} pairs — cross-FP is intentional) ──")
            for o in low[:5]:
                print(f"    \"{o.shorter[:50]}\" ({o.shorter_fp})")
                print(f"      ⊂ \"{o.longer[:50]}\" ({o.longer_fp})")
            if len(low) > 5:
                print(f"    ... and {len(low)-5} more")
            print()

    # ── Uncovered fingerprints ────────────────────────────────────────────────
    if uncov_fps:
        _h1("UNCOVERED FINGERPRINTS", len(uncov_fps))
        print("  Defined in DEFINITION_MAP but no corpus case exercises them.\n")
        for fp in sorted(uncov_fps):
            ki_tag = "✓ KNOWN_ISSUES" if fp in KNOWN_ISSUES else "  (no solution)"
            print(f"  {fp:<48}  {ki_tag}")
        print()

    # ── Uncovered KNOWN_ISSUES ────────────────────────────────────────────────
    if uncov_ki:
        _h1("UNCOVERED KNOWN_ISSUES ENTRIES", len(uncov_ki))
        print("  Hand-crafted fix scripts that were never the winning diagnosis.\n")
        for ki in sorted(uncov_ki):
            print(f"  {ki}")
        print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("═" * _W)
    if failed == 0:
        print(f"  ✓ All {len(results)} cases passed.")
    else:
        print(f"  ✗ {failed} case(s) failed — see FAILURES section above.")
    print("═" * _W)
    print()


def build_json_report(
    results:  list[CaseResult],
    overlaps: list[PatternOverlap],
    opps:     list[AIOpportunity],
    all_fps:  set[str],
    trig_fps: set[str],
    all_ki:   set[str],
    trig_ki:  set[str],
) -> dict:
    return {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
            "ai_invoked": sum(1 for r in results if r.actual_ai_invoked),
            "fingerprints_defined": len(all_fps),
            "fingerprints_triggered": len(trig_fps),
            "fingerprints_uncovered": len(all_fps - trig_fps),
            "known_issues_defined": len(all_ki),
            "known_issues_triggered": len(trig_ki),
            "known_issues_uncovered": len(all_ki - trig_ki),
            "overlap_exact_ci": sum(1 for o in overlaps if o.kind == "exact_ci"),
            "overlap_substring": sum(1 for o in overlaps if o.kind == "substring"),
        },
        "failures": [
            {
                "case_id": r.case_id,
                "description": r.description,
                "failures": r.failures,
                "actual_primary": r.actual_primary,
                "actual_fingerprints": r.actual_fingerprints,
                "actual_confidence": r.actual_confidence,
            }
            for r in results if not r.passed
        ],
        "passed": [
            {
                "case_id": r.case_id,
                "actual_primary": r.actual_primary,
                "actual_confidence": r.actual_confidence,
                "ai_invoked": r.actual_ai_invoked,
                "fingerprints": r.actual_fingerprints,
                "notices": r.notices,
            }
            for r in results if r.passed
        ],
        "ai_opportunities": [
            {
                "case_id": o.case_id,
                "description": o.description,
                "unmatched_lines": o.unmatched_lines,
                "suggestion": o.suggestion,
            }
            for o in opps
        ],
        "pattern_overlaps": {
            "exact_ci": [
                {"shorter": o.shorter, "shorter_fp": o.shorter_fp,
                 "longer": o.longer,  "longer_fp": o.longer_fp}
                for o in overlaps if o.kind == "exact_ci"
            ],
            "substring": [
                {"shorter": o.shorter, "shorter_fp": o.shorter_fp,
                 "longer": o.longer,  "longer_fp": o.longer_fp}
                for o in overlaps if o.kind == "substring"
            ],
        },
        "uncovered_fingerprints": sorted(all_fps - trig_fps),
        "uncovered_known_issues": sorted(all_ki - trig_ki),
    }


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    p = argparse.ArgumentParser(
        description="ProtonFix validation harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--json",     action="store_true", help="output JSON instead of terminal report")
    p.add_argument("--tag",      metavar="TAG",       help="only run cases with this tag")
    p.add_argument("--scaffold", metavar="LOG",       help="generate a case JSON from a log file")
    args = p.parse_args()

    if args.scaffold:
        print(json.dumps(scaffold_case(args.scaffold), indent=2))
        return 0

    cases = load_cases(tag_filter=args.tag)
    if not cases:
        print(f"No cases found in {_cases_dir()}", file=sys.stderr)
        return 2

    results: list[CaseResult] = []
    errors: list[str] = []
    for case in cases:
        try:
            results.append(run_case(case))
        except Exception as e:
            cid = case.get("id", "?")
            errors.append(f"{cid}: {e}")
            print(f"[ERROR] {cid}: {e}", file=sys.stderr)

    overlaps             = analyze_pattern_overlaps()
    opps                 = analyze_ai_opportunities(cases, results)
    all_fps, trig_fps, all_ki, trig_ki = coverage_summary(results)

    if args.json:
        report = build_json_report(results, overlaps, opps, all_fps, trig_fps, all_ki, trig_ki)
        report["load_errors"] = errors
        print(json.dumps(report, indent=2))
    else:
        print_terminal_report(results, overlaps, opps, all_fps, trig_fps, all_ki, trig_ki)
        if errors:
            print(f"[{len(errors)} case(s) could not be loaded — see stderr]")

    failed = sum(1 for r in results if not r.passed)
    return 1 if (failed or errors) else 0


if __name__ == "__main__":
    sys.exit(main())
