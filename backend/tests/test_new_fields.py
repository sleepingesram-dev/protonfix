"""
Tests for newly parsed fields in parser.py.
One representative log per field — logs are minimal but match real Proton/Steam/DXVK output.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser import parse_log


# ---------- exit_code ----------

LOG_EXIT_DECIMAL = """\
Game: Elden Ring
AppID: 1245620
Proton: 9.0-3

err:   VK_ERROR_DEVICE_LOST

Game exited with status 1
"""

LOG_EXIT_HEX = """\
Game: Cyberpunk 2077
AppID: 1091500
Proton: 9.0-3

err:seh:setup_exception stack overflow

Game exited with code 0xc0000005
"""

LOG_EXIT_CLEAN = """\
Game: Stardew Valley
AppID: 413150
Proton: 9.0-3

Game exited with status 0
"""

# ---------- launch_options ----------

LOG_LAUNCH_GAMESCOPE = """\
Game: Counter-Strike 2
AppID: 730
Proton: 10.0-1

fsync: up and running.

Game process removed: AppID 730 "gamemoderun gamescope -f -W 2560 -H 1440 -- %command%", ProcID 4321
"""

LOG_LAUNCH_SIMPLE = """\
Game: Hollow Knight
AppID: 367520
Proton: 9.0-3

fsync: up and running.

Game process removed: AppID 367520 "%command%", ProcID 9900
"""

# ---------- sync_method ----------

LOG_FSYNC = """\
Game: Death Stranding
AppID: 1850570
Proton: 10.0-1

fsync: up and running.
wine: RLIMIT_NICE is <= 20, unable to use setpriority safely
"""

LOG_ESYNC = """\
Game: Death Stranding
AppID: 1850570
Proton: 8.0-5

esync: up and running.
wine: RLIMIT_NICE is <= 20, unable to use setpriority safely
"""

LOG_NO_SYNC = """\
Game: Old Wine Title
AppID: 9999
Proton: 5.0-10

wine: RLIMIT_NICE is <= 20, unable to use setpriority safely
"""

# ---------- session_type + display_server ----------

LOG_WAYLAND = """\
Game: THE FINALS
AppID: 2073850
Proton: GE-Proton10-34
Session: KDE Wayland

fsync: up and running.
"""

LOG_X11 = """\
Game: Team Fortress 2
AppID: 440
Proton: 9.0-3
Session: GNOME X11

fsync: up and running.
"""

# ---------- kernel_version ----------

LOG_KERNEL = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1
Kernel: 7.0.10-cachyos

err:   VK_ERROR_INCOMPATIBLE_DRIVER
Game exited with status 1
"""

LOG_KERNEL_LINUX_VERSION = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1

Linux version 6.8.0-49-generic (buildd@lcy02-amd64-019) (gcc-13)

err:   VK_ERROR_INCOMPATIBLE_DRIVER
"""

# ---------- driver_version ----------

LOG_DRIVER_HEADER = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1
GPU: AMD Radeon RX 7800 XT
Driver: Mesa 24.1.0 / RADV
Kernel: 7.0.10-cachyos

err:   VK_ERROR_INCOMPATIBLE_DRIVER
"""

# ---------- vulkan_driver_version ----------

LOG_VK_ADAPTER_AMD = """\
Game: Elden Ring
AppID: 1245620
Proton: 10.0-1
GPU: AMD Radeon RX 7900 XTX

info:  DXVK: v2.6
info:  Vulkan: Found 2 adapter(s)
info:    [0] AMD Radeon RX 7900 XTX (RADV NAVI31) : Vulkan 1.3 [24.1.0.0]
info:    [1] llvmpipe (LLVM 17.0.6, 256 bits) : Vulkan 1.0 [0.0.1]
info:  Using adapter: AMD Radeon RX 7900 XTX (RADV NAVI31)
info:  D3D11_FEATURE_LEVEL_12_1
"""

LOG_VK_ADAPTER_NVIDIA = """\
Game: Cyberpunk 2077
AppID: 1091500
Proton: 10.0-1
GPU: NVIDIA GeForce RTX 4090

info:  DXVK: v2.6
info:  Vulkan: Found 1 adapter(s)
info:    [0] NVIDIA GeForce RTX 4090 (NVIDIA) : Vulkan 1.3 [545.29.6]
info:  Using adapter: NVIDIA GeForce RTX 4090 (NVIDIA)
info:  D3D11_FEATURE_LEVEL_12_1
"""

# ---------- prefix_action ----------

LOG_PREFIX_UPGRADED = """\
Game: Cyberpunk 2077
AppID: 1091500
Proton: 10.0-1

fsync: up and running.
Proton: Upgrading prefix from 9.0-3 to 10.0-1
wine: using kernel write watches, use_kernel_writewatch 1
"""

LOG_PREFIX_CREATED = """\
Game: New Game First Launch
AppID: 9999999
Proton: 10.0-1

fsync: up and running.
Proton: Creating prefix /home/user/.steam/steam/steamapps/compatdata/9999999/pfx
wine: using kernel write watches, use_kernel_writewatch 1
"""

LOG_PREFIX_FROM_NONE = """\
Game: THE FINALS
AppID: 2073850
Proton: GE-Proton10-34

fsync: up and running.
Proton: Upgrading prefix from None to GE-Proton10-34
"""

# ---------- game_exe ----------

LOG_GAME_EXE = """\
Game: Apex Legends
AppID: 1172470
Proton: 10.0-1

info:  Game: r5apex.exe
info:  DXVK: v2.6
info:  VKD3D-Proton: v2.14

err:   VK_ERROR_INCOMPATIBLE_DRIVER
"""

# ---------- gamescope_version ----------

LOG_GAMESCOPE_VERSION = """\
Game: THE FINALS
AppID: 2073850
Proton: GE-Proton10-34
Session: KDE Wayland

[gamescope] [Info]  console: gamescope version 3.16.23
[gamescope] [Info]  vulkan: selecting physical device 'AMD Radeon RX 7800 XT (RADV NAVI32)'
[gamescope] [Error] vulkan: vkCreateDevice failed (VK_ERROR_EXTENSION_NOT_PRESENT)
"""

# ---------- dx_level ----------

LOG_DX11 = """\
Game: Elden Ring
AppID: 1245620
Proton: 10.0-1

info:  DXVK: v2.6
info:  D3D11_FEATURE_LEVEL_12_1
"""

LOG_DX12 = """\
Game: Cyberpunk 2077
AppID: 1091500
Proton: 10.0-1

info:  VKD3D-Proton: v2.14
info:  vkd3d: D3D_FEATURE_LEVEL_12_1
"""

# ---------- proton_version fix: must not capture "Upgrading prefix" line ----------

LOG_PROTON_VERSION_NO_HEADER = """\
Game: Some Game
AppID: 111111

fsync: up and running.
Proton: Upgrading prefix from None to GE-Proton10-34
"""


# ============================================================
# Tests
# ============================================================

def check(field, expected, log, label):
    result = parse_log(log)
    got = result.get(field)
    ok = got == expected
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    if not ok:
        print(f"         expected {field}={expected!r}, got {got!r}")
    return ok


def run():
    failures = 0
    total = 0

    cases = [
        # exit_code
        ("exit_code", 1,          LOG_EXIT_DECIMAL,        "exit_code decimal 1"),
        ("exit_code", 0xc0000005, LOG_EXIT_HEX,            "exit_code hex 0xc0000005"),
        ("exit_code", 0,          LOG_EXIT_CLEAN,          "exit_code 0 (clean)"),

        # launch_options
        ("launch_options", "gamemoderun gamescope -f -W 2560 -H 1440 -- %command%",
         LOG_LAUNCH_GAMESCOPE,   "launch_options gamescope"),
        ("launch_options", "%command%",
         LOG_LAUNCH_SIMPLE,      "launch_options simple"),

        # sync_method
        ("sync_method", "fsync",  LOG_FSYNC,               "sync_method fsync"),
        ("sync_method", "esync",  LOG_ESYNC,               "sync_method esync"),
        ("sync_method", None,     LOG_NO_SYNC,             "sync_method None"),

        # session_type + display_server
        ("session_type",    "KDE Wayland",  LOG_WAYLAND,   "session_type KDE Wayland"),
        ("display_server",  "wayland",      LOG_WAYLAND,   "display_server wayland"),
        ("session_type",    "GNOME X11",    LOG_X11,       "session_type GNOME X11"),
        ("display_server",  "x11",          LOG_X11,       "display_server x11"),

        # kernel_version
        ("kernel_version", "7.0.10-cachyos",           LOG_KERNEL,              "kernel_version from Kernel: header"),
        ("kernel_version", "6.8.0-49-generic",         LOG_KERNEL_LINUX_VERSION,"kernel_version from Linux version line"),

        # driver_version
        ("driver_version", "Mesa 24.1.0 / RADV",       LOG_DRIVER_HEADER,       "driver_version from Driver: header"),

        # vulkan_driver_version
        ("vulkan_driver_version", "24.1.0.0",           LOG_VK_ADAPTER_AMD,      "vulkan_driver_version AMD"),
        ("vulkan_driver_version", "545.29.6",           LOG_VK_ADAPTER_NVIDIA,   "vulkan_driver_version NVIDIA"),

        # prefix_action
        ("prefix_action",       "upgraded",  LOG_PREFIX_UPGRADED,     "prefix_action upgraded"),
        ("prefix_upgrade_from", "9.0-3",     LOG_PREFIX_UPGRADED,     "prefix_upgrade_from version"),
        ("prefix_action",       "created",   LOG_PREFIX_CREATED,      "prefix_action created"),
        ("prefix_action",       "upgraded",  LOG_PREFIX_FROM_NONE,    "prefix_action upgraded from None"),
        ("prefix_upgrade_from", None,        LOG_PREFIX_FROM_NONE,    "prefix_upgrade_from None → None"),

        # game_exe
        ("game_exe", "r5apex.exe",     LOG_GAME_EXE,            "game_exe from DXVK info block"),

        # gamescope_version
        ("gamescope_version", "3.16.23", LOG_GAMESCOPE_VERSION,  "gamescope_version"),

        # dx_level
        ("dx_level", "D3D11_FEATURE_LEVEL_12_1", LOG_DX11,       "dx_level D3D11"),
        ("dx_level", "D3D_FEATURE_LEVEL_12_1",   LOG_DX12,       "dx_level VKD3D D3D12"),

        # proton_version fix
        ("proton_version", None,   LOG_PROTON_VERSION_NO_HEADER, "proton_version not captured from Upgrading line"),

        # DXVK also sets dx_level and vulkan_driver_version in the same log
        ("dx_level",               "D3D11_FEATURE_LEVEL_12_1", LOG_VK_ADAPTER_AMD, "dx_level from combined AMD log"),
        ("vulkan_driver_version",  "545.29.6",                 LOG_VK_ADAPTER_NVIDIA, "vk_driver_version in NVIDIA dx log"),
    ]

    print(f"Running {len(cases)} field extraction tests...\n")
    for field, expected, log, label in cases:
        total += 1
        if not check(field, expected, log, label):
            failures += 1

    print(f"\n{'='*50}")
    print(f"Results: {total - failures}/{total} passed", "✓" if not failures else "✗")
    return failures


if __name__ == "__main__":
    sys.exit(run())
