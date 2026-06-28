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
        # --- existing fields (backward-compatible) ---
        "game": None,
        "appid": None,
        "proton_version": None,
        "dxvk_version": None,
        "vkd3d_version": None,
        "gpu": None,
        "errors": [],
        "fingerprints": [],
        # --- new fields ---
        "exit_code": None,          # int or hex str; non-zero = crash/rejection
        "launch_options": None,     # full launch string from Steam log
        "sync_method": None,        # "fsync" | "esync" | None
        "session_type": None,       # "KDE Wayland", "GNOME X11", etc.
        "display_server": None,     # derived: "wayland" | "x11"
        "kernel_version": None,     # "7.0.10-cachyos"
        "driver_version": None,     # from Driver: header
        "vulkan_driver_version": None,  # from DXVK adapter info line
        "prefix_action": None,      # "created" | "upgraded"
        "prefix_upgrade_from": None,# previous Proton version when upgrading
        "game_exe": None,           # "r5apex.exe" from DXVK info block
        "gamescope_version": None,  # "3.16.23"
        "dx_level": None,           # "D3D11_FEATURE_LEVEL_12_1" etc.
        "cpu": None,                # "AMD Ryzen 9 7950X"
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

    # ---- existing header fields (backward-compatible) ----

    game_match = re.search(r"^Game:\s*(.+)", log_text, re.MULTILINE)
    if game_match:
        data["game"] = game_match.group(1).strip()

    appid_match = re.search(r"AppID:\s*(\d+)", log_text)
    if appid_match:
        data["appid"] = appid_match.group(1)

    # Exclude "Proton: Upgrading/Creating prefix ..." lines — those aren't version strings
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

    # ---- new fields ----

    # exit_code: decimal ("Game exited with status 1") or hex ("exited with code 0xC0000005")
    exit_decimal = re.search(
        r"Game exited with (?:status|code)\s+(\d+)", log_text, re.IGNORECASE
    )
    exit_hex = re.search(
        r"Game exited with (?:status|code)\s+(0x[0-9A-Fa-f]+)", log_text, re.IGNORECASE
    )
    if exit_hex:
        data["exit_code"] = int(exit_hex.group(1), 16)
    elif exit_decimal:
        data["exit_code"] = int(exit_decimal.group(1))

    # launch_options: extracted from Steam's "Game process removed" line
    launch_match = re.search(
        r'Game process removed:[^"]*"([^"]+)",\s*ProcID', log_text
    )
    if launch_match:
        data["launch_options"] = launch_match.group(1).strip()

    # sync_method: fsync or esync
    if re.search(r"\bfsync:\s+up and running", log_text, re.IGNORECASE):
        data["sync_method"] = "fsync"
    elif re.search(r"\besync:\s+up and running", log_text, re.IGNORECASE):
        data["sync_method"] = "esync"

    # session_type + display_server
    session_match = re.search(r"^Session:\s*(.+)", log_text, re.MULTILINE)
    if session_match:
        session_val = session_match.group(1).strip()
        data["session_type"] = session_val
        data["display_server"] = (
            "wayland" if "wayland" in session_val.lower() else "x11"
        )

    # kernel_version
    kernel_match = re.search(
        r"^Kernel:\s*(.+)", log_text, re.MULTILINE
    ) or re.search(
        r"Linux version\s+(\S+)", log_text
    )
    if kernel_match:
        data["kernel_version"] = kernel_match.group(1).strip()

    # driver_version: from explicit "Driver:" header
    driver_match = re.search(r"^Driver:\s*(.+)", log_text, re.MULTILINE)
    if driver_match:
        data["driver_version"] = driver_match.group(1).strip()

    # vulkan_driver_version: from DXVK adapter info line
    # Matches: "info:    [0] GPU NAME (DRIVER) : Vulkan 1.3 [24.1.0.0]"
    vk_adapter_match = re.search(
        r"info:\s+\[(?:0|selected)\]\s+.+?:\s+Vulkan\s+[\d.]+\s+\[([\d.]+)\]",
        log_text,
    )
    if not vk_adapter_match:
        # "info:  Using adapter: ..." line does not carry version; fall back to any adapter line
        vk_adapter_match = re.search(
            r"info:\s+\[\d+\]\s+.+?:\s+Vulkan\s+[\d.]+\s+\[([\d.]+)\]",
            log_text,
        )
    if vk_adapter_match:
        data["vulkan_driver_version"] = vk_adapter_match.group(1).strip()

    # prefix_action: created or upgraded
    prefix_upgrade = re.search(
        r"Proton:\s+Upgrading prefix from\s+(\S+)\s+to\s+", log_text, re.IGNORECASE
    )
    prefix_create = re.search(
        r"Proton:\s+Creating prefix", log_text, re.IGNORECASE
    )
    if prefix_upgrade:
        data["prefix_action"] = "upgraded"
        prev = prefix_upgrade.group(1)
        data["prefix_upgrade_from"] = None if prev.lower() == "none" else prev
    elif prefix_create:
        data["prefix_action"] = "created"

    # game_exe: from DXVK info block ("info:  Game: r5apex.exe")
    # Must end in .exe to distinguish from the game name header line
    game_exe_match = re.search(
        r"info:\s+Game:\s*(\S+\.exe)", log_text, re.IGNORECASE
    )
    if game_exe_match:
        data["game_exe"] = game_exe_match.group(1).strip()

    # gamescope_version
    gamescope_ver_match = re.search(
        r"gamescope version\s+([\d.]+)", log_text, re.IGNORECASE
    )
    if gamescope_ver_match:
        data["gamescope_version"] = gamescope_ver_match.group(1).strip()

    # dx_level: D3D feature level from DXVK or VKD3D
    dx_match = re.search(
        r"(?:info:|vkd3d:)\s+(D3D(?:11|12)?_FEATURE_LEVEL_[\w_]+)", log_text
    )
    if dx_match:
        data["dx_level"] = dx_match.group(1).strip()

    # cpu
    cpu_match = re.search(r"^CPU:\s*(.+)", log_text, re.MULTILINE)
    if cpu_match:
        data["cpu"] = cpu_match.group(1).strip()

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
