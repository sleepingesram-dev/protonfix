"""
Redactor test suite — serves as both verification and the authoritative redaction report.

Each class covers one PII category.  The TestDiagnosticPreservation class verifies
that fingerprint-relevant strings survive completely unaltered.

Run: pytest tests/test_redactor.py -v
"""

import sys
import os

# Allow imports from backend/ root when run as pytest tests/test_redactor.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from redactor import redact, REASONS


# ── Linux home paths ──────────────────────────────────────────────────────────

class TestLinuxHomePath:
    def test_simple_path_redacted(self):
        r = redact("/home/alice/.steam/steam/steamapps/")
        assert "/home/[USERNAME]/" in r.text
        assert "alice" not in r.text
        # Diagnostic path after the username is preserved
        assert ".steam/steam/steamapps/" in r.text

    def test_multiple_occurrences_counted(self):
        log = "/home/bob/.steam/\n/home/bob/.local/share/"
        r = redact(log)
        assert r.counts.get("linux_home_path", 0) == 2

    def test_proton_compatdata_path(self):
        log = "info: proton prefix: /home/carol/.local/share/Steam/steamapps/compatdata/570/"
        r = redact(log)
        assert "carol" not in r.text
        assert "Steam/steamapps/compatdata/570/" in r.text

    def test_run_user_in_same_log(self):
        log = "/home/dave/game.log XDG_RUNTIME_DIR=/run/user/1000/"
        r = redact(log)
        assert "dave" not in r.text
        assert "/run/user/[UID]/" in r.text


# ── macOS home paths ──────────────────────────────────────────────────────────

class TestMacOSHomePath:
    def test_macos_path_redacted(self):
        r = redact("/Users/eve/Library/Application Support/Steam/")
        assert "/Users/[USERNAME]/" in r.text
        assert "eve" not in r.text
        assert "Library/Application Support/Steam/" in r.text


# ── Windows user paths ────────────────────────────────────────────────────────

class TestWindowsUserPath:
    def test_windows_path_redacted(self):
        r = redact(r"C:\Users\dave\AppData\Local\Temp")
        assert r"C:\Users\[USERNAME]\AppData" in r.text
        assert "dave" not in r.text

    def test_case_insensitive(self):
        r = redact(r"c:\users\Eve\Documents")
        assert "Eve" not in r.text
        assert "[USERNAME]" in r.text

    def test_different_drive_letter_preserved(self):
        r = redact("D:\\Users\\frank\\AppData\\Local\\Temp")
        assert "D:\\Users\\[USERNAME]\\AppData" in r.text
        assert "frank" not in r.text


# ── Wine Z: paths ─────────────────────────────────────────────────────────────

class TestWineZPath:
    def test_wine_z_backslash(self):
        r = redact(r"Z:\home\grace\.wine\drive_c\ ")
        assert "[USERNAME]" in r.text
        assert "grace" not in r.text
        # path structure after username is preserved
        assert ".wine" in r.text

    def test_wine_z_slash(self):
        r = redact("Z:/home/henry/.wine/")
        assert "[USERNAME]" in r.text
        assert "henry" not in r.text


# ── Steam identifiers ─────────────────────────────────────────────────────────

class TestSteamIdentifiers:
    def test_steamid64_redacted(self):
        r = redact("steamid: 76561198012345678")
        assert "[STEAM_ID64]" in r.text
        assert "76561198012345678" not in r.text

    def test_steamid3_redacted(self):
        r = redact("SteamID: [U:1:52079950]")
        assert "[STEAM_ID3]" in r.text
        assert "52079950" not in r.text

    def test_userdata_account_id_redacted(self):
        log = "/home/user/.steam/steam/userdata/12345678/favorites.vdf"
        r = redact(log)
        assert "[STEAM_ACCT_ID]" in r.text
        assert "12345678" not in r.text
        # Filename preserved
        assert "favorites.vdf" in r.text

    def test_short_appid_not_redacted(self):
        """AppIDs (3–7 digits) are diagnostic — must not be redacted."""
        r = redact("AppID: 570\nAppID: 1091500")
        assert "570" in r.text
        assert "1091500" in r.text
        assert "[STEAM_ID64]" not in r.text


# ── IP addresses ──────────────────────────────────────────────────────────────

class TestIPAddresses:
    def test_private_ipv4_redacted(self):
        r = redact("Connecting to 192.168.1.100:27015...")
        assert "[IP_ADDRESS]" in r.text
        assert "192.168.1.100" not in r.text

    def test_loopback_redacted(self):
        r = redact("server at 127.0.0.1:8080")
        assert "[IP_ADDRESS]" in r.text

    def test_windows_version_not_redacted(self):
        """10.0.22000 is a 3-component Windows build string, not an IPv4."""
        r = redact("Windows 10.0.22000")
        assert "10.0.22000" in r.text
        assert "[IP_ADDRESS]" not in r.text

    def test_dxvk_version_not_redacted(self):
        """DXVK versions like 2.3.1 must survive."""
        r = redact("DXVK 2.3.1 initialized")
        assert "2.3.1" in r.text
        assert "[IP_ADDRESS]" not in r.text

    def test_invalid_octet_not_redacted(self):
        """999.999.999.999 has out-of-range octets — must not be treated as IP."""
        r = redact("bogus 999.999.999.999 value")
        assert "999.999.999.999" in r.text

    def test_full_ipv6_redacted(self):
        r = redact("IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        assert "[IP_ADDRESS_V6]" in r.text
        assert "2001:0db8:85a3" not in r.text


# ── Email addresses ───────────────────────────────────────────────────────────

class TestEmailAddresses:
    def test_email_redacted(self):
        r = redact("Contact: user@example.com for support")
        assert "[EMAIL]" in r.text
        assert "user@example.com" not in r.text

    def test_wine_license_email(self):
        r = redact("wine: registered to alice.smith@gaming.example.org")
        assert "[EMAIL]" in r.text
        assert "alice.smith" not in r.text


# ── UUIDs ─────────────────────────────────────────────────────────────────────

class TestUUIDs:
    def test_uuid_redacted(self):
        r = redact("DeviceID: 6a2f8c3d-1234-5678-abcd-ef0123456789")
        assert "[UUID]" in r.text
        assert "6a2f8c3d-1234-5678-abcd-ef0123456789" not in r.text

    def test_uuid_in_braces_redacted(self):
        r = redact("Volume{6a2f8c3d-1234-5678-abcd-ef0123456789}")
        assert "[UUID]" in r.text
        # Braces are preserved as they are not part of the UUID match
        assert "Volume{[UUID]}" in r.text


# ── MAC addresses ─────────────────────────────────────────────────────────────

class TestMACAddresses:
    def test_colon_mac_redacted(self):
        r = redact("adapter: 00:1A:2B:3C:4D:5E")
        assert "[MAC_ADDRESS]" in r.text
        assert "00:1A:2B:3C:4D:5E" not in r.text

    def test_hyphen_mac_redacted(self):
        r = redact("NIC: 00-1A-2B-3C-4D-5E")
        assert "[MAC_ADDRESS]" in r.text
        assert "00-1A-2B-3C-4D-5E" not in r.text


# ── Windows SIDs ──────────────────────────────────────────────────────────────

class TestWindowsSID:
    def test_sid_redacted(self):
        r = redact(r"HKEY_USERS\S-1-5-21-1234567890-1234567890-1234567890-1001")
        assert "[WINDOWS_SID]" in r.text
        assert "S-1-5-21" not in r.text


# ── /run/user/ paths ──────────────────────────────────────────────────────────

class TestRunUserPath:
    def test_run_user_uid_redacted(self):
        r = redact("XDG_RUNTIME_DIR=/run/user/1000/")
        assert "/run/user/[UID]/" in r.text
        assert "/run/user/1000/" not in r.text


# ── /media/ mounts ────────────────────────────────────────────────────────────

class TestMediaMountPath:
    def test_media_mount_redacted(self):
        r = redact("/media/alice/SANDISK/games/CyberpunkSaves/")
        assert "/media/[USERNAME]/" in r.text
        assert "alice" not in r.text
        # Drive label and subdirectory are diagnostic — preserved
        assert "SANDISK/games/CyberpunkSaves/" in r.text


# ── uid/gid info strings ──────────────────────────────────────────────────────

class TestUIDGIDInfo:
    def test_uid_entry_redacted(self):
        r = redact("uid=1000(alice) gid=1000(alice)")
        assert "alice" not in r.text
        assert "[USERNAME]" in r.text
        assert "[UID]" in r.text

    def test_keyword_preserved(self):
        r = redact("uid=1000(alice)")
        assert "uid=" in r.text


# ── Hostname keyword ──────────────────────────────────────────────────────────

class TestHostnameKeyword:
    def test_hostname_equals_redacted(self):
        r = redact("hostname=my-gaming-pc")
        assert "[HOSTNAME]" in r.text
        assert "my-gaming-pc" not in r.text
        assert "hostname=" in r.text

    def test_hostname_colon_redacted(self):
        r = redact("hostname: GAMING-RIG-01")
        assert "[HOSTNAME]" in r.text
        assert "GAMING-RIG-01" not in r.text

    def test_case_insensitive(self):
        r = redact("HOSTNAME=TOWER")
        assert "[HOSTNAME]" in r.text
        assert "TOWER" not in r.text


# ── Diagnostic preservation ───────────────────────────────────────────────────

DIAGNOSTIC_STRINGS = [
    "vkCreateInstance failed",
    "EAC: Error: failed to authenticate",
    "wine: Unhandled page fault on read access to 0x00000010",
    "DXVK: v2.5.3",
    "Proton 8.0-4",
    "fsync: up and running",
    "AppID 570",
    "AppID 1091500",
    "GameMode: Failed to request mode: com.feralinteractive.GameMode",
    "VK_ERROR_INCOMPATIBLE_DRIVER",
    "MANGOHUD_CONFIG=/etc/MangoHud.conf",
    "err: DXVK: non-fatal initialization warning",
    "proton: Downloading proton 8.0",
    "no space left on device",
    "nvk: using NVK 24.2.0",
    "dxvk: v1.10.3",
    "VKD3D-Proton 2.12",
    "error 0xC0000005",
    "wine version 8.0 (Staging)",
    "Gamescope 3.14.2",
    "OpenGL renderer: NVIDIA GeForce RTX 4070",
    "Vulkan 1.3.261",
]


@pytest.mark.parametrize("s", DIAGNOSTIC_STRINGS)
def test_diagnostic_string_preserved(s: str):
    r = redact(s)
    assert r.text == s, (
        f"Diagnostic string was altered:\n  before: {s!r}\n  after:  {r.text!r}"
    )


# ── Report structure ──────────────────────────────────────────────────────────

class TestReport:
    def test_empty_log_no_redactions(self):
        r = redact("")
        assert not r.was_redacted
        assert r.total == 0
        assert r.report()["by_category"] == {}

    def test_clean_log_no_redactions(self):
        r = redact("vkCreateInstance failed\nfsync: up and running\nProton 8.0-4")
        assert not r.was_redacted

    def test_report_structure(self):
        r = redact("/home/alice/.steam/ steamid: 76561198012345678")
        report = r.report()
        assert "was_redacted" in report
        assert "total_redactions" in report
        assert "by_category" in report
        for cat, info in report["by_category"].items():
            assert "count" in info
            assert "reason" in info

    def test_reasons_populated(self):
        r = redact("/home/alice/.steam/")
        report = r.report()
        entry = report["by_category"]["linux_home_path"]
        assert len(entry["reason"]) > 20

    def test_total_matches_sum(self):
        log = "/home/alice/.steam/ 192.168.1.1 user@example.com"
        r = redact(log)
        assert r.total == sum(r.counts.values())

    def test_was_redacted_flag(self):
        clean = redact("VK_ERROR_INCOMPATIBLE_DRIVER")
        dirty = redact("/home/alice/.steam/")
        assert not clean.was_redacted
        assert dirty.was_redacted

    def test_all_reasons_covered(self):
        """Every category produced by redact() has an entry in REASONS."""
        log = (
            "/home/alice/.steam/steam/userdata/12345678/\n"
            r"C:\Users\bob\AppData\ " + "\n"
            "76561198012345678\n"
            "[U:1:52079950]\n"
            "user@example.com\n"
            "S-1-5-21-1111111111-2222222222-3333333333-1001\n"
            "uid=1000(alice)\n"
            "6a2f8c3d-1234-5678-abcd-ef0123456789\n"
            "00:1A:2B:3C:4D:5E\n"
            "192.168.1.1\n"
            "hostname=mymachine\n"
        )
        r = redact(log)
        for cat in r.counts:
            assert cat in REASONS, f"Category {cat!r} has no entry in REASONS"


# ── Realistic composite log ───────────────────────────────────────────────────

class TestRealisticLog:
    """End-to-end test with a realistic multi-source gaming log excerpt."""

    LOG = (
        "wine: WINEDEBUG=fixme+module\n"
        "steamid user 76561198012345678 connecting\n"
        "[U:1:52079950] account lookup\n"
        "/home/carol/.steam/steam/steamapps/common/Cyberpunk 2077/bin/x64/Cyberpunk2077.exe\n"
        r"proton: mapped Z:\home\carol\.steam\ from /home/carol/.steam/" + "\n"
        "/home/carol/.steam/steam/userdata/52079950/config/localconfig.vdf\n"
        "uid=1000(carol) gid=1000(carol)\n"
        "XDG_RUNTIME_DIR=/run/user/1000/\n"
        "hostname=carol-desktop\n"
        "vkCreateInstance failed\n"
        "VK_ERROR_INCOMPATIBLE_DRIVER\n"
        "Proton 8.0-4 initialized\n"
        "DXVK: v2.3.1\n"
        "AppID 1091500\n"
    )

    def test_no_username_leaks(self):
        r = redact(self.LOG)
        assert "carol" not in r.text

    def test_no_steam_id_leaks(self):
        r = redact(self.LOG)
        assert "76561198012345678" not in r.text
        assert "52079950" not in r.text  # SteamID3 account_id
        # NOTE: The userdata folder 52079950 might survive if the steam_userdata_id
        # pattern has a minimum-digit requirement. Verify:
        assert "52079950" not in r.text

    def test_diagnostic_strings_survive(self):
        r = redact(self.LOG)
        assert "vkCreateInstance failed" in r.text
        assert "VK_ERROR_INCOMPATIBLE_DRIVER" in r.text
        assert "Proton 8.0-4" in r.text
        assert "DXVK: v2.3.1" in r.text
        assert "AppID 1091500" in r.text
        assert "Cyberpunk 2077" in r.text

    def test_path_structure_preserved(self):
        r = redact(self.LOG)
        # The Steam path structure after the username is diagnostic
        assert ".steam/steam/steamapps/common/Cyberpunk 2077/bin/x64/" in r.text
        assert "localconfig.vdf" in r.text
