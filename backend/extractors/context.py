"""
ContextEvidenceExtractor — converts structured metadata parsed from the log header
(exit_code, launch_options, display_server, kernel_version, vulkan_driver_version,
sync_method) into Evidence objects that flow through the existing inference engine.

These evidence items give the hypothesis scorer additional signal that raw pattern
matching cannot provide: e.g. a clean exit_code=0 actively contradicts crash
hypotheses; launch options containing "gamescope" directly support Gamescope
fingerprints even when no Gamescope error text appears in the log.
"""
import re

from evidence import Evidence, EvidenceKind, EvidenceSeverity


_CRASH_FPS = [
    "WINE_CRASH",
    "NTDLL_RELATED_CRASH",
    "SEGFAULT",
    "CORE_DUMPED",
]

_VULKAN_FPS = [
    "VULKAN_DRIVER_MISSING",
    "VULKAN_INIT_FAILURE",
    "VK_ERROR_DEVICE_LOST",
    "VK_ERROR_OUT_OF_DEVICE_MEMORY",
    "VK_ERROR_EXTENSION_NOT_PRESENT",
    "DXVK_ADAPTER_FAILURE",
]

_GAMESCOPE_FPS = [
    "GAMESCOPE_FAILURE",
    "GAMESCOPE_VULKAN_INIT_FAILURE",
    "GAMESCOPE_SWAPCHAIN_FAILURE",
    "GAMESCOPE_OUTPUT_FAILURE",
    "GAMESCOPE_WAYLAND_RELATED",
]

_GAMEMODE_FPS = [
    "GAMEMODE_DAEMON_RELATED",
    "GAMEMODE_REQUEST_FAILURE",
    "GAMEMODE_RELATED",
]

_AC_FPS = [
    "EAC_FAILURE",
    "BATTLEYE_FAILURE",
    "EAC_EOS_RELATED",
    "EAC_LINUX_RUNTIME_RELATED",
    "BATTLEYE_LAUNCHER_RELATED",
]


def _ev(
    id: str,
    raw_text: str,
    extracted_pattern: str,
    kind: EvidenceKind,
    severity: EvidenceSeverity,
    confidence: int,
    supports: list[str],
) -> Evidence:
    return Evidence(
        id=id,
        line_number=None,
        source="context",
        raw_text=raw_text,
        extracted_pattern=extracted_pattern,
        kind=kind,
        severity=severity,
        confidence=confidence,
        supports=supports,
        contradicts=[],
        metadata={},
    )


class ContextEvidenceExtractor:
    """Converts pre-parsed metadata fields into Evidence objects."""

    def extract_from_metadata(self, metadata: dict) -> list[Evidence]:
        items: list[Evidence] = []

        self._exit_code(metadata.get("exit_code"), items)
        self._launch_options(metadata.get("launch_options") or "", items)
        self._display_server(metadata.get("display_server"), items)
        self._kernel_version(metadata.get("kernel_version") or "", items)
        self._vulkan_driver_version(metadata.get("vulkan_driver_version") or "", items)
        # sync_method is used by the synthesizer but doesn't need its own hypothesis
        # evidence — absence of fsync is only meaningful alongside a crash fingerprint.

        return items

    # ------------------------------------------------------------------
    # exit_code
    # ------------------------------------------------------------------

    def _exit_code(self, exit_code: int | None, items: list) -> None:
        if exit_code is None:
            return

        if exit_code == 0:
            # SUCCESS kind has weight -20 in confidence.py, so adding crash
            # fingerprints to `supports` reduces their hypothesis scores.
            items.append(_ev(
                id="ctx_exit_clean",
                raw_text="Game exited with status 0 (clean exit — errors above may be non-fatal)",
                extracted_pattern="exit_code=0",
                kind=EvidenceKind.SUCCESS,
                severity=EvidenceSeverity.INFO,
                confidence=90,
                supports=_CRASH_FPS,
            ))

        elif exit_code == 0xC0000005:
            # Windows ACCESS_VIOLATION — definitive crash signal
            items.append(_ev(
                id="ctx_exit_access_violation",
                raw_text="Game exited with code 0xC0000005 (Windows ACCESS_VIOLATION)",
                extracted_pattern="exit_code=0xc0000005",
                kind=EvidenceKind.ERROR,
                severity=EvidenceSeverity.CRITICAL,
                confidence=95,
                supports=["WINE_CRASH", "NTDLL_RELATED_CRASH"],
            ))

        elif exit_code == 3:
            # EAC and BattlEye both use exit code 3 to signal Linux rejection
            items.append(_ev(
                id="ctx_exit_3_ac_rejection",
                raw_text="Game exited with status 3 (anti-cheat rejection on Linux)",
                extracted_pattern="exit_code=3",
                kind=EvidenceKind.ERROR,
                severity=EvidenceSeverity.HIGH,
                confidence=65,
                supports=_AC_FPS,
            ))

        else:
            # Any other non-zero exit is a generic crash signal
            items.append(_ev(
                id=f"ctx_exit_{exit_code}",
                raw_text=f"Game exited with non-zero status {exit_code}",
                extracted_pattern="exit_code!=0",
                kind=EvidenceKind.ERROR,
                severity=EvidenceSeverity.MEDIUM,
                confidence=55,
                supports=["WINE_CRASH"],
            ))

    # ------------------------------------------------------------------
    # launch_options
    # ------------------------------------------------------------------

    def _launch_options(self, opts: str, items: list) -> None:
        if not opts:
            return
        lower = opts.lower()

        if "gamescope" in lower:
            items.append(_ev(
                id="ctx_launch_gamescope",
                raw_text=f"Launch options include gamescope: {opts}",
                extracted_pattern="launch:gamescope",
                kind=EvidenceKind.CONTEXT,
                severity=EvidenceSeverity.INFO,
                confidence=100,
                supports=_GAMESCOPE_FPS,
            ))

        if "gamemoderun" in lower or ("gamemode" in lower and "gamescope" not in lower):
            items.append(_ev(
                id="ctx_launch_gamemode",
                raw_text=f"Launch options include gamemoderun: {opts}",
                extracted_pattern="launch:gamemoderun",
                kind=EvidenceKind.CONTEXT,
                severity=EvidenceSeverity.INFO,
                confidence=100,
                supports=_GAMEMODE_FPS,
            ))

        if "mangohud" in lower:
            items.append(_ev(
                id="ctx_launch_mangohud",
                raw_text=f"Launch options include MangoHud: {opts}",
                extracted_pattern="launch:mangohud",
                kind=EvidenceKind.CONTEXT,
                severity=EvidenceSeverity.INFO,
                confidence=100,
                supports=["MANGOHUD_FAILURE", "MANGOHUD_CONFIG_RELATED"],
            ))

        # Explicitly disabled sync primitives worsen crash likelihood
        if re.search(r"PROTON_NO_FSYNC=1", opts):
            items.append(_ev(
                id="ctx_launch_no_fsync",
                raw_text=f"PROTON_NO_FSYNC=1 in launch options — fsync disabled",
                extracted_pattern="launch:PROTON_NO_FSYNC=1",
                kind=EvidenceKind.CONFIGURATION,
                severity=EvidenceSeverity.MEDIUM,
                confidence=90,
                supports=["WINE_CRASH"],
            ))

        if re.search(r"PROTON_NO_ESYNC=1", opts):
            items.append(_ev(
                id="ctx_launch_no_esync",
                raw_text=f"PROTON_NO_ESYNC=1 in launch options — esync disabled",
                extracted_pattern="launch:PROTON_NO_ESYNC=1",
                kind=EvidenceKind.CONFIGURATION,
                severity=EvidenceSeverity.LOW,
                confidence=80,
                supports=["WINE_CRASH"],
            ))

    # ------------------------------------------------------------------
    # display_server
    # ------------------------------------------------------------------

    def _display_server(self, display_server: str | None, items: list) -> None:
        if display_server == "wayland":
            items.append(_ev(
                id="ctx_wayland_session",
                raw_text="Session is running on Wayland",
                extracted_pattern="display_server=wayland",
                kind=EvidenceKind.ENVIRONMENT,
                severity=EvidenceSeverity.INFO,
                confidence=100,
                supports=_GAMESCOPE_FPS,
            ))

    # ------------------------------------------------------------------
    # kernel_version
    # ------------------------------------------------------------------

    def _kernel_version(self, kernel_ver: str, items: list) -> None:
        m = re.match(r"(\d+)\.(\d+)", kernel_ver)
        if not m:
            return
        major, minor = int(m.group(1)), int(m.group(2))

        if major < 5 or (major == 5 and minor < 16):
            # Pre-fsync kernel — significantly increases crash risk
            items.append(_ev(
                id="ctx_kernel_pre_fsync",
                raw_text=f"Kernel {kernel_ver} is below 5.16 — fsync unavailable",
                extracted_pattern="kernel<5.16",
                kind=EvidenceKind.ENVIRONMENT,
                severity=EvidenceSeverity.HIGH,
                confidence=90,
                supports=["WINE_CRASH"],
            ))
        elif (major == 5 and minor >= 16) or (major == 6 and minor == 0):
            # Has fsync but not futex2 (futex2 landed in 6.1)
            items.append(_ev(
                id="ctx_kernel_pre_futex2",
                raw_text=f"Kernel {kernel_ver} has fsync but futex2 requires kernel 6.1+",
                extracted_pattern="kernel_5.16_to_6.0",
                kind=EvidenceKind.ENVIRONMENT,
                severity=EvidenceSeverity.LOW,
                confidence=80,
                supports=[],
            ))

    # ------------------------------------------------------------------
    # vulkan_driver_version (from DXVK adapter info)
    # ------------------------------------------------------------------

    def _vulkan_driver_version(self, vk_ver: str, items: list) -> None:
        if not vk_ver:
            return
        parts = vk_ver.split(".")
        if not parts:
            return
        try:
            major = int(parts[0])
        except ValueError:
            return

        # Mesa versions are 17–25; NVIDIA driver versions are 400+
        if major >= 100:
            return  # NVIDIA — no version-based evidence emitted

        if major < 22:
            items.append(_ev(
                id="ctx_mesa_very_old",
                raw_text=f"Mesa {vk_ver} is very old — many required Vulkan extensions are absent",
                extracted_pattern="mesa<22",
                kind=EvidenceKind.HARDWARE,
                severity=EvidenceSeverity.HIGH,
                confidence=90,
                supports=_VULKAN_FPS,
            ))
        elif major < 23:
            items.append(_ev(
                id="ctx_mesa_22",
                raw_text=f"Mesa {vk_ver} — some VKD3D-Proton features require Mesa 23+",
                extracted_pattern="mesa_22",
                kind=EvidenceKind.HARDWARE,
                severity=EvidenceSeverity.MEDIUM,
                confidence=75,
                supports=["VK_ERROR_EXTENSION_NOT_PRESENT"],
            ))
        # Mesa 23+ — no additional warning needed
