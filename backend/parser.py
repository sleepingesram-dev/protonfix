import re
from fingerprints.database import ERROR_PATTERNS
from fingerprints.ranking import rank_fingerprints, get_primary_fingerprint
from fingerprints.dependencies import build_dependency_chain
from fingerprints.metadata import get_fingerprint_metadata
from fingerprints.registry import DEFINITION_MAP
from fingerprints.reasoning import explain_reasoning
from extractors.registry import extract_all_evidence
from evidence import evidence_list_to_dicts
from inference import generate_hypotheses, get_primary_hypothesis

HIGH_CONFIDENCE_PATTERNS = {
    "vk_error_incompatible_driver",
    "vk_error_device_lost",
    "vk_error_out_of_device_memory",
    "wine: could not load kernel32.dll",
    "no space left on device",
    "read-only file system",
    "oom-killer",
}


def calculate_confidence(pattern: str, info: dict) -> int:
    pattern_lower = pattern.lower()

    if pattern_lower in HIGH_CONFIDENCE_PATTERNS:
        return 100

    if "vk_error" in pattern_lower:
        return 95

    if "failed" in pattern_lower or "error" in pattern_lower:
        return 90

    if info.get("severity") == "high":
        return 85

    if len(pattern_lower) >= 10:
        return 75

    return 50


def parse_log(log_text: str) -> dict:
    data = {
        "game": None,
        "appid": None,
        "proton_version": None,
        "dxvk_version": None,
        "vkd3d_version": None,
        "gpu": None,
        "errors": [],
        "fingerprints": [],
    }

    evidence_items = extract_all_evidence(log_text)
    data["evidence"] = evidence_list_to_dicts(evidence_items)
    hypotheses = generate_hypotheses(evidence_items)
    primary_hypothesis = get_primary_hypothesis(hypotheses)

    data["hypotheses"] = {
        node_id: {
            "node_id": hypothesis.node_id,
            "score": hypothesis.score,
            "supporting_evidence_count": len(hypothesis.supporting_evidence),
            "contradictory_evidence_count": len(hypothesis.contradictory_evidence),
            "direct_support_count": hypothesis.direct_support_count,
            "propagated_support_count": hypothesis.propagated_support_count,
        }
        for node_id, hypothesis in hypotheses.items()
    }

    data["primary_hypothesis"] = (
        {
            "node_id": primary_hypothesis.node_id,
            "score": primary_hypothesis.score,
            "supporting_evidence_count": len(primary_hypothesis.supporting_evidence),
            "contradictory_evidence_count": len(primary_hypothesis.contradictory_evidence),
            "direct_support_count": primary_hypothesis.direct_support_count,
            "propagated_support_count": primary_hypothesis.propagated_support_count,
       }
        if primary_hypothesis
        else None
    )

    game_match = re.search(r"Game:\s*(.+)", log_text)
    if game_match:
        data["game"] = game_match.group(1).strip()

    appid_match = re.search(r"AppID:\s*(\d+)", log_text)
    if appid_match:
        data["appid"] = appid_match.group(1)

    proton_match = re.search(r"Proton:\s*(.+)", log_text)
    if proton_match:
        data["proton_version"] = proton_match.group(1).strip()

    dxvk_match = re.search(r"DXVK:\s*(.+)", log_text)
    if dxvk_match:
        data["dxvk_version"] = dxvk_match.group(1).strip()

    vkd3d_match = re.search(r"VKD3D-Proton:\s*(.+)", log_text)
    if vkd3d_match:
        data["vkd3d_version"] = vkd3d_match.group(1).strip()

    gpu_match = re.search(r"GPU:\s*(.+)", log_text)
    if gpu_match:
        data["gpu"] = gpu_match.group(1).strip()

    seen_errors = set()

    for line in log_text.splitlines():
        clean_line = line.strip()
        lower = clean_line.lower()

        is_error = (
            "err:" in lower
            or "vk_error" in lower
            or "failed" in lower
            or "unhandled page fault" in lower
            or "segmentation fault" in lower
            or "core dumped" in lower
            or "permission denied" in lower
            or "no space left" in lower
            or "cannot allocate memory" in lower
        )

        if is_error and clean_line not in seen_errors:
            data["errors"].append(clean_line)
            seen_errors.add(clean_line)

    # Collect best match per fingerprint (highest confidence wins over first match)
    best_match_per_fingerprint: dict[str, tuple[dict, int]] = {}

    for pattern, info in ERROR_PATTERNS.items():
        if pattern.lower() in log_text.lower():
            fingerprint = info["fingerprint"]
            confidence = calculate_confidence(pattern, info)

            existing = best_match_per_fingerprint.get(fingerprint)
            if existing is None or confidence > existing[1]:
                best_match_per_fingerprint[fingerprint] = (info, confidence)

    for fingerprint, (info, confidence) in best_match_per_fingerprint.items():
        fingerprint_info = info.copy()
        fingerprint_info["confidence"] = confidence
        fingerprint_info["metadata"] = get_fingerprint_metadata(fingerprint)
        data["fingerprints"].append(fingerprint_info)

    data["fingerprints"] = rank_fingerprints(data["fingerprints"])

    data["primary_fingerprint"] = get_primary_fingerprint(data["fingerprints"])

    data["dependency_chain"] = build_dependency_chain(
        data["fingerprints"],
        data["primary_fingerprint"],
    )

    data["reasoning"] = explain_reasoning(DEFINITION_MAP,data["dependency_chain"],)

    return data
