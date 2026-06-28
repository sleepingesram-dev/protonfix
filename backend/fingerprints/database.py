ERROR_PATTERNS = {
    "VK_ERROR_INCOMPATIBLE_DRIVER": {
        "fingerprint": "VULKAN_DRIVER_MISSING",
        "category": "Graphics Driver",
        "severity": "high",
        "explanation": "The system could not create a Vulkan device because the Vulkan driver is missing, broken, or incompatible.",
        "known_fix": [
            "Install or reinstall the correct Vulkan driver for your GPU.",
            "For AMD GPUs on Arch/CachyOS, install mesa, vulkan-radeon, and vulkan-tools.",
            "Reboot after installing GPU or Vulkan packages.",
            "Run vulkaninfo to confirm Vulkan works."
        ],
        "safe_commands": [
            "sudo pacman -Syu mesa vulkan-radeon vulkan-tools",
            "vulkaninfo"
        ],
    },

    "Failed to create Vulkan instance": {
        "fingerprint": "VULKAN_INIT_FAILURE",
        "category": "Graphics Driver",
        "severity": "high",
        "explanation": "The game or compatibility layer failed to initialize Vulkan.",
        "known_fix": [
            "Check that Vulkan packages are installed.",
            "Check that the correct GPU driver is active.",
            "Run vulkaninfo and check for errors."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "DXGI: Failed to initialize adapter": {
        "fingerprint": "DXVK_ADAPTER_FAILURE",
        "category": "DXVK",
        "severity": "high",
        "explanation": "DXVK could not create or access a usable graphics adapter.",
        "known_fix": [
            "Fix Vulkan first because DXVK depends on Vulkan.",
            "Confirm the GPU is detected correctly.",
            "Update Mesa and Vulkan packages."
        ],
        "safe_commands": [
            "vulkaninfo",
            "lspci | grep -E 'VGA|3D|Display'"
        ],
    },

    "Unhandled page fault": {
        "fingerprint": "WINE_CRASH",
        "category": "Wine",
        "severity": "medium",
        "explanation": "Wine crashed while the game was running or starting.",
        "known_fix": [
            "Fix earlier graphics or runtime errors first.",
            "Try a different Proton version if the graphics stack is working.",
            "Check whether the game is currently compatible with Proton."
        ],
        "safe_commands": [],
    },

    "EasyAntiCheat": {
        "fingerprint": "EAC_FAILURE",
        "category": "Anti-Cheat",
        "severity": "high",
        "explanation": "Easy Anti-Cheat failed to initialize or blocked the game from launching.",
        "known_fix": [
            "Verify the game files in Steam.",
            "Check whether the game officially supports Proton/Linux anti-cheat.",
            "Try a supported Proton version recommended by ProtonDB.",
            "Do not waste time changing graphics settings until anti-cheat is confirmed working."
        ],
        "safe_commands": [],
    },

    "BattlEye": {
        "fingerprint": "BATTLEYE_FAILURE",
        "category": "Anti-Cheat",
        "severity": "high",
        "explanation": "BattlEye failed to initialize or blocked the game from launching.",
        "known_fix": [
            "Verify the game files in Steam.",
            "Check whether the game supports BattlEye through Proton.",
            "Try launching with a clean Proton prefix.",
            "Check ProtonDB for current compatibility reports."
        ],
        "safe_commands": [],
    },

        "vkCreateDevice failed": {
        "fingerprint": "GAMESCOPE_VULKAN_INIT_FAILURE",
        "category": "Gamescope",
        "severity": "high",
        "explanation": "Gamescope failed while creating a Vulkan device.",
        "known_fix": [
            "Update Gamescope and your Vulkan drivers.",
            "Check that required Vulkan extensions are available.",
            "Try launching the game without Gamescope.",
            "Run vulkaninfo and check for Vulkan driver errors.",
        ],
        "safe_commands": [
            "vulkaninfo",
            "gamescope --version",
        ],
    },

    "VK_ERROR_EXTENSION_NOT_PRESENT": {
        "fingerprint": "VK_ERROR_EXTENSION_NOT_PRESENT",
        "category": "Vulkan",
        "severity": "high",
        "explanation": "A required Vulkan extension is missing or unavailable.",
        "known_fix": [
            "Update Mesa, Vulkan drivers, and Gamescope.",
            "Confirm the correct Vulkan ICD is being used.",
            "Try launching without Gamescope to isolate whether Gamescope is the trigger.",
            "Check whether your GPU driver supports the required Vulkan extension.",
        ],
        "safe_commands": [
            "vulkaninfo",
            "ls /usr/share/vulkan/icd.d/",
        ],
    },

    "Failed to initialize Vulkan": {
        "fingerprint": "GAMESCOPE_VULKAN_INIT_FAILURE",
        "category": "Gamescope",
        "severity": "high",
        "explanation": "Gamescope could not initialize Vulkan.",
        "known_fix": [
            "Verify Vulkan works outside the game.",
            "Update Mesa and Vulkan packages.",
            "Try running the game without Gamescope.",
            "Check whether the issue happens on X11 and Wayland.",
        ],
        "safe_commands": [
            "vulkaninfo",
        ],
    },

    "Failed to create swapchain": {
        "fingerprint": "GAMESCOPE_SWAPCHAIN_FAILURE",
        "category": "Gamescope",
        "severity": "high",
        "explanation": "Gamescope failed to create a Vulkan swapchain, which prevents rendering output.",
        "known_fix": [
            "Update Gamescope and Vulkan drivers.",
            "Try disabling Gamescope for this launch.",
            "Check display mode, refresh rate, HDR, VRR, and fullscreen settings.",
            "Try a simpler Gamescope launch configuration.",
        ],
        "safe_commands": [
            "gamescope --version",
            "vulkaninfo",
        ],
    },

    "Failed to create gamescope output": {
        "fingerprint": "GAMESCOPE_OUTPUT_FAILURE",
        "category": "Gamescope",
        "severity": "high",
        "explanation": "Gamescope failed to create its display output.",
        "known_fix": [
            "Try launching the game without Gamescope.",
            "Check whether Gamescope works with another game.",
            "Update Gamescope, Mesa, and Vulkan packages.",
            "Try switching between Wayland and X11 to compare behavior.",
        ],
        "safe_commands": [
            "gamescope --version",
            "echo $XDG_SESSION_TYPE",
        ],
    },

    "DxvkAdapter: Failed to initialize adapter": {
        "fingerprint": "DXVK_ADAPTER_FAILURE",
        "category": "DXVK",
        "severity": "high",
        "explanation": "DXVK could not initialize a usable graphics adapter.",
        "known_fix": [
            "Fix Vulkan first because DXVK depends on Vulkan.",
            "Confirm the GPU is detected correctly.",
            "Update Mesa and Vulkan packages.",
            "Run vulkaninfo and check for errors.",
        ],
        "safe_commands": [
            "vulkaninfo",
            "lspci | grep -E 'VGA|3D|Display'",
        ],
    },

    "gamemode request failed": {
        "fingerprint": "GAMEMODE_REQUEST_FAILURE",
        "category": "GameMode",
        "severity": "low",
        "explanation": "The game or launcher requested GameMode, but the request failed.",
        "known_fix": [
            "Install GameMode if it is missing.",
            "Make sure the GameMode daemon is available.",
            "This usually affects performance tuning, not whether the game can launch.",
        ],
        "safe_commands": [
            "gamemoded -s",
            "systemctl --user status gamemoded",
        ],
    },

    "com.feralinteractive.GameMode was not provided by any .service files": {
        "fingerprint": "GAMEMODE_DAEMON_RELATED",
        "category": "GameMode",
        "severity": "low",
        "explanation": "The GameMode D-Bus service is missing or unavailable.",
        "known_fix": [
            "Install the GameMode package.",
            "Restart the user session after installing GameMode.",
            "Do not treat this as the main launch failure unless no other fatal errors exist.",
        ],
        "safe_commands": [
            "gamemoded -s",
            "systemctl --user status gamemoded",
        ],
    },

    "MANGOHUD: Failed to load preset": {
        "fingerprint": "MANGOHUD_CONFIG_RELATED",
        "category": "MangoHud",
        "severity": "low",
        "explanation": "MangoHud could not load a configured preset or config file.",
        "known_fix": [
            "Check whether the MangoHud config file exists.",
            "Remove the custom MangoHud preset if it is broken.",
            "This is usually cosmetic and should not be treated as the main launch failure.",
        ],
        "safe_commands": [
            "ls ~/.config/MangoHud/",
            "mangohud --version",
        ],
    },

    "gamescope": {
        "fingerprint": "GAMESCOPE_FAILURE",
        "category": "Gamescope",
        "severity": "medium",
        "explanation": "Gamescope appears in the log and may be involved in the launch failure.",
        "known_fix": [
            "Disable Gamescope temporarily.",
            "Remove Gamescope launch options and test again.",
            "Update Gamescope.",
            "If the game launches without Gamescope, re-add Gamescope options one at a time."
        ],
        "safe_commands": [],
    },

    "MangoHud": {
        "fingerprint": "MANGOHUD_FAILURE",
        "category": "Performance Overlay",
        "severity": "low",
        "explanation": "MangoHud appears in the log and may be causing overlay or launch issues.",
        "known_fix": [
            "Disable MangoHud temporarily.",
            "Remove MANGOHUD=1 from launch options.",
            "Update MangoHud.",
            "Test the game without overlays."
        ],
        "safe_commands": [],
    },

    "steam-runtime": {
        "fingerprint": "STEAM_RUNTIME_FAILURE",
        "category": "Steam Runtime",
        "severity": "high",
        "explanation": "Steam Runtime appears to have failed or caused a launch environment problem.",
        "known_fix": [
            "Restart Steam.",
            "Update Steam.",
            "Verify the game's files.",
            "Try switching between Steam Linux Runtime and native runtime if applicable."
        ],
        "safe_commands": [],
    },

    "No such file or directory": {
        "fingerprint": "MISSING_FILE",
        "category": "Missing File",
        "severity": "medium",
        "explanation": "The log references a file or path that does not exist.",
        "known_fix": [
            "Verify the game files.",
            "Check whether the missing path belongs to a mod, launcher, or dependency.",
            "Remove broken launch options that point to missing files."
        ],
        "safe_commands": [],
    },

    "permission denied": {
        "fingerprint": "PERMISSION_DENIED",
        "category": "Permissions",
        "severity": "medium",
        "explanation": "The game or launcher tried to access something without permission.",
        "known_fix": [
            "Check file permissions.",
            "Avoid running Steam as root.",
            "Make sure the game folder is owned by your user.",
            "If the game is on another drive, check mount permissions."
        ],
        "safe_commands": [
            "ls -la"
        ],
    },

    "disk write error": {
        "fingerprint": "STEAM_DISK_WRITE_ERROR",
        "category": "Steam Storage",
        "severity": "medium",
        "explanation": "Steam could not write files to the game install location.",
        "known_fix": [
            "Check free disk space.",
            "Check permissions on the Steam library folder.",
            "Restart Steam.",
            "Repair the Steam library folder."
        ],
        "safe_commands": [
            "df -h"
        ],
    },

    "out of memory": {
        "fingerprint": "OUT_OF_MEMORY",
        "category": "Memory",
        "severity": "high",
        "explanation": "The game or compatibility layer may have crashed due to memory pressure.",
        "known_fix": [
            "Close background apps.",
            "Lower texture quality or memory-heavy settings.",
            "Check RAM and swap usage.",
            "Try launching the game again after a reboot."
        ],
        "safe_commands": [
            "free -h"
        ],
    },

    "vkd3d": {
        "fingerprint": "VKD3D_RELATED_FAILURE",
        "category": "VKD3D",
        "severity": "medium",
        "explanation": "The log references VKD3D, which handles DirectX 12 translation through Vulkan.",
        "known_fix": [
            "Update Proton.",
            "Update Mesa and Vulkan drivers.",
            "Try Proton Experimental or GE-Proton.",
            "Check whether the game has known DirectX 12 issues on Proton."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "DXVK": {
        "fingerprint": "DXVK_RELATED_FAILURE",
        "category": "DXVK",
        "severity": "medium",
        "explanation": "The log references DXVK, which handles DirectX 9/10/11 translation through Vulkan.",
        "known_fix": [
            "Update Proton.",
            "Update Mesa and Vulkan drivers.",
            "Check Vulkan support with vulkaninfo.",
            "Try a different Proton version."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "Proton: Experimental": {
        "fingerprint": "PROTON_EXPERIMENTAL_USED",
        "category": "Proton Version",
        "severity": "low",
        "explanation": "The game is using Proton Experimental.",
        "known_fix": [
            "If the game fails, test a stable Proton version.",
            "If the stable version fails, test GE-Proton.",
            "Only change one Proton version at a time so results are clear."
        ],
        "safe_commands": [],
    },

    "GE-Proton": {
        "fingerprint": "GE_PROTON_USED",
        "category": "Proton Version",
        "severity": "low",
        "explanation": "The game is using GE-Proton.",
        "known_fix": [
            "If launch fails, test Proton Experimental.",
            "Try the latest GE-Proton version.",
            "Check whether the game has a recommended Proton version on ProtonDB."
        ],
        "safe_commands": [],
    },

    "gamemode": {
        "fingerprint": "GAMEMODE_RELATED",
        "category": "GameMode",
        "severity": "low",
        "explanation": "GameMode appears in the log and may be related to launch or performance behavior.",
        "known_fix": [
            "Disable GameMode temporarily.",
            "Test the game without gamemoderun.",
            "If the game launches without it, troubleshoot GameMode separately."
        ],
        "safe_commands": [
            "gamemoded -s"
        ],
    },

    "pkexec": {
        "fingerprint": "PKEXEC_PERMISSION_ISSUE",
        "category": "Permissions",
        "severity": "medium",
        "explanation": "pkexec appears in the log, which may indicate an authorization or permission problem.",
        "known_fix": [
            "Check whether the app is trying to run privileged commands.",
            "Do not run Steam or games as root.",
            "Fix the permission issue directly instead of granting broad privileges."
        ],
        "safe_commands": [],
    },

    "segmentation fault": {
        "fingerprint": "SEGFAULT",
        "category": "Crash",
        "severity": "medium",
        "explanation": "The game or compatibility layer crashed with a segmentation fault.",
        "known_fix": [
            "Check earlier errors in the log first.",
            "Try a different Proton version.",
            "Disable overlays and launch options.",
            "Verify game files."
        ],
        "safe_commands": [],
    },

    "core dumped": {
        "fingerprint": "CORE_DUMPED",
        "category": "Crash",
        "severity": "medium",
        "explanation": "The game or a related process crashed and produced a core dump.",
        "known_fix": [
            "Check the first error that appears before the crash.",
            "Try disabling overlays.",
            "Try another Proton version.",
            "Verify game files."
        ],
        "safe_commands": [],
    },

        "wineboot failed": {
        "fingerprint": "PROTON_WINEBOOT_FAILURE",
        "category": "Proton Prefix",
        "severity": "high",
        "explanation": "Wineboot failed while setting up or updating the Proton prefix.",
        "known_fix": [
            "The Proton prefix may be corrupted or incomplete.",
            "Try switching Proton versions once.",
            "If the issue continues, rebuild the game's Proton prefix.",
            "Verify game files after rebuilding the prefix."
        ],
        "safe_commands": [],
    },

    "failed to open dll": {
        "fingerprint": "PROTON_DLL_MISSING",
        "category": "Proton Dependency",
        "severity": "medium",
        "explanation": "Proton or Wine tried to load a DLL that could not be opened.",
        "known_fix": [
            "Verify the game files in Steam.",
            "Check whether the missing DLL belongs to the game, a launcher, or a mod.",
            "Try a clean Proton prefix.",
            "Avoid manually downloading random DLL files from the internet."
        ],
        "safe_commands": [],
    },

    "ntdll": {
        "fingerprint": "NTDLL_RELATED_CRASH",
        "category": "Wine",
        "severity": "medium",
        "explanation": "The crash references ntdll, a core Wine/Windows compatibility component.",
        "known_fix": [
            "Look for earlier errors before the ntdll crash.",
            "Try a different Proton version.",
            "Disable overlays and launch options.",
            "Verify game files."
        ],
        "safe_commands": [],
    },

    "amdgpu: gpu reset": {
        "fingerprint": "AMDGPU_RESET",
        "category": "AMD Driver",
        "severity": "high",
        "explanation": "The AMD GPU driver reported a GPU reset, usually caused by a driver crash, unstable settings, or a Vulkan failure.",
        "known_fix": [
            "Update Mesa and Vulkan packages.",
            "Remove GPU overclocks or undervolts while testing.",
            "Reboot after driver updates.",
            "Check whether the crash happens in other Vulkan games."
        ],
        "safe_commands": [
            "sudo pacman -Syu mesa vulkan-radeon lib32-vulkan-radeon",
            "journalctl -k | grep -i amdgpu"
        ],
    },

    "ring gfx timeout": {
        "fingerprint": "AMDGPU_RING_TIMEOUT",
        "category": "AMD Driver",
        "severity": "high",
        "explanation": "The AMD graphics ring timed out, which usually means the GPU driver hung.",
        "known_fix": [
            "Update Mesa and the Linux kernel.",
            "Remove overclocks or undervolts.",
            "Test without Gamescope or overlays.",
            "Check kernel logs for amdgpu errors."
        ],
        "safe_commands": [
            "journalctl -k | grep -i amdgpu"
        ],
    },

    "radv": {
        "fingerprint": "RADV_RELATED_FAILURE",
        "category": "AMD Vulkan",
        "severity": "medium",
        "explanation": "The log references RADV, the Mesa Vulkan driver for AMD GPUs.",
        "known_fix": [
            "Update Mesa and Vulkan packages.",
            "Check Vulkan with vulkaninfo.",
            "Try disabling experimental Vulkan options.",
            "Make sure the system is not using the wrong Vulkan ICD."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "nvidia driver": {
        "fingerprint": "NVIDIA_DRIVER_RELATED",
        "category": "NVIDIA Driver",
        "severity": "medium",
        "explanation": "The log references the NVIDIA driver and may indicate a driver compatibility issue.",
        "known_fix": [
            "Check that the NVIDIA driver is installed and loaded.",
            "Make sure 32-bit Vulkan libraries are installed if using Steam.",
            "Update the NVIDIA driver.",
            "Check Vulkan support with vulkaninfo."
        ],
        "safe_commands": [
            "nvidia-smi",
            "vulkaninfo"
        ],
    },

    "vk_error_device_lost": {
        "fingerprint": "VK_ERROR_DEVICE_LOST",
        "category": "Vulkan",
        "severity": "high",
        "explanation": "Vulkan reported device lost, which usually means the GPU driver crashed or the device became unavailable.",
        "known_fix": [
            "Update GPU drivers.",
            "Remove GPU overclocks or undervolts.",
            "Disable overlays temporarily.",
            "Try a different Proton version."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "vk_error_out_of_device_memory": {
        "fingerprint": "VK_ERROR_OUT_OF_DEVICE_MEMORY",
        "category": "Vulkan",
        "severity": "high",
        "explanation": "Vulkan ran out of GPU-accessible memory.",
        "known_fix": [
            "Lower texture quality.",
            "Close background GPU-heavy apps.",
            "Disable high-resolution texture packs.",
            "Check VRAM usage."
        ],
        "safe_commands": [],
    },

    "vk_error_extension_not_present": {
        "fingerprint": "VK_ERROR_EXTENSION_NOT_PRESENT",
        "category": "Vulkan",
        "severity": "medium",
        "explanation": "A required Vulkan extension was not available.",
        "known_fix": [
            "Update the GPU driver.",
            "Update Mesa or NVIDIA Vulkan packages.",
            "Check whether the GPU supports the required Vulkan features.",
            "Try a different Proton version."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

        "steam api init failed": {
        "fingerprint": "STEAM_API_INIT_FAILURE",
        "category": "Steam",
        "severity": "medium",
        "explanation": "The game failed to initialize the Steam API.",
        "known_fix": [
            "Restart Steam.",
            "Verify the game files.",
            "Make sure the game is launched through Steam.",
            "Disable broken launch options temporarily."
        ],
        "safe_commands": [],
    },

    "steam cloud": {
        "fingerprint": "STEAM_CLOUD_RELATED",
        "category": "Steam",
        "severity": "low",
        "explanation": "Steam Cloud appears in the log and may be related to sync or save issues.",
        "known_fix": [
            "Restart Steam.",
            "Temporarily disable Steam Cloud for the game if launch is blocked.",
            "Check for cloud sync conflicts.",
            "Try launching again after Steam finishes syncing."
        ],
        "safe_commands": [],
    },

    "shader pre-caching": {
        "fingerprint": "STEAM_SHADER_CACHE_RELATED",
        "category": "Steam",
        "severity": "low",
        "explanation": "Steam shader pre-caching appears in the log and may be delaying or affecting launch.",
        "known_fix": [
            "Wait for shader processing to finish.",
            "Restart Steam.",
            "Clear shader cache only if it repeatedly fails.",
            "Update GPU drivers."
        ],
        "safe_commands": [],
    },

    "prefix is not owned by you": {
        "fingerprint": "PROTON_PREFIX_PERMISSION_ISSUE",
        "category": "Proton Prefix",
        "severity": "high",
        "explanation": "The Proton prefix appears to have ownership or permission problems.",
        "known_fix": [
            "Do not run Steam as root.",
            "Make sure the Steam library and compatdata folder are owned by your user.",
            "If the prefix was created with root permissions, fix ownership carefully.",
            "Restart Steam after fixing ownership."
        ],
        "safe_commands": [
            "ls -la ~/.steam/steam/steamapps/compatdata"
        ],
    },

    "wine: could not load kernel32.dll": {
        "fingerprint": "PROTON_PREFIX_CORRUPTED",
        "category": "Proton Prefix",
        "severity": "high",
        "explanation": "Wine could not load a core Windows DLL, which often means the Proton prefix is corrupted.",
        "known_fix": [
            "Verify game files.",
            "Try a different Proton version.",
            "Rebuild the game's Proton prefix if needed.",
            "Avoid deleting files manually unless you know the exact AppID."
        ],
        "safe_commands": [],
    },

        "gamemoded": {
        "fingerprint": "GAMEMODE_DAEMON_RELATED",
        "category": "GameMode",
        "severity": "medium",
        "explanation": "The GameMode daemon appears in the log and may be failing or misconfigured.",
        "known_fix": [
            "Check whether GameMode is running correctly.",
            "Test the game without gamemoderun.",
            "Reinstall GameMode if the daemon is missing or broken."
        ],
        "safe_commands": [
            "gamemoded -s"
        ],
    },

    "gamemode request failed": {
        "fingerprint": "GAMEMODE_REQUEST_FAILURE",
        "category": "GameMode",
        "severity": "medium",
        "explanation": "The game or launcher requested GameMode, but the request failed.",
        "known_fix": [
            "Test without GameMode.",
            "Check GameMode service status.",
            "Make sure GameMode is installed correctly."
        ],
        "safe_commands": [
            "gamemoded -s"
        ],
    },

    "gamescope: vkcreateinstance failed": {
        "fingerprint": "GAMESCOPE_VULKAN_INIT_FAILURE",
        "category": "Gamescope",
        "severity": "high",
        "explanation": "Gamescope failed while creating a Vulkan instance.",
        "known_fix": [
            "Fix Vulkan first.",
            "Test the game without Gamescope.",
            "Update Gamescope and GPU drivers.",
            "Run vulkaninfo to confirm Vulkan works outside Gamescope."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "gamescope: wayland": {
        "fingerprint": "GAMESCOPE_WAYLAND_RELATED",
        "category": "Gamescope",
        "severity": "medium",
        "explanation": "Gamescope references Wayland and may be having a session or compositor issue.",
        "known_fix": [
            "Test without Gamescope.",
            "Try a simpler Gamescope launch option.",
            "Update Gamescope.",
            "Check whether the issue happens only on Wayland."
        ],
        "safe_commands": [],
    },

    "mangohud config": {
        "fingerprint": "MANGOHUD_CONFIG_RELATED",
        "category": "Performance Overlay",
        "severity": "low",
        "explanation": "MangoHud configuration appears in the log and may be affecting overlay behavior.",
        "known_fix": [
            "Temporarily disable MangoHud.",
            "Test the game without overlays.",
            "Reset MangoHud config if the overlay causes launch issues."
        ],
        "safe_commands": [],
    },

        "easyanticheat eos": {
        "fingerprint": "EAC_EOS_RELATED",
        "category": "Anti-Cheat",
        "severity": "high",
        "explanation": "Easy Anti-Cheat EOS appears in the log and may be blocking launch.",
        "known_fix": [
            "Verify game files.",
            "Check whether the game currently supports EAC on Proton.",
            "Try the Proton version recommended by ProtonDB.",
            "Do not troubleshoot graphics first if anti-cheat is the first failure."
        ],
        "safe_commands": [],
    },

    "easyanticheat_x64.so": {
        "fingerprint": "EAC_LINUX_RUNTIME_RELATED",
        "category": "Anti-Cheat",
        "severity": "high",
        "explanation": "The Linux Easy Anti-Cheat runtime appears in the log.",
        "known_fix": [
            "Confirm the game enables EAC support for Proton.",
            "Verify game files.",
            "Restart Steam.",
            "Try Proton Experimental."
        ],
        "safe_commands": [],
    },

    "battleye launcher": {
        "fingerprint": "BATTLEYE_LAUNCHER_RELATED",
        "category": "Anti-Cheat",
        "severity": "high",
        "explanation": "BattlEye launcher appears in the log and may be preventing startup.",
        "known_fix": [
            "Verify game files.",
            "Check whether BattlEye support is enabled for the game on Proton.",
            "Try Proton Experimental.",
            "Avoid custom launch scripts while testing."
        ],
        "safe_commands": [],
    },

    "steam linux runtime": {
        "fingerprint": "STEAM_LINUX_RUNTIME_RELATED",
        "category": "Steam Runtime",
        "severity": "medium",
        "explanation": "Steam Linux Runtime appears in the log and may be involved in the launch environment.",
        "known_fix": [
            "Restart Steam.",
            "Update Steam Runtime components.",
            "Verify game files.",
            "Try switching Proton versions."
        ],
        "safe_commands": [],
    },

    "pressure-vessel": {
        "fingerprint": "PRESSURE_VESSEL_RELATED",
        "category": "Steam Runtime",
        "severity": "medium",
        "explanation": "Pressure Vessel, Steam's container runtime, appears in the log and may be part of the failure.",
        "known_fix": [
            "Restart Steam.",
            "Update Steam.",
            "Check whether Steam Runtime tools are installed correctly.",
            "Test with a different Proton version."
        ],
        "safe_commands": [],
    },

        "oom-killer": {
        "fingerprint": "OOM_KILLER_TRIGGERED",
        "category": "Memory",
        "severity": "high",
        "explanation": "The Linux OOM killer appears to have terminated a process because the system ran out of memory.",
        "known_fix": [
            "Close background apps before launching the game.",
            "Lower memory-heavy settings like textures.",
            "Check RAM and swap usage.",
            "Consider enabling or increasing swap if the system has none."
        ],
        "safe_commands": [
            "free -h",
            "journalctl -k | grep -i oom"
        ],
    },

    "cannot allocate memory": {
        "fingerprint": "MEMORY_ALLOCATION_FAILURE",
        "category": "Memory",
        "severity": "high",
        "explanation": "The game or compatibility layer failed to allocate memory.",
        "known_fix": [
            "Close background apps.",
            "Lower game settings.",
            "Reboot and test again.",
            "Check available RAM and swap."
        ],
        "safe_commands": [
            "free -h"
        ],
    },

    "no space left on device": {
        "fingerprint": "DISK_FULL",
        "category": "Storage",
        "severity": "high",
        "explanation": "The system or Steam library appears to be out of available disk space.",
        "known_fix": [
            "Free up disk space.",
            "Clear unnecessary downloads or shader caches.",
            "Verify the Steam library has enough space.",
            "Restart Steam after freeing space."
        ],
        "safe_commands": [
            "df -h"
        ],
    },

    "read-only file system": {
        "fingerprint": "READ_ONLY_FILESYSTEM",
        "category": "Storage",
        "severity": "high",
        "explanation": "The game or Steam tried to write to a filesystem mounted as read-only.",
        "known_fix": [
            "Check whether the drive is mounted read-only.",
            "Check the health of the drive.",
            "Avoid installing games to drives with broken mount options.",
            "Restart and check the filesystem if this appeared suddenly."
        ],
        "safe_commands": [
            "mount | grep ' ro,'",
            "df -h"
        ],
    },

    "input/output error": {
        "fingerprint": "FILESYSTEM_IO_ERROR",
        "category": "Storage",
        "severity": "high",
        "explanation": "The log shows an input/output error, which can indicate filesystem, drive, or mount problems.",
        "known_fix": [
            "Check whether the game drive is healthy.",
            "Verify game files.",
            "Check kernel logs for disk errors.",
            "Avoid repeatedly launching from a failing drive."
        ],
        "safe_commands": [
            "journalctl -k | grep -i error",
            "df -h"
        ],
    },

        "d3d11: failed": {
        "fingerprint": "DXVK_D3D11_FAILURE",
        "category": "DXVK",
        "severity": "medium",
        "explanation": "DXVK reported a Direct3D 11 failure.",
        "known_fix": [
            "Update Proton.",
            "Update Mesa or NVIDIA drivers.",
            "Try a different Proton version.",
            "Check Vulkan with vulkaninfo."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "dxvk: failed": {
        "fingerprint": "DXVK_GENERAL_FAILURE",
        "category": "DXVK",
        "severity": "medium",
        "explanation": "DXVK reported a general failure.",
        "known_fix": [
            "Fix Vulkan first.",
            "Update GPU drivers.",
            "Try Proton Experimental or GE-Proton.",
            "Disable overlays while testing."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "vkd3d-proton: failed": {
        "fingerprint": "VKD3D_PROTON_FAILURE",
        "category": "VKD3D",
        "severity": "medium",
        "explanation": "VKD3D-Proton reported a DirectX 12 translation failure.",
        "known_fix": [
            "Update Proton.",
            "Update GPU drivers.",
            "Try Proton Experimental.",
            "If the game supports DirectX 11, test DX11 mode."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "d3d12": {
        "fingerprint": "DIRECTX12_RELATED",
        "category": "VKD3D",
        "severity": "medium",
        "explanation": "The log references DirectX 12, which Proton handles through VKD3D-Proton.",
        "known_fix": [
            "Update Proton and GPU drivers.",
            "Try Proton Experimental.",
            "Try DirectX 11 mode if the game supports it.",
            "Check whether the GPU supports required Vulkan features."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

    "d3d11": {
        "fingerprint": "DIRECTX11_RELATED",
        "category": "DXVK",
        "severity": "low",
        "explanation": "The log references DirectX 11, which Proton handles through DXVK.",
        "known_fix": [
            "If errors also mention Vulkan, fix Vulkan first.",
            "Update Proton.",
            "Update GPU drivers.",
            "Try a different Proton version."
        ],
        "safe_commands": [
            "vulkaninfo"
        ],
    },

        "nvidia_icd": {
        "fingerprint": "NVIDIA_ICD_RELATED",
        "category": "NVIDIA Vulkan",
        "severity": "high",
        "explanation": "The log references the NVIDIA Vulkan ICD, which may be missing, broken, or mismatched.",
        "known_fix": [
            "Check that the NVIDIA Vulkan driver is installed.",
            "Install 32-bit NVIDIA Vulkan libraries for Steam if needed.",
            "Update the NVIDIA driver.",
            "Run vulkaninfo to confirm Vulkan works."
        ],
        "safe_commands": [
            "nvidia-smi",
            "vulkaninfo"
        ],
    },

    "libnvidia-gl": {
        "fingerprint": "NVIDIA_GL_LIBRARY_RELATED",
        "category": "NVIDIA Driver",
        "severity": "medium",
        "explanation": "The log references NVIDIA OpenGL/Vulkan driver libraries.",
        "known_fix": [
            "Check for NVIDIA driver version mismatches.",
            "Update NVIDIA packages together.",
            "Reboot after updating graphics drivers.",
            "Make sure 32-bit NVIDIA libraries are installed for Steam."
        ],
        "safe_commands": [
            "nvidia-smi"
        ],
    },

    "wrong elf class": {
        "fingerprint": "WRONG_ARCH_LIBRARY",
        "category": "Library Mismatch",
        "severity": "high",
        "explanation": "A library with the wrong architecture was loaded, usually a 32-bit versus 64-bit mismatch.",
        "known_fix": [
            "Install the matching 32-bit library package.",
            "Verify Steam runtime dependencies.",
            "Avoid manually copying libraries into game folders.",
            "Reinstall the affected driver/runtime packages."
        ],
        "safe_commands": [],
    },

    "cannot open shared object file": {
        "fingerprint": "MISSING_SHARED_LIBRARY",
        "category": "Missing Library",
        "severity": "medium",
        "explanation": "A required Linux shared library could not be opened.",
        "known_fix": [
            "Identify which library is missing.",
            "Install the package that provides it.",
            "Verify game files.",
            "Avoid downloading random shared libraries manually."
        ],
        "safe_commands": [
            "ldd --version"
        ],
    },

    "icd": {
        "fingerprint": "VULKAN_ICD_RELATED",
        "category": "Vulkan",
        "severity": "medium",
        "explanation": "The log references a Vulkan ICD, which controls which Vulkan driver is loaded.",
        "known_fix": [
            "Check that the correct Vulkan ICD is installed.",
            "Remove broken Vulkan environment overrides.",
            "Run vulkaninfo.",
            "Check whether multiple GPU drivers are conflicting."
        ],
        "safe_commands": [
            "vulkaninfo",
            "ls /usr/share/vulkan/icd.d/"
        ],
    },

        "mfplat": {
        "fingerprint": "MEDIA_FOUNDATION_RELATED",
        "category": "Media Foundation",
        "severity": "medium",
        "explanation": "The log references Media Foundation, which is often involved in cutscenes, videos, launchers, or in-game media playback.",
        "known_fix": [
            "Try Proton Experimental or GE-Proton.",
            "Check whether the issue happens during videos or cutscenes.",
            "Verify game files.",
            "Check ProtonDB for game-specific Media Foundation notes."
        ],
        "safe_commands": [],
    },

    "wmvcore": {
        "fingerprint": "WINDOWS_MEDIA_COMPONENT_RELATED",
        "category": "Media Foundation",
        "severity": "medium",
        "explanation": "The log references Windows media components that may be required for video playback.",
        "known_fix": [
            "Try Proton Experimental or GE-Proton.",
            "Verify game files.",
            "Check whether the game fails during intro videos.",
            "Look for game-specific ProtonDB launch notes."
        ],
        "safe_commands": [],
    },

    "xaudio2": {
        "fingerprint": "XAUDIO_RELATED",
        "category": "Audio",
        "severity": "medium",
        "explanation": "The log references XAudio, a Windows audio component commonly used by games.",
        "known_fix": [
            "Try a different Proton version.",
            "Check PipeWire or PulseAudio output devices.",
            "Disable unusual audio launch options.",
            "Verify game files."
        ],
        "safe_commands": [
            "pactl info"
        ],
    },

    "faudio": {
        "fingerprint": "FAUDIO_RELATED",
        "category": "Audio",
        "severity": "medium",
        "explanation": "The log references FAudio, which Proton uses for XAudio compatibility.",
        "known_fix": [
            "Update Proton.",
            "Check that system audio is working outside the game.",
            "Restart PipeWire or the audio session if audio is broken system-wide.",
            "Try another Proton version."
        ],
        "safe_commands": [
            "pactl info"
        ],
    },

    "pulse audio": {
        "fingerprint": "PULSEAUDIO_RELATED",
        "category": "Audio",
        "severity": "low",
        "explanation": "The log references PulseAudio compatibility or audio routing.",
        "known_fix": [
            "Check the active audio server.",
            "Restart the game after changing audio devices.",
            "Test with default audio output.",
            "Check whether PipeWire-Pulse is running."
        ],
        "safe_commands": [
            "pactl info"
        ],
    },

        "wineprefix": {
        "fingerprint": "WINEPREFIX_RELATED",
        "category": "Proton Prefix",
        "severity": "medium",
        "explanation": "The log references a Wine or Proton prefix.",
        "known_fix": [
            "Check for earlier prefix errors.",
            "Try another Proton version.",
            "Verify game files.",
            "If the prefix is corrupted, rebuild it."
        ],
        "safe_commands": [],
    },

    "failed to open registry key": {
        "fingerprint": "PROTON_REGISTRY_FAILURE",
        "category": "Registry",
        "severity": "medium",
        "explanation": "Wine failed to access a registry key required by the game or launcher.",
        "known_fix": [
            "Try a clean Proton prefix.",
            "Verify game files.",
            "Switch Proton versions once.",
            "Check for broken mods or launchers."
        ],
        "safe_commands": [],
    },

    "wineboot.exe": {
        "fingerprint": "WINEBOOT_EXECUTION_FAILURE",
        "category": "Proton Prefix",
        "severity": "high",
        "explanation": "Wineboot failed during prefix initialization.",
        "known_fix": [
            "Rebuild the Proton prefix.",
            "Verify game files.",
            "Update Proton.",
            "Avoid mixing Proton versions inside the same prefix."
        ],
        "safe_commands": [],
    },

    "setupapi": {
        "fingerprint": "SETUPAPI_RELATED",
        "category": "Windows Runtime",
        "severity": "medium",
        "explanation": "Wine SetupAPI was involved in a failure.",
        "known_fix": [
            "Check earlier DLL or prefix errors.",
            "Verify game files.",
            "Try another Proton version.",
            "Rebuild the prefix if setup repeatedly fails."
        ],
        "safe_commands": [],
    },

    "kernel32.dll": {
        "fingerprint": "KERNEL32_RELATED_FAILURE",
        "category": "Windows Runtime",
        "severity": "high",
        "explanation": "Kernel32 is a core Windows component and its failure usually indicates a broken prefix or dependency issue.",
        "known_fix": [
            "Verify game files.",
            "Try another Proton version.",
            "Rebuild the Proton prefix.",
            "Check for broken DLL overrides."
        ],
        "safe_commands": [],
    }
}

from fingerprints.registry import ERROR_PATTERNS_V2

ERROR_PATTERNS.update(ERROR_PATTERNS_V2)
