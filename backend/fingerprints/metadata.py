FINGERPRINT_METADATA = {
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
    "DXVK_ADAPTER_FAILURE": {
        "display_name": "DXVK Could Not Find GPU Adapter",
        "short_description": "DXVK could not detect or use a compatible Vulkan adapter.",
        "icon": "dxvk",
    },
    "DXVK_RELATED_FAILURE": {
        "display_name": "DXVK Failure",
        "short_description": "DirectX-to-Vulkan translation failed or reported errors.",
        "icon": "dxvk",
    },
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
    "GAMESCOPE_VULKAN_INIT_FAILURE": {
        "display_name": "Gamescope Vulkan Failure",
        "short_description": "Gamescope could not initialize Vulkan.",
        "icon": "gamescope",
    },
    "GAMEMODE_DAEMON_RELATED": {
        "display_name": "GameMode Daemon Issue",
        "short_description": "The GameMode background service appears unavailable or broken.",
        "icon": "gamemode",
    },
    "GAMEMODE_REQUEST_FAILURE": {
        "display_name": "GameMode Request Failed",
        "short_description": "The game or launcher requested GameMode, but the request failed.",
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
    "PROTON_PREFIX_CORRUPTED": {
        "display_name": "Corrupted Proton Prefix",
        "short_description": "The Proton/Wine prefix may be damaged or inconsistent.",
        "icon": "proton",
    },
    "PROTON_PREFIX_PERMISSION_ISSUE": {
        "display_name": "Proton Prefix Permission Issue",
        "short_description": "Proton may not have permission to read or write its prefix.",
        "icon": "permissions",
    },
    "DISK_FULL": {
        "display_name": "Disk Full",
        "short_description": "The drive does not have enough free space.",
        "icon": "storage",
    },
    "READ_ONLY_FILESYSTEM": {
        "display_name": "Read-Only Filesystem",
        "short_description": "The game or Steam is trying to write to a read-only location.",
        "icon": "storage",
    },
    "OUT_OF_MEMORY": {
        "display_name": "Out of Memory",
        "short_description": "The system or GPU ran out of available memory.",
        "icon": "memory",
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
