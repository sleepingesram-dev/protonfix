KNOWN_ISSUES = {

    # ---- Vulkan / GPU driver ----

    "VULKAN_DRIVER_MISSING": {
        "title": "Missing or Broken Vulkan Driver",
        "summary": "The log shows Vulkan cannot find a compatible driver or GPU device.",
        "probable_cause": "The Vulkan driver is missing, broken, or incompatible with the installed GPU driver.",
        "severity": "high",
        "fix_steps": [
            "Install or reinstall the Vulkan driver for your GPU.",
            "For AMD GPUs on Arch/CachyOS: install mesa, vulkan-radeon, and vulkan-tools.",
            "For NVIDIA GPUs: install the nvidia package and nvidia-utils.",
            "Reboot after installing or updating graphics packages.",
            "Run vulkaninfo to confirm Vulkan is working.",
            "Try launching the game again after Vulkan works.",
        ],
        "recommended_commands": [
            "vulkaninfo",
            "sudo pacman -Syu mesa vulkan-radeon vulkan-tools",
        ],
        "warnings": [
            "Do not troubleshoot Proton first if Vulkan itself is broken.",
            "DXVK depends on Vulkan, so DXVK errors may be symptoms of the same root problem.",
        ],
    },

    "VULKAN_INIT_FAILURE": {
        "title": "Vulkan Initialization Failed",
        "summary": "The game or compatibility layer could not initialize Vulkan.",
        "probable_cause": "Vulkan could not create an instance. The driver may be missing, outdated, or misconfigured.",
        "severity": "high",
        "fix_steps": [
            "Run vulkaninfo to check whether Vulkan works outside the game.",
            "Update Mesa or the NVIDIA Vulkan driver.",
            "Remove custom VULKAN_ICD_FILENAMES or VK_ICD_FILENAMES environment variables.",
            "Try launching the game without Gamescope to isolate the issue.",
            "Reboot after driver updates.",
        ],
        "recommended_commands": [
            "vulkaninfo",
            "ls /usr/share/vulkan/icd.d/",
        ],
        "warnings": [
            "If vulkaninfo also fails, the Vulkan driver itself is broken — fix that first.",
        ],
    },

    "VK_ERROR_DEVICE_LOST": {
        "title": "Vulkan Device Lost",
        "summary": "The GPU driver reported a device-lost error, which usually means the driver crashed mid-frame.",
        "probable_cause": "A Vulkan device-lost error occurred. Common causes: unstable GPU overclock, driver bug, or VRAM corruption.",
        "severity": "high",
        "fix_steps": [
            "Remove any GPU overclocks or undervolts and test again.",
            "Update Mesa or the NVIDIA driver.",
            "Disable DXVK async shader compilation (remove DXVK_ASYNC=1 from launch options).",
            "Try a different Proton version.",
            "Check kernel logs for amdgpu or nvidia driver errors.",
        ],
        "recommended_commands": [
            "journalctl -k | grep -iE 'amdgpu|nvidia|gpu'",
            "vulkaninfo",
        ],
        "warnings": [
            "If this happens in multiple games, the GPU or driver is the problem, not the game.",
        ],
    },

    "VK_ERROR_OUT_OF_DEVICE_MEMORY": {
        "title": "GPU Out of Memory (VRAM)",
        "summary": "Vulkan ran out of GPU-accessible memory while the game was running.",
        "probable_cause": "The game or translation layer could not allocate more VRAM. The GPU may not have enough memory for the current settings.",
        "severity": "high",
        "fix_steps": [
            "Lower texture quality or resolution in the game settings.",
            "Disable high-resolution texture mods or replacement packs.",
            "Close other GPU-heavy applications.",
            "Lower anti-aliasing and shadow quality settings.",
            "Check available VRAM before launching the game.",
        ],
        "recommended_commands": [
            "nvidia-smi",
            "radeontop",
        ],
        "warnings": [
            "Lowering in-game settings is more effective than changing Proton version for VRAM errors.",
        ],
    },

    "VK_ERROR_EXTENSION_NOT_PRESENT": {
        "title": "Missing Vulkan Extension",
        "summary": "A Vulkan extension required by the game or DXVK/VKD3D is not available on this system.",
        "probable_cause": "The installed Vulkan driver does not support an extension the game or translation layer requires.",
        "severity": "high",
        "fix_steps": [
            "Update Mesa or the NVIDIA Vulkan driver — older versions lack extensions newer games need.",
            "Run vulkaninfo and check which extensions are listed.",
            "If using Gamescope, try launching without it and check whether the extension is available directly.",
            "Verify the correct Vulkan ICD is being loaded (check ls /usr/share/vulkan/icd.d/).",
        ],
        "recommended_commands": [
            "vulkaninfo",
            "ls /usr/share/vulkan/icd.d/",
        ],
        "warnings": [],
    },

    # ---- DXVK ----

    "DXVK_ADAPTER_FAILURE": {
        "title": "DXVK Could Not Initialize Graphics Adapter",
        "summary": "DXVK failed to find or initialize a usable Vulkan graphics adapter.",
        "probable_cause": "DXVK depends on Vulkan. If Vulkan is broken or the adapter is not exposed correctly, DXVK cannot start.",
        "severity": "high",
        "fix_steps": [
            "Fix Vulkan first — run vulkaninfo and confirm it works without errors.",
            "Update Mesa or the NVIDIA Vulkan driver.",
            "Remove any DXVK_FILTER_DEVICE_NAME or similar environment variable overrides.",
            "Try a different Proton version.",
        ],
        "recommended_commands": [
            "vulkaninfo",
            "lspci | grep -E 'VGA|3D|Display'",
        ],
        "warnings": [
            "DXVK adapter errors are almost always a symptom of a Vulkan problem, not a DXVK bug.",
        ],
    },

    "DXVK_RELATED_FAILURE": {
        "title": "DXVK Failure",
        "summary": "DXVK, which translates DirectX 9/10/11 to Vulkan, reported a failure.",
        "probable_cause": "DXVK encountered an error during DirectX-to-Vulkan translation. Usually caused by an outdated Vulkan driver or an incompatible Proton version.",
        "severity": "medium",
        "fix_steps": [
            "Check for Vulkan errors first — DXVK errors often cascade from Vulkan problems.",
            "Update Proton to the latest version.",
            "Update Mesa or the NVIDIA driver.",
            "Try Proton Experimental or GE-Proton.",
            "Disable overlays while testing.",
        ],
        "recommended_commands": ["vulkaninfo"],
        "warnings": [],
    },

    "DXVK_D3D11_FAILURE": {
        "title": "DXVK Direct3D 11 Failure",
        "summary": "DXVK reported a Direct3D 11 initialization or runtime failure.",
        "probable_cause": "DXVK failed while creating or using a D3D11 device. This is usually a Vulkan driver or DXVK version mismatch.",
        "severity": "medium",
        "fix_steps": [
            "Update Proton — DXVK is bundled with Proton and updating Proton updates DXVK.",
            "Update Mesa or NVIDIA Vulkan packages.",
            "Try a different Proton version.",
            "Run vulkaninfo to confirm Vulkan is functional.",
        ],
        "recommended_commands": ["vulkaninfo"],
        "warnings": [],
    },

    # ---- VKD3D ----

    "VKD3D_RELATED_FAILURE": {
        "title": "VKD3D Failure",
        "summary": "VKD3D-Proton, which translates DirectX 12 to Vulkan, reported a failure.",
        "probable_cause": "VKD3D-Proton could not initialize or translate a DX12 call. Often caused by an outdated Vulkan driver lacking required extensions.",
        "severity": "high",
        "fix_steps": [
            "Update Proton — VKD3D-Proton is bundled with Proton.",
            "Update Mesa or the NVIDIA Vulkan driver.",
            "Run vulkaninfo and look for missing Vulkan 1.2/1.3 features.",
            "If the game supports DirectX 11, try forcing DX11 mode via launch options.",
            "Try Proton Experimental.",
        ],
        "recommended_commands": ["vulkaninfo"],
        "warnings": [
            "VKD3D-Proton requires Vulkan 1.3 and several extensions. Very old drivers will not work.",
        ],
    },

    "VKD3D_PROTON_FAILURE": {
        "title": "VKD3D-Proton Failure",
        "summary": "VKD3D-Proton reported an error during DirectX 12 translation.",
        "probable_cause": "A specific VKD3D-Proton call failed. Causes include missing Vulkan features, incorrect GPU state, or a known VKD3D bug.",
        "severity": "medium",
        "fix_steps": [
            "Update Proton to the latest version.",
            "Update your GPU drivers.",
            "Set VKD3D_CONFIG=no_upload_hvv as a launch option and test.",
            "If the game supports DX11, use PROTON_NO_D3D12=1 to disable DX12.",
            "Check ProtonDB for game-specific VKD3D notes.",
        ],
        "recommended_commands": ["vulkaninfo"],
        "warnings": [],
    },

    # ---- Anti-cheat ----

    "EAC_FAILURE": {
        "title": "Easy Anti-Cheat Failure",
        "summary": "Easy Anti-Cheat failed to initialize or blocked the game from starting.",
        "probable_cause": "EAC did not start successfully. On Linux, EAC requires the game developer to enable Linux/Proton support in the EAC configuration.",
        "severity": "high",
        "fix_steps": [
            "Check ProtonDB to confirm whether this game has EAC working on Proton.",
            "Verify game files in Steam.",
            "If the game uses EAC Easy Anti-Cheat for Epic Online Services, ensure the EOS overlay is enabled.",
            "Use the Proton version recommended by ProtonDB for this specific game.",
            "Do not troubleshoot graphics until EAC is confirmed working.",
        ],
        "recommended_commands": [],
        "warnings": [
            "EAC on Linux depends on the game developer enabling it — not all games support it.",
            "Changing Proton version is the most reliable fix when EAC is the root cause.",
        ],
    },

    "EAC_EOS_RELATED": {
        "title": "Easy Anti-Cheat EOS Issue",
        "summary": "The Easy Anti-Cheat Epic Online Services component appears in the log and may be blocking launch.",
        "probable_cause": "EAC EOS failed to initialize. This usually means the game requires the Epic Online Services overlay or a specific Proton runtime.",
        "severity": "high",
        "fix_steps": [
            "Verify game files in Steam.",
            "Use the Proton version recommended by ProtonDB for this game.",
            "Ensure the EOS overlay is not disabled in Steam settings.",
            "Do not change graphics settings until anti-cheat is confirmed working.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    "EAC_LINUX_RUNTIME_RELATED": {
        "title": "Easy Anti-Cheat Linux Runtime",
        "summary": "The native Linux EAC runtime (easyanticheat_x64.so) appears in the log.",
        "probable_cause": "The Linux EAC runtime was detected but may have failed or not been enabled properly by the game.",
        "severity": "high",
        "fix_steps": [
            "Verify game files in Steam.",
            "Restart Steam and try again.",
            "Use Proton Experimental if using an older Proton version.",
            "Check ProtonDB for current EAC reports for this game.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    "BATTLEYE_FAILURE": {
        "title": "BattlEye Failure",
        "summary": "BattlEye anti-cheat failed to initialize or blocked the game from starting.",
        "probable_cause": "BattlEye did not start successfully. Similar to EAC, BattlEye on Linux requires the game developer to enable Proton/Linux support.",
        "severity": "high",
        "fix_steps": [
            "Check ProtonDB to confirm whether BattlEye works for this game on Proton.",
            "Verify game files in Steam.",
            "Use the Proton version recommended by ProtonDB for this game.",
            "Try Proton Experimental.",
            "Do not troubleshoot graphics or audio until BattlEye is confirmed working.",
        ],
        "recommended_commands": [],
        "warnings": [
            "BattlEye on Linux depends on developer support — not all games enable it.",
        ],
    },

    "BATTLEYE_LAUNCHER_RELATED": {
        "title": "BattlEye Launcher Issue",
        "summary": "The BattlEye launcher component appears in the log and may be blocking startup.",
        "probable_cause": "The BattlEye launcher failed or did not initialize the anti-cheat service correctly.",
        "severity": "high",
        "fix_steps": [
            "Verify game files in Steam.",
            "Try Proton Experimental.",
            "Check ProtonDB for current BattlEye compatibility reports.",
            "Avoid custom launch scripts while testing anti-cheat issues.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    # ---- Proton prefix ----

    "PROTON_PREFIX_CORRUPTED": {
        "title": "Corrupted Proton Prefix",
        "summary": "The Proton/Wine prefix appears to be damaged or missing critical files.",
        "probable_cause": "The Proton prefix for this game is corrupted. This often happens after a bad update, an interrupted install, or switching Proton versions incorrectly.",
        "severity": "high",
        "fix_steps": [
            "Verify game files in Steam — this rebuilds the prefix if it is incomplete.",
            "Try switching to a different Proton version once and launch the game.",
            "If the issue persists, delete the prefix folder and let Steam recreate it.",
            "To delete the prefix: go to ~/.steam/steam/steamapps/compatdata/<AppID>/ and delete the pfx folder.",
            "Avoid manually mixing files between different Proton version prefixes.",
        ],
        "recommended_commands": [
            "ls ~/.steam/steam/steamapps/compatdata/",
        ],
        "warnings": [
            "Deleting the prefix will reset all game settings stored in the prefix (registry, saved configs).",
        ],
    },

    "PROTON_PREFIX_PERMISSION_ISSUE": {
        "title": "Proton Prefix Permission Problem",
        "summary": "Proton cannot read or write its prefix directory due to a permission error.",
        "probable_cause": "The Proton prefix or Steam library folder has incorrect ownership or permissions — often caused by running Steam as root at some point.",
        "severity": "high",
        "fix_steps": [
            "Do not run Steam as root or with sudo.",
            "Check that the Steam library and compatdata folder are owned by your regular user.",
            "Fix ownership: chown -R $USER:$USER ~/.steam/steam/steamapps/compatdata/<AppID>/",
            "Restart Steam after fixing permissions.",
        ],
        "recommended_commands": [
            "ls -la ~/.steam/steam/steamapps/compatdata/",
            "stat ~/.steam/steam/steamapps/",
        ],
        "warnings": [
            "Never run Steam as root — it causes ownership issues that are hard to reverse cleanly.",
        ],
    },

    "PROTON_WINEBOOT_FAILURE": {
        "title": "Proton Wineboot Failed",
        "summary": "Wineboot failed while setting up or updating the Proton prefix.",
        "probable_cause": "The prefix setup step (wineboot) failed, which prevents the game from starting. Usually caused by a corrupted prefix or a Proton version incompatibility.",
        "severity": "high",
        "fix_steps": [
            "Try switching to a different Proton version and launch again.",
            "Verify game files in Steam.",
            "If wineboot still fails, delete the prefix and let Proton rebuild it.",
            "Avoid installing winetricks or modifying the prefix manually.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    "PROTON_DLL_MISSING": {
        "title": "Missing DLL",
        "summary": "Proton or Wine could not load a required DLL.",
        "probable_cause": "A required Windows DLL could not be found or loaded. This could be a game file, a launcher dependency, or a corrupted prefix.",
        "severity": "medium",
        "fix_steps": [
            "Verify game files in Steam.",
            "If the DLL belongs to a launcher (Epic, EA App, etc.), reinstall the launcher within the prefix.",
            "Try a clean Proton prefix.",
            "Do not manually download DLL files from the internet — use verified package sources.",
        ],
        "recommended_commands": [],
        "warnings": [
            "Random DLL downloads from the internet are a security risk and rarely fix the root problem.",
        ],
    },

    "PROTON_REGISTRY_FAILURE": {
        "title": "Wine Registry Access Failed",
        "summary": "Wine could not open a registry key required by the game or launcher.",
        "probable_cause": "The Proton prefix registry is corrupted or the required registry entry is missing.",
        "severity": "medium",
        "fix_steps": [
            "Try a clean Proton prefix.",
            "Verify game files in Steam.",
            "Switch Proton versions once.",
            "Check for broken mods or third-party launchers that modify the registry.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    # ---- AMD ----

    "AMDGPU_RESET": {
        "title": "AMD GPU Reset",
        "summary": "The AMD GPU driver reported a GPU reset, which means the driver recovered from a crash.",
        "probable_cause": "The AMD GPU driver hung and triggered a reset. Common causes: unstable GPU overclock/undervolt, driver bug, or a Vulkan crash.",
        "severity": "high",
        "fix_steps": [
            "Remove any GPU overclocks or undervolts and test at stock settings.",
            "Update Mesa and Vulkan packages.",
            "Reboot after updating.",
            "Check kernel logs for amdgpu errors before and after the reset.",
            "If the reset happens in multiple games, the issue is driver-level, not game-specific.",
        ],
        "recommended_commands": [
            "sudo pacman -Syu mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon",
            "journalctl -k | grep -i amdgpu",
        ],
        "warnings": [
            "GPU resets indicate instability — playing with overclocks active after a reset risks data loss.",
        ],
    },

    "AMDGPU_RING_TIMEOUT": {
        "title": "AMD GPU Ring Timeout",
        "summary": "The AMD graphics command ring timed out, meaning the GPU driver hung.",
        "probable_cause": "The AMD GPU driver stopped responding. This is similar to a GPU reset and is caused by driver instability, overclocks, or a kernel/Mesa mismatch.",
        "severity": "high",
        "fix_steps": [
            "Update Mesa and the Linux kernel together.",
            "Remove any GPU overclocks or undervolts.",
            "Test the game without Gamescope and without overlays.",
            "Check kernel logs for the full amdgpu error context.",
        ],
        "recommended_commands": [
            "journalctl -k | grep -i amdgpu",
            "uname -r",
        ],
        "warnings": [],
    },

    "RADV_RELATED_FAILURE": {
        "title": "RADV (AMD Mesa Vulkan) Issue",
        "summary": "The RADV Mesa Vulkan driver for AMD GPUs reported a problem.",
        "probable_cause": "RADV encountered an error. This could be a driver bug, an outdated Mesa version, or a Vulkan feature mismatch.",
        "severity": "medium",
        "fix_steps": [
            "Update Mesa to the latest available version.",
            "Run vulkaninfo to check RADV is the active Vulkan driver.",
            "Remove any RADV_PERFTEST or RADV_DEBUG environment variables and test.",
            "If using ACO shader compiler, try disabling experimental options.",
        ],
        "recommended_commands": [
            "vulkaninfo | grep -i radv",
            "sudo pacman -Syu mesa vulkan-radeon",
        ],
        "warnings": [],
    },

    # ---- NVIDIA ----

    "NVIDIA_DRIVER_RELATED": {
        "title": "NVIDIA Driver Issue",
        "summary": "The log references the NVIDIA driver and may indicate a driver compatibility problem.",
        "probable_cause": "The NVIDIA driver encountered an issue. This could be a missing 32-bit library, a driver version mismatch, or a Vulkan ICD problem.",
        "severity": "medium",
        "fix_steps": [
            "Verify the NVIDIA driver is installed and loaded: run nvidia-smi.",
            "Install 32-bit NVIDIA libraries if using Steam: lib32-nvidia-utils on Arch.",
            "Update the NVIDIA driver.",
            "Run vulkaninfo and check whether NVIDIA appears as a Vulkan device.",
            "Reboot after driver updates.",
        ],
        "recommended_commands": [
            "nvidia-smi",
            "vulkaninfo",
        ],
        "warnings": [],
    },

    "NVIDIA_ICD_RELATED": {
        "title": "NVIDIA Vulkan ICD Issue",
        "summary": "The NVIDIA Vulkan ICD file is missing, broken, or not loaded correctly.",
        "probable_cause": "The Vulkan loader cannot find or load the NVIDIA ICD. This happens when the NVIDIA Vulkan package is missing or misconfigured.",
        "severity": "high",
        "fix_steps": [
            "Install or reinstall the NVIDIA Vulkan driver package.",
            "On Arch: install nvidia-utils and lib32-nvidia-utils.",
            "Check that /usr/share/vulkan/icd.d/nvidia_icd.json exists.",
            "Reboot after reinstalling.",
            "Run vulkaninfo to confirm NVIDIA appears as a Vulkan device.",
        ],
        "recommended_commands": [
            "ls /usr/share/vulkan/icd.d/",
            "nvidia-smi",
            "vulkaninfo",
        ],
        "warnings": [],
    },

    "NVIDIA_GL_LIBRARY_RELATED": {
        "title": "NVIDIA OpenGL/Vulkan Library Issue",
        "summary": "An NVIDIA OpenGL or Vulkan library could not be loaded.",
        "probable_cause": "The NVIDIA driver library files are missing or have a version mismatch between 32-bit and 64-bit packages.",
        "severity": "medium",
        "fix_steps": [
            "Update NVIDIA packages as a group to avoid version mismatches.",
            "Install lib32-nvidia-utils for 32-bit game and Steam support.",
            "Reboot after updating.",
            "Run nvidia-smi to confirm the driver is loaded.",
        ],
        "recommended_commands": [
            "nvidia-smi",
        ],
        "warnings": [
            "Partial NVIDIA upgrades (one package but not others) cause library version mismatches.",
        ],
    },

    # ---- Memory ----

    "OUT_OF_MEMORY": {
        "title": "Out of System Memory",
        "summary": "The system or game ran out of available RAM or swap space.",
        "probable_cause": "The system could not allocate enough memory. This may be caused by the game needing more RAM than available, or background processes consuming too much memory.",
        "severity": "high",
        "fix_steps": [
            "Close background applications before launching the game.",
            "Lower game settings that use a lot of memory (textures, render distance).",
            "Check RAM and swap usage before launching.",
            "If you have no swap, consider enabling a swap file.",
            "Reboot and try again.",
        ],
        "recommended_commands": [
            "free -h",
            "swapon --show",
        ],
        "warnings": [],
    },

    "OOM_KILLER_TRIGGERED": {
        "title": "OOM Killer Terminated a Process",
        "summary": "The Linux kernel OOM killer terminated a process because the system ran out of memory.",
        "probable_cause": "Physical RAM and swap were exhausted. The kernel chose a process to kill to recover memory.",
        "severity": "high",
        "fix_steps": [
            "Close background applications before launching memory-heavy games.",
            "Lower texture quality and other memory-intensive settings.",
            "Add or increase swap space if the system has none.",
            "Check which process was killed in the kernel log.",
        ],
        "recommended_commands": [
            "free -h",
            "journalctl -k | grep -i oom",
        ],
        "warnings": [
            "If the game process itself was killed, save data may be lost.",
        ],
    },

    "MEMORY_ALLOCATION_FAILURE": {
        "title": "Memory Allocation Failure",
        "summary": "The game or compatibility layer could not allocate the memory it needed.",
        "probable_cause": "A memory allocation call returned an error, usually because available RAM or address space was exhausted.",
        "severity": "high",
        "fix_steps": [
            "Close background applications.",
            "Lower game settings.",
            "Check RAM and swap usage.",
            "Reboot and try again.",
        ],
        "recommended_commands": [
            "free -h",
        ],
        "warnings": [],
    },

    # ---- Storage ----

    "DISK_FULL": {
        "title": "Disk Full",
        "summary": "The game or Steam cannot write files because the drive is out of space.",
        "probable_cause": "The filesystem where the game or its prefix is stored has no free space.",
        "severity": "high",
        "fix_steps": [
            "Check free space on all drives with df -h.",
            "Clear Steam download cache: Steam → Settings → Downloads → Clear Download Cache.",
            "Delete old shader cache folders in ~/.steam/steam/shadercache/.",
            "Remove games you are not playing.",
            "Restart Steam after freeing space.",
        ],
        "recommended_commands": [
            "df -h",
        ],
        "warnings": [],
    },

    "READ_ONLY_FILESYSTEM": {
        "title": "Read-Only Filesystem",
        "summary": "The game or Steam tried to write to a filesystem that is mounted read-only.",
        "probable_cause": "The drive or partition is mounted in read-only mode — either intentionally or because the filesystem has errors.",
        "severity": "high",
        "fix_steps": [
            "Check whether the drive is mounted read-only: run mount and look for 'ro'.",
            "Check drive health with smartctl.",
            "If the drive remounted read-only automatically, there may be filesystem corruption — run fsck after unmounting.",
            "Restart and check whether the drive mounts correctly.",
        ],
        "recommended_commands": [
            "mount | grep ' ro,'",
            "df -h",
        ],
        "warnings": [
            "A drive remounting itself read-only usually means filesystem errors — back up data before running fsck.",
        ],
    },

    "FILESYSTEM_IO_ERROR": {
        "title": "Filesystem I/O Error",
        "summary": "The log shows an input/output error, which can mean a failing drive or filesystem corruption.",
        "probable_cause": "A disk read or write operation failed. This could be a failing drive, bad sectors, or a corrupted filesystem.",
        "severity": "high",
        "fix_steps": [
            "Check kernel logs for disk errors.",
            "Run smartctl on the affected drive to check drive health.",
            "Verify game files in Steam.",
            "Back up important data before taking further steps.",
        ],
        "recommended_commands": [
            "journalctl -k | grep -iE 'error|failed'",
            "df -h",
        ],
        "warnings": [
            "Repeated I/O errors may indicate a failing drive. Back up data immediately.",
        ],
    },

    # ---- Media Foundation / Video ----

    "MEDIA_FOUNDATION_RELATED": {
        "title": "Windows Media Foundation Missing",
        "summary": "The game requires Windows Media Foundation components for video playback or the launcher.",
        "probable_cause": "mfplat.dll or related Media Foundation DLLs are not available in the Proton prefix. This affects games that use Windows video codecs for cutscenes or intro videos.",
        "severity": "medium",
        "fix_steps": [
            "Use GE-Proton — it includes Media Foundation patches by default.",
            "With standard Proton, try: PROTON_ENABLE_NVAPI=0 %command% (some games need this).",
            "If the issue is only intro videos, check whether skipping the video (ESC key) allows the game to continue.",
            "Verify game files in Steam.",
            "Check ProtonDB for game-specific Media Foundation workarounds.",
        ],
        "recommended_commands": [],
        "warnings": [
            "GE-Proton is the easiest fix for mfplat issues — standard Proton requires manual steps.",
        ],
    },

    "WINDOWS_MEDIA_COMPONENT_RELATED": {
        "title": "Windows Media Component Missing",
        "summary": "A Windows media component (wmvcore, etc.) required by the game is not available.",
        "probable_cause": "The game requires Windows media DLLs for video or audio playback that are not present in the standard Proton prefix.",
        "severity": "medium",
        "fix_steps": [
            "Use GE-Proton, which includes media component support.",
            "Check whether the issue occurs only on video/cutscene playback.",
            "Verify game files in Steam.",
            "Check ProtonDB for game-specific media workarounds.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    # ---- Library mismatches ----

    "MISSING_SHARED_LIBRARY": {
        "title": "Missing Linux Shared Library",
        "summary": "A required Linux shared library (.so file) could not be found.",
        "probable_cause": "A system library that the game or Proton needs is not installed or is not in the library path.",
        "severity": "medium",
        "fix_steps": [
            "Note the name of the missing .so file from the error.",
            "Find which package provides it: pkgfile <library.so> (Arch) or apt-file search <library.so> (Debian).",
            "Install the missing package, including 32-bit variants if needed.",
            "Verify game files in Steam after installing dependencies.",
        ],
        "recommended_commands": [
            "ldd --version",
        ],
        "warnings": [
            "Do not manually copy .so files between directories — install them via the package manager.",
        ],
    },

    "WRONG_ARCH_LIBRARY": {
        "title": "Architecture Mismatch (32-bit vs 64-bit)",
        "summary": "A library with the wrong architecture was loaded — usually a 32-bit library where a 64-bit one is expected, or vice versa.",
        "probable_cause": "The game or Steam is trying to load a 32-bit library but only the 64-bit version is installed, or vice versa.",
        "severity": "high",
        "fix_steps": [
            "Install the 32-bit version of the missing library (lib32-* on Arch).",
            "For Vulkan: install lib32-vulkan-radeon or lib32-nvidia-utils.",
            "For general Steam: install the steam-native-runtime or multilib packages.",
            "Reinstall the affected driver or runtime packages after enabling multilib.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    # ---- Gamescope ----

    "GAMESCOPE_VULKAN_INIT_FAILURE": {
        "title": "Gamescope Vulkan Initialization Failed",
        "summary": "Gamescope could not initialize Vulkan, preventing it from creating its rendering environment.",
        "probable_cause": "Gamescope failed to create a Vulkan instance or device. Usually caused by a broken Vulkan driver or missing Vulkan extensions.",
        "severity": "high",
        "fix_steps": [
            "Fix Vulkan first — run vulkaninfo outside Gamescope and confirm it works.",
            "Update Gamescope, Mesa, and Vulkan packages.",
            "Try launching the game without Gamescope to isolate the problem.",
            "If the game works without Gamescope, add Gamescope options back one at a time.",
        ],
        "recommended_commands": [
            "vulkaninfo",
            "gamescope --version",
        ],
        "warnings": [
            "Gamescope requires a working Vulkan driver — always fix Vulkan first.",
        ],
    },

    "GAMESCOPE_SWAPCHAIN_FAILURE": {
        "title": "Gamescope Swapchain Failure",
        "summary": "Gamescope could not create a Vulkan swapchain, which is required for display output.",
        "probable_cause": "Gamescope failed to set up its rendering surface. Common causes: HDR/VRR misconfiguration, Wayland compositor issues, or an incompatible display mode.",
        "severity": "high",
        "fix_steps": [
            "Try launching without HDR or VRR Gamescope options.",
            "Try a simpler Gamescope command (e.g., gamescope -w 1920 -h 1080 -f).",
            "Update Gamescope and Vulkan drivers.",
            "Test whether the game works without Gamescope.",
        ],
        "recommended_commands": [
            "gamescope --version",
        ],
        "warnings": [],
    },

    # ---- Steam ----

    "STEAM_API_INIT_FAILURE": {
        "title": "Steam API Initialization Failed",
        "summary": "The game could not initialize the Steam API.",
        "probable_cause": "The Steam API failed to start. This usually means the game was not launched through Steam, Steam is not running, or the game files are corrupted.",
        "severity": "medium",
        "fix_steps": [
            "Make sure Steam is running before launching the game.",
            "Always launch the game through Steam, not directly from the file manager.",
            "Restart Steam.",
            "Verify game files in Steam.",
            "Remove custom launch options that might interfere with Steam initialization.",
        ],
        "recommended_commands": [],
        "warnings": [],
    },

    "STEAM_DISK_WRITE_ERROR": {
        "title": "Steam Disk Write Error",
        "summary": "Steam could not write files to the game install location.",
        "probable_cause": "The Steam library folder has a permission problem, or the drive is full or failing.",
        "severity": "medium",
        "fix_steps": [
            "Check free disk space.",
            "Verify permissions on the Steam library folder.",
            "Restart Steam.",
            "Use Steam's library repair tool: Steam → Library → right-click library → Repair.",
        ],
        "recommended_commands": [
            "df -h",
        ],
        "warnings": [],
    },

    # ---- GameMode ----

    "GAMEMODE_DAEMON_RELATED": {
        "title": "GameMode Daemon Unavailable",
        "summary": "The GameMode background service is missing or not responding.",
        "probable_cause": "gamemoded is not installed or not running. GameMode optimizes CPU performance while gaming but is not required to launch games.",
        "severity": "low",
        "fix_steps": [
            "Install GameMode: sudo pacman -S gamemode (Arch) or sudo apt install gamemode (Debian).",
            "Start the daemon: systemctl --user start gamemoded.",
            "Remove gamemoderun from launch options if GameMode is not needed.",
            "This error is non-fatal — fix other errors first if the game is not launching.",
        ],
        "recommended_commands": [
            "systemctl --user status gamemoded",
            "gamemoded -s",
        ],
        "warnings": [
            "GameMode failure does not prevent game launch — treat it as low priority.",
        ],
    },

    "GAMEMODE_REQUEST_FAILURE": {
        "title": "GameMode Request Failed",
        "summary": "The game or launcher tried to activate GameMode but the request failed.",
        "probable_cause": "The GameMode daemon is not running or the requesting process does not have permission to use it.",
        "severity": "low",
        "fix_steps": [
            "Check whether gamemoded is running.",
            "Test the game without gamemoderun in launch options.",
            "If the game still fails without GameMode, the root cause is elsewhere.",
        ],
        "recommended_commands": [
            "gamemoded -s",
        ],
        "warnings": [],
    },

    # ---- Audio ----

    "XAUDIO_RELATED": {
        "title": "XAudio2 Issue",
        "summary": "The game could not initialize or use XAudio2, the Windows audio component.",
        "probable_cause": "XAudio2 failed in Proton. This can happen with certain audio configurations or when the audio device is unavailable.",
        "severity": "medium",
        "fix_steps": [
            "Check that system audio is working outside the game.",
            "Try setting the audio output device in the game to 'Default'.",
            "Try a different Proton version.",
            "If using PipeWire, ensure pipewire-pulse is running.",
        ],
        "recommended_commands": [
            "pactl info",
            "systemctl --user status pipewire pipewire-pulse",
        ],
        "warnings": [],
    },

    "FAUDIO_RELATED": {
        "title": "FAudio Issue",
        "summary": "FAudio, which Proton uses for XAudio compatibility, reported a problem.",
        "probable_cause": "FAudio could not initialize or connect to the audio system. Usually caused by an audio server problem.",
        "severity": "medium",
        "fix_steps": [
            "Check that audio works in other applications.",
            "Restart PipeWire: systemctl --user restart pipewire pipewire-pulse.",
            "Update Proton.",
            "Try another Proton version.",
        ],
        "recommended_commands": [
            "pactl info",
        ],
        "warnings": [],
    },

}
