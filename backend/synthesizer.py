import re

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


# ---------------------------------------------------------------------------
# Context enrichment
# ---------------------------------------------------------------------------

def _enrich_with_context(diagnosis: dict, parsed: dict) -> dict:
    """
    Append context-specific fix steps and warnings derived from the six
    newly parsed metadata fields: exit_code, launch_options, sync_method,
    session_type/display_server, kernel_version, vulkan_driver_version.

    Called at the end of both synthesis paths so both KNOWN_ISSUES and
    auto-synthesized diagnoses receive the same contextual enrichment.
    """
    extra_steps: list[str] = []
    extra_warnings: list[str] = []

    exit_code    = parsed.get("exit_code")
    launch_opts  = parsed.get("launch_options") or ""
    sync_method  = parsed.get("sync_method")
    display_srv  = parsed.get("display_server")
    kernel_ver   = parsed.get("kernel_version") or ""
    vk_ver       = parsed.get("vulkan_driver_version") or ""
    primary_fp   = (parsed.get("primary_fingerprint") or {}).get("fingerprint", "")

    # ---- exit_code --------------------------------------------------------

    if exit_code is not None:
        if exit_code == 0:
            extra_warnings.append(
                "The game exited cleanly (exit code 0). The errors above may be "
                "non-fatal warnings — try launching the game again before troubleshooting."
            )
        elif exit_code == 0xC0000005:
            extra_warnings.append(
                "Exit code 0xC0000005 is a Windows ACCESS_VIOLATION: the process crashed "
                "due to an invalid memory access. Common causes: missing or mismatched DLL, "
                "corrupt Proton prefix, or a GPU driver crash mid-frame."
            )
        elif exit_code == 3:
            extra_warnings.append(
                "Exit code 3 is commonly used by EasyAntiCheat and BattlEye on Linux to "
                "signal that the anti-cheat blocked the launch. Confirm the game's EAC/BE "
                "version has Linux support and that no unsupported kernel flags are set."
            )
        elif exit_code != 0:
            extra_warnings.append(
                f"Game exited with non-zero status {exit_code}, confirming the process "
                "did not shut down cleanly."
            )

    # ---- launch_options ---------------------------------------------------

    if launch_opts:
        opts_lower = launch_opts.lower()

        # Gamescope in launch options + Gamescope fingerprint → name the culprit
        if "gamescope" in opts_lower and "GAMESCOPE" in primary_fp:
            extra_steps.append(
                f"Your launch options include gamescope (\"{launch_opts}\"). "
                "Temporarily remove gamescope from your launch options to test whether "
                "it is the source of this failure."
            )

        # Gamescope in launch options — always worth noting even without a GAMESCOPE fp
        elif "gamescope" in opts_lower and "VULKAN" in primary_fp:
            extra_steps.append(
                "Gamescope is in your launch options. Vulkan failures inside Gamescope can "
                "be caused by extension mismatches between your gamescope version and Mesa. "
                "Try launching without gamescope to isolate the issue."
            )

        # Disabled sync is always a warning-worthy misconfiguration
        if re.search(r"PROTON_NO_FSYNC=1", launch_opts):
            extra_warnings.append(
                "PROTON_NO_FSYNC=1 is set in your launch options, disabling fsync. "
                "Remove this flag — fsync prevents threading deadlocks in many games."
            )

        if re.search(r"PROTON_NO_ESYNC=1", launch_opts):
            extra_warnings.append(
                "PROTON_NO_ESYNC=1 is set in your launch options, disabling esync. "
                "Remove this unless you have a specific reason to keep it."
            )

    # ---- sync_method ------------------------------------------------------

    if sync_method is None and primary_fp in {
        "WINE_CRASH", "NTDLL_RELATED_CRASH", "PROTON_WINEBOOT_FAILURE",
    }:
        extra_steps.append(
            "Neither fsync nor esync was detected in the log. Wine synchronization "
            "primitives (fsync ≥ kernel 5.16, esync on older kernels) are important for "
            "multi-threaded game stability. Ensure PROTON_NO_FSYNC is not set and that "
            "your kernel supports fsync."
        )
    elif sync_method:
        # Positive confirmation — include in context but no action needed
        diagnosis.setdefault("extra_info_needed", [])  # keep key present

    # ---- display_server + gamescope fingerprint/launch option ---------------------------

    gamescope_active = "GAMESCOPE" in primary_fp or "gamescope" in launch_opts.lower()

    if display_srv and gamescope_active:
        if display_srv == "wayland":
            extra_steps.append(
                "You are running on a Wayland session with Gamescope. Ensure XWayland "
                "is installed (xorg-xwayland) and that your gamescope version is "
                "compatible with your installed Mesa version."
            )
        else:
            extra_steps.append(
                "You are running Gamescope on an X11 session. Verify that the DISPLAY "
                "environment variable is set correctly and that no other compositor is "
                "holding an exclusive lock on the display."
            )

    # ---- kernel_version ---------------------------------------------------

    if kernel_ver:
        km = re.match(r"(\d+)\.(\d+)", kernel_ver)
        if km:
            major, minor = int(km.group(1)), int(km.group(2))
            if major < 5 or (major == 5 and minor < 16):
                extra_warnings.append(
                    f"Kernel {kernel_ver} is below 5.16 — fsync is not available on this "
                    "kernel. Upgrade to 5.16+ (or 6.1+ for futex2) for significantly better "
                    "game stability with Proton."
                )
            elif (major == 5 and minor >= 16) or major == 6:
                if major < 6 or (major == 6 and minor < 1):
                    extra_warnings.append(
                        f"Kernel {kernel_ver} supports fsync but not futex2 (available in "
                        "6.1+). futex2 further reduces threading overhead in Proton games."
                    )

    # ---- vulkan_driver_version --------------------------------------------

    if vk_ver:
        parts = vk_ver.split(".")
        try:
            major = int(parts[0])
            is_mesa = major < 100  # Mesa 17–25; NVIDIA 400+

            if is_mesa:
                if major < 22:
                    extra_warnings.append(
                        f"Mesa {vk_ver} is very old. Upgrade to Mesa 23.0+ for significantly "
                        "better Vulkan extension coverage and game compatibility."
                    )
                elif major < 23:
                    extra_warnings.append(
                        f"Mesa {vk_ver} is functional but Mesa 23.0+ is recommended for "
                        "full VKD3D-Proton and RADV compatibility."
                    )
                # Mesa 23+ — no warning needed
            else:
                # NVIDIA: just add version context, no version-based warnings
                pass

        except (ValueError, IndexError):
            pass

    # ---- apply -------------------------------------------------------

    if extra_steps:
        diagnosis["fix_steps"] = diagnosis.get("fix_steps", []) + extra_steps
    if extra_warnings:
        diagnosis["warnings"] = diagnosis.get("warnings", []) + extra_warnings

    return diagnosis


# ---------------------------------------------------------------------------
# Main synthesis entry point
# ---------------------------------------------------------------------------

def synthesize_diagnosis(parsed: dict) -> dict | None:
    """
    Build a deterministic diagnosis from parsed fingerprint and hypothesis data.

    Flow:
    1. KNOWN_ISSUES entry for the primary fingerprint — hand-crafted, highest quality.
    2. Auto-synthesis from the fingerprint's explanation, known_fix, and safe_commands.
    3. Context enrichment appended to both paths via _enrich_with_context().
    4. Returns None only when zero fingerprints were detected, triggering the AI fallback.

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
        diagnosis = {
            "used_known_issue": True,
            "known_issue_id": fingerprint_id,
            "summary": issue["summary"],
            "probable_cause": issue["probable_cause"],
            "confidence": confidence,
            "severity": issue["severity"],
            "detected_errors": parsed.get("errors", []),
            "fix_steps": list(issue["fix_steps"]),
            "recommended_commands": issue["recommended_commands"],
            "extra_info_needed": [],
            "warnings": list(issue.get("warnings", [])),
        }
        return _enrich_with_context(diagnosis, parsed)

    # --- Path 2: auto-synthesize from fingerprint metadata ---
    metadata = get_fingerprint_metadata(fingerprint_id)
    fix_steps = list(primary.get("known_fix") or [])
    safe_commands = list(primary.get("safe_commands") or [])
    explanation = primary.get("explanation") or metadata.get(
        "short_description", f"{fingerprint_id} detected."
    )

    secondary_ids = [
        f.get("fingerprint")
        for f in fingerprints[1:4]
        if f.get("fingerprint") and f.get("fingerprint") != fingerprint_id
    ]

    short_desc = metadata.get("short_description", f"{fingerprint_id} detected.")
    summary = (
        f"{short_desc} Related issues also detected: {', '.join(secondary_ids)}."
        if secondary_ids
        else short_desc
    )

    if not fix_steps:
        fix_steps = [
            "Review the log for earlier errors that may explain this issue.",
            "Try a different Proton version.",
            "Verify game files in Steam.",
            "Disable overlays and custom launch options while testing.",
        ]

    diagnosis = {
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
    return _enrich_with_context(diagnosis, parsed)
