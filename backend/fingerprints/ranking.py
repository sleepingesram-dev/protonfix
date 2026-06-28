from typing import Any


ROOT_CAUSE_PRIORITY = {
    # ---- Vulkan / GPU driver ----
    "VULKAN_DRIVER_MISSING": 100,
    "VULKAN_INIT_FAILURE": 98,
    "GAMESCOPE_VULKAN_INIT_FAILURE": 97,
    "VK_ERROR_EXTENSION_NOT_PRESENT": 96,
    "VK_ERROR_DEVICE_LOST": 94,
    "VK_ERROR_OUT_OF_DEVICE_MEMORY": 94,
    "VK_ERROR_OUT_OF_HOST_MEMORY": 93,
    "VULKAN_ICD_RELATED": 92,

    # ---- Storage / filesystem ----
    "DISK_FULL": 95,
    "READ_ONLY_FILESYSTEM": 95,
    "FILESYSTEM_IO_ERROR": 91,
    "PERMISSION_DENIED": 90,
    "STEAM_DISK_WRITE_ERROR": 88,

    # ---- Anti-cheat ----
    "EAC_FAILURE": 90,
    "BATTLEYE_FAILURE": 90,
    "EAC_EOS_RELATED": 89,
    "EAC_LINUX_RUNTIME_RELATED": 89,
    "BATTLEYE_LAUNCHER_RELATED": 89,

    # ---- AMD driver ----
    "AMDGPU_RING_TIMEOUT": 92,
    "AMDGPU_RESET": 91,
    "AMDGPU_FIRMWARE_MISSING": 90,
    "AMDGPU_INIT_FAILURE": 89,
    "RADV_RELATED_FAILURE": 85,

    # ---- NVIDIA driver ----
    "NVIDIA_GPU_HANG": 92,
    "NVIDIA_ICD_RELATED": 91,
    "NVIDIA_DRIVER_RELATED": 86,
    "NVIDIA_GL_LIBRARY_RELATED": 83,
    "NVIDIA_PRIME_RELATED": 70,

    # ---- Memory ----
    "OOM_KILLER_TRIGGERED": 93,
    "OUT_OF_MEMORY": 91,
    "MEMORY_ALLOCATION_FAILURE": 88,

    # ---- Proton / Wine prefix ----
    "PROTON_PREFIX_CORRUPTED": 88,
    "PROTON_PREFIX_PERMISSION_ISSUE": 87,
    "MEDIA_FOUNDATION_RELATED": 90,
    "PROTON_DLL_MISSING": 84,
    "PROTON_WINEBOOT_FAILURE": 83,
    "WINEBOOT_EXECUTION_FAILURE": 82,
    "PROTON_REGISTRY_FAILURE": 78,
    "KERNEL32_RELATED_FAILURE": 80,
    "WRONG_ARCH_LIBRARY": 79,
    "MISSING_SHARED_LIBRARY": 76,

    # ---- DXVK / VKD3D ----
    "DXVK_ADAPTER_FAILURE": 80,
    "DXVK_GENERAL_FAILURE": 77,
    "DXVK_D3D11_FAILURE": 76,
    "DXVK_SHADER_COMPILE_FAILURE": 74,
    "DXVK_RELATED_FAILURE": 75,
    "VKD3D_RELATED_FAILURE": 75,
    "VKD3D_PROTON_FAILURE": 74,
    "DIRECTX12_RELATED": 65,
    "DIRECTX11_RELATED": 55,

    # ---- Gamescope ----
    "GAMESCOPE_OUTPUT_FAILURE": 80,
    "GAMESCOPE_SWAPCHAIN_FAILURE": 79,
    "GAMESCOPE_FAILURE": 78,
    "GAMESCOPE_WAYLAND_RELATED": 72,

    # ---- Steam ----
    "STEAM_RUNTIME_FAILURE": 72,
    "STEAM_LINUX_RUNTIME_RELATED": 70,
    "PRESSURE_VESSEL_RELATED": 68,
    "STEAM_API_INIT_FAILURE": 65,

    # ---- Crashes (usually secondary) ----
    "WINE_CRASH": 60,
    "NTDLL_RELATED_CRASH": 59,
    "SEGFAULT": 58,
    "CORE_DUMPED": 55,

    # ---- Audio ----
    "XAUDIO_RELATED": 50,
    "FAUDIO_RELATED": 48,
    "ALSA_AUDIO_FAILURE": 40,
    "PULSEAUDIO_RELATED": 38,
    "OPENAL_AUDIO_FAILURE": 36,

    # ---- Non-fatal helpers ----
    "PROTON_XINPUT_FAILURE": 35,
    "GAMEMODE_RELATED": 35,
    "GAMEMODE_DAEMON_RELATED": 35,
    "GAMEMODE_REQUEST_FAILURE": 35,
    "PKEXEC_PERMISSION_ISSUE": 30,
    "MANGOHUD_FAILURE": 25,
    "MANGOHUD_CONFIG_RELATED": 20,
    "WINDOWS_MEDIA_COMPONENT_RELATED": 50,
}


CATEGORY_PRIORITY = {
    "Graphics Driver": 90,
    "Vulkan": 90,
    "AMD Driver": 88,
    "AMD Vulkan": 85,
    "NVIDIA Driver": 88,
    "NVIDIA Vulkan": 88,
    "Gamescope": 80,
    "Anti-Cheat": 78,
    "Storage": 75,
    "Filesystem": 75,
    "Memory": 73,
    "DXVK": 65,
    "VKD3D": 65,
    "Media Foundation": 65,
    "Proton Prefix": 62,
    "Proton Dependency": 60,
    "Registry": 58,
    "Missing Library": 58,
    "Library Mismatch": 58,
    "Windows Runtime": 55,
    "Proton": 60,
    "Wine": 55,
    "Steam Runtime": 55,
    "Steam Storage": 52,
    "Steam": 50,
    "Audio": 45,
    "GameMode": 25,
    "MangoHud": 20,
    "Performance Overlay": 20,
    "Proton Version": 15,
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
