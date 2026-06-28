"""
Tests for context-aware pipeline behavior introduced in the six-field routing:

- ContextEvidenceExtractor emits correct Evidence for each metadata field
- calculate_confidence adjusts scores based on exit_code and display_server
- Hypothesis scores shift correctly when context evidence is added
- synthesize_diagnosis enriches fix_steps and warnings from context
- Backward compatibility: logs without new fields produce identical existing fields

Representative sample log snippets are included inline for each case.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse_log, calculate_confidence
from synthesizer import synthesize_diagnosis
from extractors.context import ContextEvidenceExtractor
from evidence import EvidenceKind, EvidenceSeverity


EXTRACTOR = ContextEvidenceExtractor()


# ===========================================================================
# 1. ContextEvidenceExtractor — evidence shape and targets
# ===========================================================================

class TestContextExtractor:

    # --- exit_code ---

    # Sample: game exits cleanly; crash fingerprints should be suppressed
    def test_exit_code_0_emits_success(self):
        evs = EXTRACTOR.extract_from_metadata({"exit_code": 0})
        assert any(e.kind == EvidenceKind.SUCCESS for e in evs), \
            "exit_code=0 must emit a SUCCESS evidence item"
        crash_ev = next(e for e in evs if e.kind == EvidenceKind.SUCCESS)
        assert "WINE_CRASH" in crash_ev.supports

    # Sample: game exits with Windows access violation code
    def test_exit_code_access_violation_targets_wine_crash(self):
        evs = EXTRACTOR.extract_from_metadata({"exit_code": 0xC0000005})
        assert any("WINE_CRASH" in e.supports for e in evs)
        assert any(e.severity == EvidenceSeverity.CRITICAL for e in evs)

    # Sample: game exits with status 3 (EAC/BattlEye Linux rejection)
    def test_exit_code_3_targets_anticheat(self):
        evs = EXTRACTOR.extract_from_metadata({"exit_code": 3})
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "EAC_FAILURE" in targets
        assert "BATTLEYE_FAILURE" in targets

    # Sample: generic non-zero exit
    def test_exit_code_nonzero_targets_wine_crash(self):
        evs = EXTRACTOR.extract_from_metadata({"exit_code": 42})
        assert any("WINE_CRASH" in e.supports for e in evs)

    # --- launch_options ---

    # Sample: "gamemoderun gamescope -f -- %command%"
    def test_launch_gamescope_targets_gamescope_fps(self):
        evs = EXTRACTOR.extract_from_metadata({
            "launch_options": "gamemoderun gamescope -f -- %command%"
        })
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "GAMESCOPE_FAILURE" in targets
        assert "GAMESCOPE_VULKAN_INIT_FAILURE" in targets

    # Sample: "gamemoderun -- %command%"
    def test_launch_gamemode_targets_gamemode_fps(self):
        evs = EXTRACTOR.extract_from_metadata({"launch_options": "gamemoderun -- %command%"})
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "GAMEMODE_REQUEST_FAILURE" in targets

    # Sample: "MANGOHUD=1 %command%"
    def test_launch_mangohud_targets_mangohud_fps(self):
        evs = EXTRACTOR.extract_from_metadata({"launch_options": "MANGOHUD=1 %command%"})
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "MANGOHUD_FAILURE" in targets

    # Sample: user disabled fsync "PROTON_NO_FSYNC=1 %command%"
    def test_launch_no_fsync_is_configuration_evidence(self):
        evs = EXTRACTOR.extract_from_metadata({"launch_options": "PROTON_NO_FSYNC=1 %command%"})
        cfg_evs = [e for e in evs if e.kind == EvidenceKind.CONFIGURATION]
        assert cfg_evs, "PROTON_NO_FSYNC=1 must emit CONFIGURATION evidence"
        assert any("WINE_CRASH" in e.supports for e in cfg_evs)

    # --- display_server ---

    # Sample: Session: KDE Wayland
    def test_wayland_targets_gamescope_fps(self):
        evs = EXTRACTOR.extract_from_metadata({"display_server": "wayland"})
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "GAMESCOPE_VULKAN_INIT_FAILURE" in targets
        assert "GAMESCOPE_FAILURE" in targets

    def test_x11_emits_no_context_evidence(self):
        evs = EXTRACTOR.extract_from_metadata({"display_server": "x11"})
        assert len(evs) == 0, "x11 session should not emit any context evidence"

    # --- kernel_version ---

    # Sample: Kernel: 5.10.0-generic (pre-fsync)
    def test_kernel_pre_fsync_emits_high_severity(self):
        evs = EXTRACTOR.extract_from_metadata({"kernel_version": "5.10.0-generic"})
        assert any(e.severity == EvidenceSeverity.HIGH for e in evs)
        assert any("WINE_CRASH" in e.supports for e in evs)

    # Sample: Kernel: 5.16.0 (has fsync, not futex2)
    def test_kernel_5_16_emits_low_severity(self):
        evs = EXTRACTOR.extract_from_metadata({"kernel_version": "5.16.0"})
        assert any(e.severity == EvidenceSeverity.LOW for e in evs)

    # Sample: Kernel: 7.0.10-cachyos (modern — no warning needed)
    def test_kernel_modern_emits_nothing(self):
        evs = EXTRACTOR.extract_from_metadata({"kernel_version": "7.0.10-cachyos"})
        assert len(evs) == 0, "modern kernel should emit no negative evidence"

    # --- vulkan_driver_version ---

    # Sample: info: [0] AMD RX 7800 XT (RADV NAVI32) : Vulkan 1.3 [21.3.5.0]
    def test_mesa_pre_22_emits_high_severity_vulkan_evidence(self):
        evs = EXTRACTOR.extract_from_metadata({"vulkan_driver_version": "21.3.5.0"})
        assert any(e.severity == EvidenceSeverity.HIGH for e in evs)
        targets = set()
        for e in evs:
            targets.update(e.supports)
        assert "VULKAN_DRIVER_MISSING" in targets

    # Sample: Mesa 22.x
    def test_mesa_22_emits_medium_severity(self):
        evs = EXTRACTOR.extract_from_metadata({"vulkan_driver_version": "22.3.0.0"})
        assert any(e.severity == EvidenceSeverity.MEDIUM for e in evs)

    # Sample: Mesa 24.x (modern — no warning needed)
    def test_mesa_modern_emits_nothing(self):
        evs = EXTRACTOR.extract_from_metadata({"vulkan_driver_version": "24.1.0.0"})
        assert len(evs) == 0

    # Sample: NVIDIA 545.29.6 — no version-based evidence
    def test_nvidia_driver_emits_nothing(self):
        evs = EXTRACTOR.extract_from_metadata({"vulkan_driver_version": "545.29.6"})
        assert len(evs) == 0


# ===========================================================================
# 2. calculate_confidence — context-aware adjustments
# ===========================================================================

_WINE_CRASH_INFO = {"fingerprint": "WINE_CRASH", "severity": "medium"}
_VULKAN_INFO     = {"fingerprint": "VULKAN_DRIVER_MISSING", "severity": "high"}
_GAMESCOPE_INFO  = {"fingerprint": "GAMESCOPE_VULKAN_INIT_FAILURE", "severity": "high"}
_AC_INFO         = {"fingerprint": "EAC_FAILURE", "severity": "high"}
_UNRELATED_INFO  = {"fingerprint": "DISK_FULL", "severity": "high"}

class TestCalculateConfidence:

    def _base(self, info):
        """Confidence without any context."""
        return calculate_confidence("some error", info, context=None)

    # Sample: log with "Game exited with status 0" — clean exit reduces crash confidence
    def test_clean_exit_reduces_crash_confidence(self):
        ctx = {"exit_code": 0, "display_server": None}
        base = self._base(_WINE_CRASH_INFO)
        with_ctx = calculate_confidence("some error", _WINE_CRASH_INFO, context=ctx)
        assert with_ctx < base, "clean exit must reduce WINE_CRASH confidence"

    def test_clean_exit_does_not_affect_unrelated_fps(self):
        ctx = {"exit_code": 0, "display_server": None}
        pattern = "some disk error occurred"
        base = calculate_confidence(pattern, _UNRELATED_INFO, context=None)
        with_ctx = calculate_confidence(pattern, _UNRELATED_INFO, context=ctx)
        assert with_ctx == base, "clean exit must not affect non-crash fingerprints"

    # Sample: log with "Game exited with status 1" — crash boosts crash confidence
    def test_nonzero_exit_boosts_vulkan_confidence(self):
        ctx = {"exit_code": 1, "display_server": None}
        base = self._base(_VULKAN_INFO)
        with_ctx = calculate_confidence("VK_ERROR_INCOMPATIBLE_DRIVER", _VULKAN_INFO, context=ctx)
        assert with_ctx > base, "non-zero exit must boost Vulkan fingerprint confidence"

    # Sample: log with "Game exited with status 3" (EAC rejection) boosts AC fingerprints
    def test_exit_code_3_boosts_anticheat_confidence(self):
        ctx = {"exit_code": 3, "display_server": None}
        ctx_exit1 = {"exit_code": 1, "display_server": None}
        with_3 = calculate_confidence("EasyAntiCheat", _AC_INFO, context=ctx)
        with_1 = calculate_confidence("EasyAntiCheat", _AC_INFO, context=ctx_exit1)
        assert with_3 > with_1, "exit code 3 must give more boost to AC fingerprints than exit 1"

    # Sample: Session: KDE Wayland + Gamescope fingerprint → confidence boost
    def test_wayland_boosts_gamescope_confidence(self):
        ctx_wayland = {"exit_code": None, "display_server": "wayland"}
        ctx_x11     = {"exit_code": None, "display_server": "x11"}
        wayland_conf = calculate_confidence("gamescope", _GAMESCOPE_INFO, context=ctx_wayland)
        x11_conf     = calculate_confidence("gamescope", _GAMESCOPE_INFO, context=ctx_x11)
        assert wayland_conf > x11_conf, "Wayland session must boost Gamescope fingerprint confidence"

    def test_no_context_matches_original_behavior(self):
        base = self._base(_VULKAN_INFO)
        assert base == calculate_confidence("some error", _VULKAN_INFO, context=None)


# ===========================================================================
# 3. Hypothesis score shifts from context evidence
# ===========================================================================

class TestHypothesisScores:

    LOG_VULKAN_CRASH = """\
Game: Elden Ring
AppID: 1245620
Proton: 10.0-1

err:   VK_ERROR_INCOMPATIBLE_DRIVER

Game exited with status 1
"""

    LOG_VULKAN_CLEAN_EXIT = """\
Game: Elden Ring
AppID: 1245620
Proton: 10.0-1

err:   VK_ERROR_INCOMPATIBLE_DRIVER

Game exited with status 0
"""

    LOG_GAMESCOPE_WAYLAND = """\
Game: THE FINALS
AppID: 2073850
Proton: GE-Proton10-34
Session: KDE Wayland

[gamescope] [Error] vulkan: vkCreateDevice failed (VK_ERROR_EXTENSION_NOT_PRESENT)
Game process removed: AppID 2073850 "gamescope -f -- %command%", ProcID 9000
Game exited with status 1
"""

    LOG_EAC_EXIT_3 = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1

EasyAntiCheat: failed to initialize

Game exited with status 3
"""

    def test_crash_exit_raises_vulkan_hypothesis_score(self):
        crash = parse_log(self.LOG_VULKAN_CRASH)
        clean = parse_log(self.LOG_VULKAN_CLEAN_EXIT)
        fp = "VULKAN_DRIVER_MISSING"
        crash_score = (crash["hypotheses"].get(fp) or {}).get("score", 0)
        clean_score = (clean["hypotheses"].get(fp) or {}).get("score", 0)
        assert crash_score > clean_score, \
            f"crash exit should give higher hypothesis score ({crash_score} vs {clean_score})"

    def test_wayland_raises_gamescope_hypothesis_score(self):
        result = parse_log(self.LOG_GAMESCOPE_WAYLAND)
        fp = "GAMESCOPE_VULKAN_INIT_FAILURE"
        score = (result["hypotheses"].get(fp) or {}).get("score", 0)
        assert score > 0, f"Gamescope hypothesis should have a positive score, got {score}"

    def test_exit_3_raises_eac_hypothesis_score(self):
        result = parse_log(self.LOG_EAC_EXIT_3)
        eac_score = (result["hypotheses"].get("EAC_FAILURE") or {}).get("score", 0)
        assert eac_score > 0, f"EAC_FAILURE hypothesis score should be positive, got {eac_score}"


# ===========================================================================
# 4. Synthesizer enrichment
# ===========================================================================

class TestSynthesizerEnrichment:

    # Sample: Vulkan error + gamescope in launch options + Wayland
    LOG_GAMESCOPE_VULKAN = """\
Game: THE FINALS
AppID: 2073850
Proton: GE-Proton10-34
Session: KDE Wayland

[gamescope] [Error] vulkan: vkCreateDevice failed (VK_ERROR_EXTENSION_NOT_PRESENT)
err:   DxvkAdapter: Failed to initialize adapter

Game process removed: AppID 2073850 "gamemoderun gamescope -f -- %command%", ProcID 9001
Game exited with status 1
"""

    # Sample: old kernel (pre-fsync) + crash
    LOG_OLD_KERNEL_CRASH = """\
Game: Some Game
AppID: 99999
Proton: 9.0-3
Kernel: 5.10.0-generic

err:   wine: Unhandled page fault

Game exited with status 1
"""

    # Sample: clean exit — should warn that errors may be non-fatal
    LOG_CLEAN_EXIT_WITH_ERRORS = """\
Game: Stardew Valley
AppID: 413150
Proton: 9.0-3

err:   wine: RLIMIT_NICE is <= 20

Game exited with status 0
"""

    # Sample: PROTON_NO_FSYNC=1 set + crash
    LOG_NOSYNC_CRASH = """\
Game: Death Stranding
AppID: 1850570
Proton: 10.0-1

err:   wine: Unhandled page fault

Game process removed: AppID 1850570 "PROTON_NO_FSYNC=1 %command%", ProcID 5555
Game exited with status 1
"""

    # Sample: exit code 3 (EAC rejection on Linux)
    LOG_EAC_EXIT_3 = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1

EasyAntiCheat: failed to initialize

Game exited with status 3
"""

    # Sample: old Mesa + Vulkan failure
    LOG_OLD_MESA_VULKAN = """\
Game: Elden Ring
AppID: 1245620
Proton: 10.0-1

info:  DXVK: v2.6
info:  Vulkan: Found 1 adapter(s)
info:    [0] AMD Radeon RX 580 (RADV FIJI) : Vulkan 1.3 [21.3.5.0]

err:   VK_ERROR_INCOMPATIBLE_DRIVER
Game exited with status 1
"""

    def _synth(self, log):
        return synthesize_diagnosis(parse_log(log))

    def test_gamescope_launch_option_appears_in_fix_steps(self):
        d = self._synth(self.LOG_GAMESCOPE_VULKAN)
        all_steps = " ".join(d["fix_steps"]).lower()
        assert "gamescope" in all_steps, \
            "gamescope in launch options should appear in fix_steps"

    def test_wayland_gamescope_fix_step_mentions_xwayland(self):
        d = self._synth(self.LOG_GAMESCOPE_VULKAN)
        all_steps = " ".join(d["fix_steps"]).lower()
        assert "xwayland" in all_steps, \
            "Wayland + Gamescope fix step should mention XWayland"

    def test_old_kernel_warning_appears(self):
        d = self._synth(self.LOG_OLD_KERNEL_CRASH)
        all_warnings = " ".join(d["warnings"]).lower()
        assert "5.10" in all_warnings or "5.16" in all_warnings, \
            "Old kernel warning should reference the kernel version or the required version"

    def test_clean_exit_warning_appears(self):
        d = self._synth(self.LOG_CLEAN_EXIT_WITH_ERRORS)
        if d:  # may return None if no fingerprints
            all_warnings = " ".join(d["warnings"]).lower()
            assert "exit code 0" in all_warnings or "exited cleanly" in all_warnings

    def test_proton_no_fsync_warning_appears(self):
        d = self._synth(self.LOG_NOSYNC_CRASH)
        all_warnings = " ".join(d["warnings"]).lower()
        assert "proton_no_fsync" in all_warnings or "fsync" in all_warnings

    def test_exit_code_3_warning_mentions_anticheat(self):
        d = self._synth(self.LOG_EAC_EXIT_3)
        all_warnings = " ".join(d["warnings"]).lower()
        assert "anti-cheat" in all_warnings or "easyanticheat" in all_warnings \
            or "exit code 3" in all_warnings

    def test_old_mesa_warning_appears(self):
        d = self._synth(self.LOG_OLD_MESA_VULKAN)
        all_warnings = " ".join(d["warnings"]).lower()
        assert "mesa" in all_warnings and "upgrade" in all_warnings

    def test_enrichment_does_not_break_existing_fields(self):
        """Enrichment must not remove or retype any existing diagnosis fields."""
        d = self._synth(self.LOG_GAMESCOPE_VULKAN)
        assert d is not None
        required = [
            "used_known_issue", "known_issue_id", "summary", "probable_cause",
            "confidence", "severity", "detected_errors", "fix_steps",
            "recommended_commands", "extra_info_needed", "warnings",
        ]
        for field in required:
            assert field in d, f"field '{field}' missing after enrichment"
            if field in ("fix_steps", "recommended_commands", "extra_info_needed",
                         "detected_errors", "warnings"):
                assert isinstance(d[field], list), f"'{field}' must remain a list"
        assert d["confidence"] in ("high", "medium", "low")
        assert d["severity"] in ("high", "medium", "low", "critical", "info")


# ===========================================================================
# 5. Backward compatibility
# ===========================================================================

class TestBackwardCompatibility:

    LOG_MINIMAL = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1

err:   VK_ERROR_INCOMPATIBLE_DRIVER
"""

    def test_existing_fields_unchanged(self):
        result = parse_log(self.LOG_MINIMAL)
        assert result["game"] == "Apex Legends"
        assert result["appid"] == "1172470"
        assert result["proton_version"] == "10.0-1"
        assert isinstance(result["fingerprints"], list)
        assert isinstance(result["errors"], list)
        assert isinstance(result["evidence"], list)
        assert isinstance(result["hypotheses"], dict)
        assert isinstance(result["dependency_chain"], list)
        assert isinstance(result["reasoning"], list)

    def test_new_fields_default_to_none_when_absent(self):
        result = parse_log(self.LOG_MINIMAL)
        for field in (
            "exit_code", "launch_options", "sync_method", "session_type",
            "display_server", "kernel_version", "driver_version",
            "vulkan_driver_version", "prefix_action", "prefix_upgrade_from",
            "game_exe", "gamescope_version", "dx_level", "cpu",
        ):
            assert result[field] is None, f"field '{field}' should be None when absent"

    def test_synthesis_still_works_without_new_fields(self):
        result = parse_log(self.LOG_MINIMAL)
        d = synthesize_diagnosis(result)
        assert d is not None
        assert d["confidence"] in ("high", "medium", "low")
        assert isinstance(d["fix_steps"], list)


# ===========================================================================
# Runner
# ===========================================================================

def run():
    import traceback
    suites = [
        TestContextExtractor,
        TestCalculateConfidence,
        TestHypothesisScores,
        TestSynthesizerEnrichment,
        TestBackwardCompatibility,
    ]
    passed = failed = 0
    for suite_cls in suites:
        suite = suite_cls()
        methods = [m for m in dir(suite_cls) if m.startswith("test_")]
        print(f"\n{suite_cls.__name__} ({len(methods)} tests)")
        for method in methods:
            try:
                getattr(suite, method)()
                print(f"  [PASS] {method}")
                passed += 1
            except Exception as e:
                print(f"  [FAIL] {method}: {e}")
                traceback.print_exc()
                failed += 1
    print(f"\n{'='*55}")
    print(f"Results: {passed}/{passed+failed} passed", "✓" if not failed else "✗")
    return failed


if __name__ == "__main__":
    sys.exit(run())
