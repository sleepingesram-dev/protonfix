FINGERPRINT_METADATA = {

    # ---- Vulkan ----
    "VULKAN_DRIVER_MISSING": {
        "display_name": "Missing Vulkan Driver",
        "short_description": "Vulkan could not find a working graphics driver.",
        "icon": "gpu",
    },
    "VULKAN_INIT_FAILURE": {
        "display_name": "Vulkan Initialization Failed",
        "short_description": "The game or compatibility layer failed to start Vulkan.",
        "icon": "gpu",
    },
    "VK_ERROR_DEVICE_LOST": {
        "display_name": "Vulkan Device Lost",
        "short_description": "The GPU driver crashed and reported a device-lost error.",
        "icon": "gpu",
    },
    "VK_ERROR_OUT_OF_DEVICE_MEMORY": {
        "display_name": "GPU Out of Memory",
        "short_description": "Vulkan ran out of GPU-accessible VRAM.",
        "icon": "memory",
    },
    "VK_ERROR_OUT_OF_HOST_MEMORY": {
        "display_name": "Vulkan Out of Host Memory",
        "short_description": "Vulkan ran out of system (CPU-side) memory.",
        "icon": "memory",
    },
    "VK_ERROR_EXTENSION_NOT_PRESENT": {
        "display_name": "Missing Vulkan Extension",
        "short_description": "A required Vulkan extension is not available on this system.",
        "icon": "gpu",
    },
    "VULKAN_ICD_RELATED": {
        "display_name": "Vulkan ICD Issue",
        "short_description": "The Vulkan ICD that maps to the GPU driver could not be loaded.",
        "icon": "gpu",
    },

    # ---- DXVK ----
    "DXVK_ADAPTER_FAILURE": {
        "display_name": "DXVK Adapter Failure",
        "short_description": "DXVK could not detect or use a compatible Vulkan adapter.",
        "icon": "dxvk",
    },
    "DXVK_RELATED_FAILURE": {
        "display_name": "DXVK Failure",
        "short_description": "DirectX-to-Vulkan translation failed or reported errors.",
        "icon": "dxvk",
    },
    "DXVK_GENERAL_FAILURE": {
        "display_name": "DXVK Failure",
        "short_description": "DXVK reported a general DirectX translation error.",
        "icon": "dxvk",
    },
    "DXVK_D3D11_FAILURE": {
        "display_name": "DXVK D3D11 Failure",
        "short_description": "DXVK failed during Direct3D 11 initialization or operation.",
        "icon": "dxvk",
    },
    "DXVK_SHADER_COMPILE_FAILURE": {
        "display_name": "DXVK Shader Compilation Failure",
        "short_description": "DXVK could not compile or cache a shader.",
        "icon": "dxvk",
    },
    "DIRECTX11_RELATED": {
        "display_name": "DirectX 11 Issue",
        "short_description": "A DirectX 11 related error was detected (handled by DXVK).",
        "icon": "dxvk",
    },

    # ---- VKD3D ----
    "VKD3D_RELATED_FAILURE": {
        "display_name": "VKD3D Failure",
        "short_description": "DirectX 12 translation through VKD3D-Proton failed.",
        "icon": "vkd3d",
    },
    "VKD3D_PROTON_FAILURE": {
        "display_name": "VKD3D-Proton Failure",
        "short_description": "VKD3D-Proton failed while handling DirectX 12 translation.",
        "icon": "vkd3d",
    },
    "DIRECTX12_RELATED": {
        "display_name": "DirectX 12 Issue",
        "short_description": "A DirectX 12 related error was detected (handled by VKD3D-Proton).",
        "icon": "vkd3d",
    },

    # ---- AMD ----
    "AMDGPU_RESET": {
        "display_name": "AMD GPU Reset",
        "short_description": "The AMD GPU driver triggered a recovery reset after a hang.",
        "icon": "gpu",
    },
    "AMDGPU_RING_TIMEOUT": {
        "display_name": "AMD GPU Ring Timeout",
        "short_description": "The AMD GPU graphics command ring timed out.",
        "icon": "gpu",
    },
    "RADV_RELATED_FAILURE": {
        "display_name": "RADV (AMD Vulkan) Issue",
        "short_description": "The RADV Mesa Vulkan driver for AMD GPUs reported a problem.",
        "icon": "gpu",
    },
    "AMDGPU_FIRMWARE_MISSING": {
        "display_name": "AMD GPU Firmware Missing",
        "short_description": "The AMD GPU driver could not load required firmware files.",
        "icon": "gpu",
    },
    "AMDGPU_INIT_FAILURE": {
        "display_name": "AMD GPU Initialization Failure",
        "short_description": "The AMD GPU driver failed during initialization.",
        "icon": "gpu",
    },

    # ---- NVIDIA ----
    "NVIDIA_DRIVER_RELATED": {
        "display_name": "NVIDIA Driver Issue",
        "short_description": "The NVIDIA driver encountered a compatibility or load problem.",
        "icon": "gpu",
    },
    "NVIDIA_ICD_RELATED": {
        "display_name": "NVIDIA Vulkan ICD Issue",
        "short_description": "The NVIDIA Vulkan ICD file is missing or not loaded correctly.",
        "icon": "gpu",
    },
    "NVIDIA_GPU_HANG": {
        "display_name": "NVIDIA GPU Hang (XID Error)",
        "short_description": "The NVIDIA driver reported a GPU hang or XID critical error.",
        "icon": "gpu",
    },
    "NVIDIA_GL_LIBRARY_RELATED": {
        "display_name": "NVIDIA Library Issue",
        "short_description": "An NVIDIA OpenGL or Vulkan shared library could not be loaded.",
        "icon": "gpu",
    },
    "NVIDIA_PRIME_RELATED": {
        "display_name": "NVIDIA PRIME/Optimus Issue",
        "short_description": "NVIDIA PRIME render offload or Optimus GPU switching had a problem.",
        "icon": "gpu",
    },

    # ---- Anti-cheat ----
    "EAC_FAILURE": {
        "display_name": "Easy Anti-Cheat Failure",
        "short_description": "Easy Anti-Cheat failed to initialize or blocked the game.",
        "icon": "anticheat",
    },
    "EAC_EOS_RELATED": {
        "display_name": "EAC Epic Online Services Issue",
        "short_description": "The Easy Anti-Cheat EOS component failed.",
        "icon": "anticheat",
    },
    "EAC_LINUX_RUNTIME_RELATED": {
        "display_name": "EAC Linux Runtime",
        "short_description": "The native Linux Easy Anti-Cheat runtime was detected.",
        "icon": "anticheat",
    },
    "BATTLEYE_FAILURE": {
        "display_name": "BattlEye Failure",
        "short_description": "BattlEye anti-cheat failed to initialize or blocked the game.",
        "icon": "anticheat",
    },
    "BATTLEYE_LAUNCHER_RELATED": {
        "display_name": "BattlEye Launcher Issue",
        "short_description": "The BattlEye launcher component encountered a problem.",
        "icon": "anticheat",
    },

    # ---- Proton / Wine prefix ----
    "PROTON_PREFIX_CORRUPTED": {
        "display_name": "Corrupted Proton Prefix",
        "short_description": "The Proton/Wine prefix is damaged or missing critical files.",
        "icon": "proton",
    },
    "PROTON_PREFIX_PERMISSION_ISSUE": {
        "display_name": "Proton Prefix Permission Issue",
        "short_description": "Proton does not have permission to read or write its prefix.",
        "icon": "permissions",
    },
    "PROTON_WINEBOOT_FAILURE": {
        "display_name": "Proton Wineboot Failed",
        "short_description": "Wineboot failed during Proton prefix setup or update.",
        "icon": "proton",
    },
    "WINEBOOT_EXECUTION_FAILURE": {
        "display_name": "Wineboot Execution Failure",
        "short_description": "The wineboot process failed to run during prefix initialization.",
        "icon": "proton",
    },
    "PROTON_DLL_MISSING": {
        "display_name": "Missing DLL",
        "short_description": "Proton or Wine could not load a required Windows DLL.",
        "icon": "proton",
    },
    "PROTON_REGISTRY_FAILURE": {
        "display_name": "Wine Registry Failure",
        "short_description": "Wine could not open or write a required registry key.",
        "icon": "proton",
    },
    "KERNEL32_RELATED_FAILURE": {
        "display_name": "Kernel32 Failure",
        "short_description": "kernel32.dll, a core Windows component, failed to load.",
        "icon": "proton",
    },
    "WINE_CRASH": {
        "display_name": "Wine/Proton Crash",
        "short_description": "Wine or Proton crashed while running the game.",
        "icon": "proton",
    },
    "NTDLL_RELATED_CRASH": {
        "display_name": "ntdll Crash",
        "short_description": "A crash involving ntdll, a core Wine compatibility component.",
        "icon": "proton",
    },
    "MEDIA_FOUNDATION_RELATED": {
        "display_name": "Windows Media Foundation Missing",
        "short_description": "The game requires Windows Media Foundation for video or audio playback.",
        "icon": "proton",
    },
    "WINDOWS_MEDIA_COMPONENT_RELATED": {
        "display_name": "Windows Media Component Missing",
        "short_description": "A Windows media DLL required by the game is not available.",
        "icon": "proton",
    },
    "PROTON_XINPUT_FAILURE": {
        "display_name": "XInput Controller Issue",
        "short_description": "Proton could not initialize XInput for controller support.",
        "icon": "proton",
    },
    "SETUPAPI_RELATED": {
        "display_name": "Windows Setup API Issue",
        "short_description": "Wine SetupAPI was involved in a failure during game or launcher setup.",
        "icon": "proton",
    },

    # ---- Memory ----
    "OUT_OF_MEMORY": {
        "display_name": "Out of System Memory",
        "short_description": "The system or game ran out of available RAM or swap space.",
        "icon": "memory",
    },
    "OOM_KILLER_TRIGGERED": {
        "display_name": "OOM Killer Triggered",
        "short_description": "The Linux kernel OOM killer terminated a process due to memory exhaustion.",
        "icon": "memory",
    },
    "MEMORY_ALLOCATION_FAILURE": {
        "display_name": "Memory Allocation Failure",
        "short_description": "A memory allocation call failed — RAM or swap is exhausted.",
        "icon": "memory",
    },

    # ---- Storage ----
    "DISK_FULL": {
        "display_name": "Disk Full",
        "short_description": "The drive does not have enough free space for the game or Steam.",
        "icon": "storage",
    },
    "READ_ONLY_FILESYSTEM": {
        "display_name": "Read-Only Filesystem",
        "short_description": "The game or Steam tried to write to a read-only filesystem.",
        "icon": "storage",
    },
    "FILESYSTEM_IO_ERROR": {
        "display_name": "Filesystem I/O Error",
        "short_description": "A disk read or write error was detected — possible drive failure.",
        "icon": "storage",
    },
    "STEAM_DISK_WRITE_ERROR": {
        "display_name": "Steam Disk Write Error",
        "short_description": "Steam could not write files to the game install location.",
        "icon": "storage",
    },
    "MISSING_FILE": {
        "display_name": "Missing File",
        "short_description": "A required file or path referenced in the log does not exist.",
        "icon": "storage",
    },

    # ---- Library mismatches ----
    "MISSING_SHARED_LIBRARY": {
        "display_name": "Missing Shared Library",
        "short_description": "A required Linux shared library (.so file) could not be found.",
        "icon": "proton",
    },
    "WRONG_ARCH_LIBRARY": {
        "display_name": "Architecture Mismatch",
        "short_description": "A library with the wrong architecture (32-bit vs 64-bit) was loaded.",
        "icon": "proton",
    },

    # ---- Gamescope ----
    "GAMESCOPE_VULKAN_INIT_FAILURE": {
        "display_name": "Gamescope Vulkan Failure",
        "short_description": "Gamescope could not initialize Vulkan.",
        "icon": "gamescope",
    },
    "GAMESCOPE_SWAPCHAIN_FAILURE": {
        "display_name": "Gamescope Swapchain Failure",
        "short_description": "Gamescope could not create a Vulkan swapchain for display output.",
        "icon": "gamescope",
    },
    "GAMESCOPE_OUTPUT_FAILURE": {
        "display_name": "Gamescope Output Failure",
        "short_description": "Gamescope failed to create its display output.",
        "icon": "gamescope",
    },
    "GAMESCOPE_WAYLAND_RELATED": {
        "display_name": "Gamescope Wayland Issue",
        "short_description": "Gamescope had a problem with the Wayland compositor.",
        "icon": "gamescope",
    },
    "GAMESCOPE_FAILURE": {
        "display_name": "Gamescope Failure",
        "short_description": "Gamescope reported an error or exited unexpectedly.",
        "icon": "gamescope",
    },

    # ---- Steam / runtime ----
    "STEAM_API_INIT_FAILURE": {
        "display_name": "Steam API Initialization Failed",
        "short_description": "The game could not initialize the Steam API.",
        "icon": "steam",
    },
    "STEAM_RUNTIME_FAILURE": {
        "display_name": "Steam Runtime Failure",
        "short_description": "The Steam Runtime had a failure that may have prevented the game from launching.",
        "icon": "steam",
    },
    "STEAM_LINUX_RUNTIME_RELATED": {
        "display_name": "Steam Linux Runtime Issue",
        "short_description": "Steam Linux Runtime appeared in the log and may be involved in the failure.",
        "icon": "steam",
    },
    "PRESSURE_VESSEL_RELATED": {
        "display_name": "Pressure Vessel Issue",
        "short_description": "Pressure Vessel (Steam's container runtime) appeared in the log.",
        "icon": "steam",
    },
    "STEAM_CLOUD_RELATED": {
        "display_name": "Steam Cloud Issue",
        "short_description": "Steam Cloud sync may be delaying or blocking the game launch.",
        "icon": "steam",
    },
    "STEAM_SHADER_CACHE_RELATED": {
        "display_name": "Steam Shader Cache Issue",
        "short_description": "Steam shader pre-caching appeared in the log.",
        "icon": "steam",
    },

    # ---- Audio ----
    "XAUDIO_RELATED": {
        "display_name": "XAudio2 Issue",
        "short_description": "XAudio2, the Windows audio component, encountered a problem.",
        "icon": "audio",
    },
    "FAUDIO_RELATED": {
        "display_name": "FAudio Issue",
        "short_description": "FAudio (XAudio compatibility layer) encountered a problem.",
        "icon": "audio",
    },
    "PULSEAUDIO_RELATED": {
        "display_name": "PulseAudio/PipeWire Audio Issue",
        "short_description": "The audio server reported a problem with audio routing.",
        "icon": "audio",
    },
    "ALSA_AUDIO_FAILURE": {
        "display_name": "ALSA Audio Failure",
        "short_description": "ALSA reported an audio device error.",
        "icon": "audio",
    },
    "OPENAL_AUDIO_FAILURE": {
        "display_name": "OpenAL Audio Failure",
        "short_description": "OpenAL could not initialize or find an audio device.",
        "icon": "audio",
    },

    # ---- GameMode / overlays ----
    "GAMEMODE_DAEMON_RELATED": {
        "display_name": "GameMode Daemon Unavailable",
        "short_description": "The GameMode background service is missing or not responding.",
        "icon": "gamemode",
    },
    "GAMEMODE_REQUEST_FAILURE": {
        "display_name": "GameMode Request Failed",
        "short_description": "The game or launcher tried to activate GameMode but the request failed.",
        "icon": "gamemode",
    },
    "GAMEMODE_RELATED": {
        "display_name": "GameMode Issue",
        "short_description": "GameMode reported a problem or failed to apply optimizations.",
        "icon": "gamemode",
    },
    "PKEXEC_PERMISSION_ISSUE": {
        "display_name": "Permission Prompt Issue",
        "short_description": "A privileged helper failed because authorization was denied.",
        "icon": "permissions",
    },
    "MANGOHUD_CONFIG_RELATED": {
        "display_name": "MangoHud Config Issue",
        "short_description": "MangoHud configuration appears invalid or broken.",
        "icon": "mangohud",
    },
    "MANGOHUD_FAILURE": {
        "display_name": "MangoHud Failure",
        "short_description": "MangoHud failed to load or attach correctly.",
        "icon": "mangohud",
    },

    # ---- Crashes (secondary) ----
    "SEGFAULT": {
        "display_name": "Segmentation Fault",
        "short_description": "The game or a related process crashed with a segmentation fault.",
        "icon": "crash",
    },
    "CORE_DUMPED": {
        "display_name": "Core Dump",
        "short_description": "The game or a related process crashed and produced a core dump.",
        "icon": "crash",
    },
    "PERMISSION_DENIED": {
        "display_name": "Permission Denied",
        "short_description": "A file or resource access was denied due to insufficient permissions.",
        "icon": "permissions",
    },
    "MISSING_FILE": {
        "display_name": "Missing File",
        "short_description": "A file or path referenced in the log does not exist.",
        "icon": "storage",
    },
    "WINEPREFIX_RELATED": {
        "display_name": "Wine Prefix Issue",
        "short_description": "A Wine or Proton prefix-related error was detected.",
        "icon": "proton",
    },
    "PROTON_EXPERIMENTAL_USED": {
        "display_name": "Proton Experimental",
        "short_description": "The game is using Proton Experimental.",
        "icon": "proton",
    },
    "GE_PROTON_USED": {
        "display_name": "GE-Proton",
        "short_description": "The game is using GE-Proton.",
        "icon": "proton",
    },
}


def get_fingerprint_metadata(fingerprint: str) -> dict:
    return FINGERPRINT_METADATA.get(
        fingerprint,
        {
            "display_name": fingerprint.replace("_", " ").title(),
            "short_description": "No display metadata has been added for this fingerprint yet.",
            "icon": "unknown",
        },
    )
