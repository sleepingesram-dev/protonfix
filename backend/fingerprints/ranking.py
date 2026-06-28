from typing import Any


ROOT_CAUSE_PRIORITY = {
    # Vulkan / GPU
    "VULKAN_DRIVER_MISSING": 100,
    "VULKAN_INIT_FAILURE": 98,
    "GAMESCOPE_VULKAN_INIT_FAILURE": 97,
    "VK_ERROR_EXTENSION_NOT_PRESENT": 96,
    "VK_ERROR_DEVICE_LOST": 94,
    "VK_ERROR_OUT_OF_DEVICE_MEMORY": 94,
    "VULKAN_ICD_RELATED": 92,

    # Storage / filesystem
    "DISK_FULL": 95,
    "READ_ONLY_FILESYSTEM": 95,
    "PERMISSION_DENIED": 90,
    "STEAM_DISK_WRITE_ERROR": 88,

    # Anti-cheat
    "EAC_FAILURE": 90,
    "BATTLEYE_FAILURE": 90,

    # Proton / Wine prefix
    "PROTON_PREFIX_CORRUPTED": 88,
    "PROTON_PREFIX_PERMISSION_ISSUE": 87,
    "PROTON_DLL_MISSING": 84,
    "WINEBOOT_EXECUTION_FAILURE": 82,

    # DXVK / VKD3D
    "DXVK_ADAPTER_FAILURE": 80,
    "DXVK_RELATED_FAILURE": 75,
    "VKD3D_RELATED_FAILURE": 75,

    # Gamescope
    "GAMESCOPE_FAILURE": 78,
    "GAMESCOPE_WAYLAND_RELATED": 72,

    # Crashes, often secondary
    "WINE_CRASH": 60,
    "SEGFAULT": 58,
    "CORE_DUMPED": 55,

    # Warnings / non-fatal helpers
    "GAMEMODE_RELATED": 35,
    "GAMEMODE_DAEMON_RELATED": 35,
    "GAMEMODE_REQUEST_FAILURE": 35,
    "PKEXEC_PERMISSION_ISSUE": 30,
    "MANGOHUD_FAILURE": 25,
    "MANGOHUD_CONFIG_RELATED": 20,
}


CATEGORY_PRIORITY = {
    "Graphics Driver": 90,
    "Vulkan": 90,
    "Gamescope": 80,
    "Anti-Cheat": 78,
    "Storage": 75,
    "Filesystem": 75,
    "DXVK": 65,
    "VKD3D": 65,
    "Proton": 60,
    "Wine": 55,
    "Steam": 50,
    "GameMode": 25,
    "MangoHud": 20,
}


SEVERITY_PRIORITY = {
    "high": 30,
    "medium": 15,
    "low": 5,
}


def get_root_cause_score(item: dict[str, Any]) -> int:
    fingerprint = item.get("fingerprint")
    category = item.get("category")
    severity = str(item.get("severity", "low")).lower()
    confidence = int(item.get("confidence", 0) or 0)

    fingerprint_score = ROOT_CAUSE_PRIORITY.get(fingerprint, 50)
    category_score = CATEGORY_PRIORITY.get(category, 40)
    severity_score = SEVERITY_PRIORITY.get(severity, 5)

    return fingerprint_score + category_score + severity_score + confidence


def rank_fingerprints(fingerprints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = []

    for item in fingerprints:
        ranked_item = item.copy()
        ranked_item["root_cause_score"] = get_root_cause_score(item)
        ranked.append(ranked_item)

    ranked.sort(
        key=lambda item: item.get("root_cause_score", 0),
        reverse=True,
    )

    return ranked


def get_primary_fingerprint(
    fingerprints: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not fingerprints:
        return None

    ranked = rank_fingerprints(fingerprints)
    return ranked[0]
