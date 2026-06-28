"""
PII redactor for anonymous log submissions.

Scrubs personally-identifiable information from Proton/Steam/Wine gaming logs
before they are stored in the submissions table.

Design goals
  - Non-destructive to diagnostic value: fingerprint-relevant strings survive
  - Labeled replacements: [USERNAME], [IP_ADDRESS], etc., not blank erasures
  - Auditable: every substitution is counted per-category and returned in the report
  - Conservative on ambiguous patterns (prefer a miss over a false positive)

Application order
  1. Filesystem paths  — most specific; run first to avoid partial re-matching
  2. Account IDs       — Steam IDs, Windows SIDs, email
  3. Hardware/network  — UUIDs, MAC, IPv4, IPv6
  4. Keyword-anchored  — hostname keyword; least specific, run last
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ── Why each category is sensitive ──────────────────────────────────────────

REASONS: dict[str, str] = {
    "linux_home_path": (
        "Linux /home/<user>/ paths expose the OS account name used to run Steam"
    ),
    "macos_home_path": (
        "macOS /Users/<user>/ paths expose the OS account name"
    ),
    "windows_user_path": (
        "Windows C:\\Users\\<user>\\ paths expose the Windows account name"
    ),
    "wine_z_path": (
        "Wine's Z: drive maps the Linux root; Z:\\home\\<user>\\ reveals the OS username"
    ),
    "steam_id64": (
        "SteamID64 is a permanent, globally unique identifier for a Steam account"
    ),
    "steam_id3": (
        "SteamID3 [U:1:XXXXXXX] uniquely identifies a Steam account"
    ),
    "steam_userdata_id": (
        "The numeric folder under Steam's userdata/ directory is a per-account identifier"
    ),
    "ip_address_v4": (
        "IPv4 addresses identify the machine or network; home IPs are tied to real locations"
    ),
    "ip_address_v6": (
        "IPv6 EUI-64 addresses embed the device's MAC address, directly identifying hardware"
    ),
    "email_address": (
        "Email addresses directly identify the user"
    ),
    "uuid": (
        "UUIDs in hardware or installation contexts uniquely identify the machine"
    ),
    "mac_address": (
        "MAC addresses permanently and uniquely identify a physical network adapter"
    ),
    "windows_sid": (
        "Windows Security Identifiers (SIDs) uniquely identify a Windows account across systems"
    ),
    "uid_gid_info": (
        "uid=N(name) / gid=N(name) entries expose both the numeric UID and the OS username"
    ),
    "run_user_path": (
        "/run/user/<UID>/ paths expose the numeric UID of the logged-in account"
    ),
    "media_mount_path": (
        "/media/<user>/ mount paths expose the OS username (Ubuntu/Debian removable media convention)"
    ),
    "hostname_keyword": (
        "Machine hostnames expose the device's network identity and may be used to fingerprint it"
    ),
}


# ── Result type ──────────────────────────────────────────────────────────────

@dataclass
class RedactionResult:
    text: str
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(self.counts.values())

    @property
    def was_redacted(self) -> bool:
        return self.total > 0

    def report(self) -> dict:
        return {
            "was_redacted": self.was_redacted,
            "total_redactions": self.total,
            "by_category": {
                cat: {
                    "count": count,
                    "reason": REASONS.get(cat, "Potentially identifying information"),
                }
                for cat, count in sorted(self.counts.items())
                if count > 0
            },
        }


# ── Helper ───────────────────────────────────────────────────────────────────

def _apply(
    pattern: re.Pattern,
    replacement: str,
    text: str,
    counts: dict[str, int],
    category: str,
) -> str:
    result, n = pattern.subn(replacement, text)
    if n:
        counts[category] = counts.get(category, 0) + n
    return result


# ── Compiled patterns ────────────────────────────────────────────────────────

# Phase 1 — filesystem paths
# Must run in this order: Wine Z: before Linux /home (to avoid double-match),
# and all path rules before identifier rules.

# Wine Z:\home\<user>\ or Z:/home/<user>/
# Groups: 1=Z:separator, 2=home separator, 3=username, 4=trailing separator
_RE_WINE_Z = re.compile(
    r'([Zz]:[/\\])home([/\\])([a-zA-Z0-9_.-]{1,64})([/\\])'
)

# Linux /home/<user>/
_RE_LINUX_HOME = re.compile(r'/home/([a-zA-Z0-9_.-]{1,64})/')

# macOS /Users/<user>/
_RE_MACOS_HOME = re.compile(r'/Users/([a-zA-Z0-9_.-]{1,64})/')

# Windows C:\Users\<user>\  (any drive letter, case-insensitive)
# Groups: 1=drive+\Users\, 2=username, 3=trailing backslash
_RE_WIN_HOME = re.compile(
    r'([A-Za-z]:\\Users\\)([^\\/:*?"<>|\r\n]{1,64})(\\)',
    re.IGNORECASE,
)

# Steam userdata/<account_id>/ (7–12 digit account folder)
# Groups: 1=userdata/, 2=account_id, 3=trailing separator
_RE_STEAM_USERDATA = re.compile(r'(userdata[/\\])(\d{4,12})([/\\])')

# /run/user/<UID>/
_RE_RUN_USER = re.compile(r'/run/user/(\d+)/')

# /media/<username>/  (Ubuntu/Debian removable media mounts)
_RE_MEDIA = re.compile(r'/media/([a-zA-Z0-9_.-]{1,64})/')


# Phase 2 — account identifiers

# SteamID64: 17 digits starting with 7656 (universe + type + instance bits)
_RE_STEAMID64 = re.compile(r'\b7656\d{13}\b')

# SteamID3: [U:1:XXXXXXXXX]
_RE_STEAMID3 = re.compile(r'\[U:1:\d{1,10}\]')

# Email addresses
_RE_EMAIL = re.compile(
    r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b'
)

# Windows SID: S-1-<authority>-<sub>[-<sub>...]
_RE_WIN_SID = re.compile(r'\bS-1-[0-9]+-\d+(?:-\d+){1,9}\b')

# uid=N(name) and gid=N(name) process/file ownership strings
# Group 1: uid|gid keyword (preserved in replacement)
_RE_UID_GID = re.compile(r'\b(uid|gid)=\d+\([a-zA-Z0-9_.-]+\)')


# Phase 3 — hardware / network identifiers

# Standard UUID: 8-4-4-4-12 hex groups
_RE_UUID = re.compile(
    r'\b[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}'
    r'-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\b'
)

# MAC address: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX (consistent separator)
_RE_MAC = re.compile(
    r'\b(?:(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'
    r'|(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2})\b'
)

# Raw IPv4 capture groups for octet validation (see _redact_ipv4)
_RE_IPV4_RAW = re.compile(
    r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b'
)

# IPv6 — full 8-group form only; avoids false positives from compressed forms
_RE_IPV6 = re.compile(
    r'\b[0-9A-Fa-f]{1,4}(?::[0-9A-Fa-f]{1,4}){7}\b'
)


# Phase 4 — keyword-anchored patterns

# hostname= or hostname: followed by the value
# Group 1: keyword + separator (preserved), Group 2: hostname value (redacted)
_RE_HOSTNAME_KW = re.compile(
    r'(hostname\s*[=:]\s*)(\S+)',
    re.IGNORECASE,
)


# ── IPv4 with octet validation ───────────────────────────────────────────────

def _redact_ipv4(text: str, counts: dict[str, int]) -> str:
    """Replace IPv4 addresses only when all four octets are 0–255.

    This prevents false positives on three-component version strings
    like "10.0.22000" (Windows build) or "2.3.1" (DXVK version) —
    those have fewer than four dot-separated components and will not
    match the four-group pattern at all.  The octet check is a
    secondary guard against things like "999.999.999.999".
    """
    def _replace(m: re.Match) -> str:
        if all(0 <= int(m.group(i)) <= 255 for i in range(1, 5)):
            counts["ip_address_v4"] = counts.get("ip_address_v4", 0) + 1
            return "[IP_ADDRESS]"
        return m.group(0)

    return _RE_IPV4_RAW.sub(_replace, text)


# ── Public API ───────────────────────────────────────────────────────────────

def redact(log_text: str) -> RedactionResult:
    """Redact PII from *log_text* and return the scrubbed text plus a hit report."""
    counts: dict[str, int] = {}
    t = log_text

    # Phase 1 — paths
    t = _apply(_RE_WINE_Z,          r'\1home\2[USERNAME]\4', t, counts, "wine_z_path")
    t = _apply(_RE_LINUX_HOME,      '/home/[USERNAME]/',     t, counts, "linux_home_path")
    t = _apply(_RE_MACOS_HOME,      '/Users/[USERNAME]/',    t, counts, "macos_home_path")
    t = _apply(_RE_WIN_HOME,        r'\1[USERNAME]\3',       t, counts, "windows_user_path")
    t = _apply(_RE_STEAM_USERDATA,  r'\1[STEAM_ACCT_ID]\3', t, counts, "steam_userdata_id")
    t = _apply(_RE_RUN_USER,        '/run/user/[UID]/',      t, counts, "run_user_path")
    t = _apply(_RE_MEDIA,           '/media/[USERNAME]/',    t, counts, "media_mount_path")

    # Phase 2 — account identifiers
    t = _apply(_RE_STEAMID64,  '[STEAM_ID64]',           t, counts, "steam_id64")
    t = _apply(_RE_STEAMID3,   '[STEAM_ID3]',            t, counts, "steam_id3")
    t = _apply(_RE_EMAIL,      '[EMAIL]',                 t, counts, "email_address")
    t = _apply(_RE_WIN_SID,    '[WINDOWS_SID]',           t, counts, "windows_sid")
    t = _apply(_RE_UID_GID,    r'\1=[UID]([USERNAME])',   t, counts, "uid_gid_info")

    # Phase 3 — hardware / network
    t = _apply(_RE_UUID,       '[UUID]',                  t, counts, "uuid")
    t = _apply(_RE_MAC,        '[MAC_ADDRESS]',           t, counts, "mac_address")
    t = _redact_ipv4(t, counts)
    t = _apply(_RE_IPV6,       '[IP_ADDRESS_V6]',         t, counts, "ip_address_v6")

    # Phase 4 — keyword-anchored
    t = _apply(_RE_HOSTNAME_KW, r'\1[HOSTNAME]',          t, counts, "hostname_keyword")

    return RedactionResult(text=t, counts=counts)
