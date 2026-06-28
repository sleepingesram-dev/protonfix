import re
from fingerprints.database import ERROR_PATTERNS
from fingerprints.ranking import rank_fingerprints, get_primary_fingerprint
from fingerprints.dependencies import build_dependency_chain
from fingerprints.metadata import get_fingerprint_metadata
from fingerprints.registry import DEFINITION_MAP
from fingerprints.reasoning import explain_reasoning
from extractors.registry import extract_all_evidence, extract_context_evidence
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

# Fingerprint sets used for context-aware confidence adjustments
_CRASH_FPS = {"WINE_CRASH", "NTDLL_RELATED_CRASH", "SEGFAULT", "CORE_DUMPED"}
_VULKAN_FPS = {
    "VULKAN_DRIVER_MISSING", "VULKAN_INIT_FAILURE", "VK_ERROR_DEVICE_LOST",
    "VK_ERROR_OUT_OF_DEVICE_MEMORY", "VK_ERROR_EXTENSION_NOT_PRESENT", "DXVK_ADAPTER_FAILURE",
}
_GAMESCOPE_FPS = {
    "GAMESCOPE_FAILURE", "GAMESCOPE_VULKAN_INIT_FAILURE",
    "GAMESCOPE_SWAPCHAIN_FAILURE", "GAMESCOPE_OUTPUT_FAILURE",
}
_AC_FPS = {"EAC_FAILURE", "BATTLEYE_FAILURE"}


def calculate_confidence(pattern: str, info: dict, context: dict | None = None) -> int:
    """
    Return a 0–100 confidence integer for a pattern match.

    `context` (the partially-populated parse_log data dict) enables
    adjustments based on parsed metadata: non-zero exit code boosts
    crash/Vulkan fingerprints; clean exit reduces them; Wayland session
    boosts Gamescope fingerprints; exit code 3 boosts anti-cheat.
    """
    pattern_lower = pattern.lower()

    if pattern_lower in HIGH_CONFIDENCE_PATTERNS:
        base = 100
    elif "vk_error" in pattern_lower:
        base = 95
    elif "failed" in pattern_lower or "error" in pattern_lower:
        base = 90
    elif info.get("severity") == "high":
        base = 85
    elif len(pattern_lower) >= 10:
        base = 75
    else:
        base = 50

    if not context:
        return base

    fingerprint = info.get("fingerprint", "")
    exit_code = context.get("exit_code")
    display_server = context.get("display_server")

    if exit_code is not None:
        if exit_code == 0:
            # Clean exit — crash and Vulkan fingerprints were probably non-fatal warnings
            if fingerprint in _CRASH_FPS | _VULKAN_FPS:
                base = max(0, base - 25)
        else:
            # Non-zero exit confirms something went wrong
            if fingerprint in _CRASH_FPS | _VULKAN_FPS:
                base = min(100, base + 10)
            # Exit code 3 specifically indicates anti-cheat rejection on Linux
            if exit_code == 3 and fingerprint in _AC_FPS:
                base = min(100, base + 15)

    # Wayland session corroborates Gamescope-related fingerprints
    if display_server == "wayland" and fingerprint in _GAMESCOPE_FPS:
        base = min(100, base + 10)

    return base


def _extract_metadata(log_text: str, data: dict) -> None:
    """
    Phase 1: extract all structured header and metadata fields from the raw log.
    Must run BEFORE evidence extraction so context evidence can use these values.
    """
    # --- existing header fields ---

    game_match = re.search(r"^Game:\s*(.+)", log_text, re.MULTILINE)
    if game_match:
        data["game"] = game_match.group(1).strip()

    appid_match = re.search(r"AppID:\s*(\d+)", log_text)
    if appid_match:
        data["appid"] = appid_match.group(1)

    # Exclude "Proton: Upgrading/Creating prefix ..." lines — not a version string
    proton_match = re.search(
        r"^Proton:\s+(?!Upgrading|Creating|Downgrading)(.+)", log_text, re.MULTILINE
    )
    if proton_match:
        data["proton_version"] = proton_match.group(1).strip()

    dxvk_match = re.search(r"DXVK:\s*v?(.+)", log_text)
    if dxvk_match:
        data["dxvk_version"] = dxvk_match.group(1).strip()

    vkd3d_match = re.search(r"VKD3D-Proton:\s*v?(.+)", log_text)
    if vkd3d_match:
        data["vkd3d_version"] = vkd3d_match.group(1).strip()

    gpu_match = re.search(r"^GPU:\s*(.+)", log_text, re.MULTILINE)
    if gpu_match:
        data["gpu"] = gpu_match.group(1).strip()

    # --- new fields ---

    # exit_code — hex wins over decimal when both match (hex is more specific)
    exit_hex = re.search(
        r"Game exited with (?:status|code)\s+(0x[0-9A-Fa-f]+)", log_text, re.IGNORECASE
    )
    exit_decimal = re.search(
        r"Game exited with (?:status|code)\s+(\d+)", log_text, re.IGNORECASE
    )
    if exit_hex:
        data["exit_code"] = int(exit_hex.group(1), 16)
    elif exit_decimal:
        data["exit_code"] = int(exit_decimal.group(1))

    # launch_options — from Steam's "Game process removed" line
    launch_match = re.search(
        r'Game process removed:[^"]*"([^"]+)",\s*ProcID', log_text
    )
    if launch_match:
        data["launch_options"] = launch_match.group(1).strip()

    # sync_method
    if re.search(r"\bfsync:\s+up and running", log_text, re.IGNORECASE):
        data["sync_method"] = "fsync"
    elif re.search(r"\besync:\s+up and running", log_text, re.IGNORECASE):
        data["sync_method"] = "esync"

    # session_type + display_server (derived)
    session_match = re.search(r"^Session:\s*(.+)", log_text, re.MULTILINE)
    if session_match:
        session_val = session_match.group(1).strip()
        data["session_type"] = session_val
        data["display_server"] = "wayland" if "wayland" in session_val.lower() else "x11"

    # kernel_version — header line takes precedence over journal "Linux version" line
    kernel_match = re.search(r"^Kernel:\s*(.+)", log_text, re.MULTILINE) or re.search(
        r"Linux version\s+(\S+)", log_text
    )
    if kernel_match:
        data["kernel_version"] = kernel_match.group(1).strip()

    # driver_version — explicit header only
    driver_match = re.search(r"^Driver:\s*(.+)", log_text, re.MULTILINE)
    if driver_match:
        data["driver_version"] = driver_match.group(1).strip()

    # vulkan_driver_version — from DXVK adapter info line
    # e.g. "info:    [0] AMD Radeon RX 7800 XT (RADV NAVI32) : Vulkan 1.3 [24.1.0.0]"
    vk_adapter_match = re.search(
        r"info:\s+\[\d+\]\s+.+?:\s+Vulkan\s+[\d.]+\s+\[([\d.]+)\]", log_text
    )
    if vk_adapter_match:
        data["vulkan_driver_version"] = vk_adapter_match.group(1).strip()

    # prefix_action
    prefix_upgrade = re.search(
        r"Proton:\s+Upgrading prefix from\s+(\S+)\s+to\s+", log_text, re.IGNORECASE
    )
    prefix_create = re.search(r"Proton:\s+Creating prefix", log_text, re.IGNORECASE)
    if prefix_upgrade:
        data["prefix_action"] = "upgraded"
        prev = prefix_upgrade.group(1)
        data["prefix_upgrade_from"] = None if prev.lower() == "none" else prev
    elif prefix_create:
        data["prefix_action"] = "created"

    # game_exe — from DXVK info block (ends in .exe to distinguish from game name)
    game_exe_match = re.search(r"info:\s+Game:\s*(\S+\.exe)", log_text, re.IGNORECASE)
    if game_exe_match:
        data["game_exe"] = game_exe_match.group(1).strip()

    # gamescope_version
    gamescope_ver_match = re.search(
        r"gamescope version\s+([\d.]+)", log_text, re.IGNORECASE
    )
    if gamescope_ver_match:
        data["gamescope_version"] = gamescope_ver_match.group(1).strip()

    # dx_level — from DXVK or VKD3D info line
    dx_match = re.search(
        r"(?:info:|vkd3d:)\s+(D3D(?:11|12)?_FEATURE_LEVEL_[\w_]+)", log_text
    )
    if dx_match:
        data["dx_level"] = dx_match.group(1).strip()

    # cpu
    cpu_match = re.search(r"^CPU:\s*(.+)", log_text, re.MULTILINE)
    if cpu_match:
        data["cpu"] = cpu_match.group(1).strip()


def parse_log(log_text: str) -> dict:
    data = {
        # existing fields
        "game": None,
        "appid": None,
        "proton_version": None,
        "dxvk_version": None,
        "vkd3d_version": None,
        "gpu": None,
        "errors": [],
        "fingerprints": [],
        # new fields (all None by default — backward-compatible)
        "exit_code": None,
        "launch_options": None,
        "sync_method": None,
        "session_type": None,
        "display_server": None,
        "kernel_version": None,
        "driver_version": None,
        "vulkan_driver_version": None,
        "prefix_action": None,
        "prefix_upgrade_from": None,
        "game_exe": None,
        "gamescope_version": None,
        "dx_level": None,
        "cpu": None,
    }

    # Phase 1: extract all metadata so context evidence and confidence scoring
    # can use it immediately in Phase 2.
    _extract_metadata(log_text, data)

    # Phase 2: run pattern evidence extraction, then add context evidence derived
    # from the just-parsed metadata fields.
    pattern_evidence = extract_all_evidence(log_text)
    context_evidence = extract_context_evidence(data)
    all_evidence = pattern_evidence + context_evidence

    data["evidence"] = evidence_list_to_dicts(all_evidence)

    # Phase 3: inference — hypothesis scoring now benefits from context evidence.
    hypotheses = generate_hypotheses(all_evidence)
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

    # Phase 4: collect error lines
    seen_errors: set[str] = set()
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

    # Phase 5: fingerprint matching with context-aware confidence
    best_match_per_fingerprint: dict[str, tuple[dict, int]] = {}
    for pattern, info in ERROR_PATTERNS.items():
        if pattern.lower() in log_text.lower():
            fingerprint = info["fingerprint"]
            confidence = calculate_confidence(pattern, info, context=data)

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
    data["reasoning"] = explain_reasoning(DEFINITION_MAP, data["dependency_chain"])

    return data
