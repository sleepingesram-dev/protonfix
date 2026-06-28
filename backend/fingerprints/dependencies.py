ROOT_CAUSE_GRAPH = {

    # ---- Vulkan / GPU driver chains ----
    "VULKAN_DRIVER_MISSING": [
        "VULKAN_INIT_FAILURE",
        "DXVK_ADAPTER_FAILURE",
        "DXVK_RELATED_FAILURE",
        "DXVK_GENERAL_FAILURE",
        "VKD3D_RELATED_FAILURE",
        "VKD3D_PROTON_FAILURE",
        "GAMESCOPE_VULKAN_INIT_FAILURE",
    ],

    "VULKAN_INIT_FAILURE": [
        "DXVK_ADAPTER_FAILURE",
        "DXVK_RELATED_FAILURE",
        "VKD3D_RELATED_FAILURE",
        "GAMESCOPE_FAILURE",
        "GAMESCOPE_VULKAN_INIT_FAILURE",
    ],

    "VK_ERROR_EXTENSION_NOT_PRESENT": [
        "DXVK_ADAPTER_FAILURE",
        "DXVK_RELATED_FAILURE",
        "GAMESCOPE_VULKAN_INIT_FAILURE",
    ],

    "VK_ERROR_DEVICE_LOST": [
        "WINE_CRASH",
        "CORE_DUMPED",
        "DXVK_GENERAL_FAILURE",
    ],

    # ---- DXVK chains ----
    "DXVK_ADAPTER_FAILURE": [
        "DXVK_RELATED_FAILURE",
        "DXVK_GENERAL_FAILURE",
        "DXVK_D3D11_FAILURE",
        "DIRECTX11_RELATED",
    ],

    "DXVK_GENERAL_FAILURE": [
        "DXVK_D3D11_FAILURE",
        "WINE_CRASH",
    ],

    # ---- VKD3D chains ----
    "VKD3D_RELATED_FAILURE": [
        "VKD3D_PROTON_FAILURE",
        "DIRECTX12_RELATED",
    ],

    # ---- AMD driver chains ----
    "AMDGPU_RING_TIMEOUT": [
        "AMDGPU_RESET",
        "VK_ERROR_DEVICE_LOST",
        "WINE_CRASH",
    ],

    "AMDGPU_RESET": [
        "VK_ERROR_DEVICE_LOST",
        "WINE_CRASH",
        "CORE_DUMPED",
    ],

    "RADV_RELATED_FAILURE": [
        "VULKAN_INIT_FAILURE",
        "DXVK_ADAPTER_FAILURE",
    ],

    "AMDGPU_FIRMWARE_MISSING": [
        "AMDGPU_INIT_FAILURE",
        "VULKAN_DRIVER_MISSING",
    ],

    # ---- NVIDIA driver chains ----
    "NVIDIA_ICD_RELATED": [
        "VULKAN_DRIVER_MISSING",
        "VULKAN_INIT_FAILURE",
    ],

    "NVIDIA_GPU_HANG": [
        "VK_ERROR_DEVICE_LOST",
        "WINE_CRASH",
        "CORE_DUMPED",
    ],

    # ---- Proton prefix chains ----
    "PROTON_PREFIX_CORRUPTED": [
        "PROTON_WINEBOOT_FAILURE",
        "PROTON_REGISTRY_FAILURE",
        "WINEBOOT_EXECUTION_FAILURE",
        "WINE_CRASH",
        "NTDLL_RELATED_CRASH",
    ],

    "PROTON_PREFIX_PERMISSION_ISSUE": [
        "PERMISSION_DENIED",
        "PROTON_WINEBOOT_FAILURE",
        "WINEBOOT_EXECUTION_FAILURE",
    ],

    "PROTON_DLL_MISSING": [
        "WINE_CRASH",
        "NTDLL_RELATED_CRASH",
    ],

    "MEDIA_FOUNDATION_RELATED": [
        "PROTON_DLL_MISSING",
        "WINE_CRASH",
    ],

    # ---- Storage chains ----
    "DISK_FULL": [
        "STEAM_DISK_WRITE_ERROR",
        "FILESYSTEM_IO_ERROR",
        "PROTON_PREFIX_CORRUPTED",
    ],

    "READ_ONLY_FILESYSTEM": [
        "STEAM_DISK_WRITE_ERROR",
        "FILESYSTEM_IO_ERROR",
        "PERMISSION_DENIED",
    ],

    # ---- Memory chains ----
    "OUT_OF_MEMORY": [
        "MEMORY_ALLOCATION_FAILURE",
        "VK_ERROR_OUT_OF_DEVICE_MEMORY",
        "VK_ERROR_OUT_OF_HOST_MEMORY",
        "WINE_CRASH",
        "CORE_DUMPED",
    ],

    "OOM_KILLER_TRIGGERED": [
        "MEMORY_ALLOCATION_FAILURE",
        "VK_ERROR_OUT_OF_DEVICE_MEMORY",
        "WINE_CRASH",
        "CORE_DUMPED",
    ],

    # ---- Gamescope chains ----
    "GAMESCOPE_VULKAN_INIT_FAILURE": [
        "GAMESCOPE_SWAPCHAIN_FAILURE",
        "GAMESCOPE_OUTPUT_FAILURE",
        "WINE_CRASH",
    ],

    "GAMESCOPE_FAILURE": [
        "GAMESCOPE_SWAPCHAIN_FAILURE",
        "WINE_CRASH",
    ],

    # ---- Anti-cheat chains ----
    "EAC_FAILURE": [
        "EAC_EOS_RELATED",
        "EAC_LINUX_RUNTIME_RELATED",
    ],

    # ---- GameMode / overlay chains ----
    "GAMEMODE_DAEMON_RELATED": [
        "GAMEMODE_REQUEST_FAILURE",
        "GAMEMODE_RELATED",
        "PKEXEC_PERMISSION_ISSUE",
    ],

    "MANGOHUD_CONFIG_RELATED": [
        "MANGOHUD_FAILURE",
    ],
}


def build_dependency_chain(
    fingerprints: list[dict],
    primary_fingerprint: dict | None = None,
) -> list[str]:
    detected = {
        item.get("fingerprint")
        for item in fingerprints
        if item.get("fingerprint")
    }

    if not detected:
        return []

    primary_id = None

    if primary_fingerprint:
        primary_id = primary_fingerprint.get("fingerprint")

    if primary_id:
        chain = [primary_id]

        for child in ROOT_CAUSE_GRAPH.get(primary_id, []):
            if child in detected:
                chain.append(child)

        return chain

    ranked_fingerprints = [
        item.get("fingerprint")
        for item in fingerprints
        if item.get("fingerprint")
    ]

    return ranked_fingerprints
