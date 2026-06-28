ROOT_CAUSE_GRAPH = {
    "VULKAN_DRIVER_MISSING": [
        "VULKAN_INIT_FAILURE",
        "DXVK_ADAPTER_FAILURE",
        "DXVK_RELATED_FAILURE",
        "VKD3D_RELATED_FAILURE",
        "VKD3D_PROTON_FAILURE",
        "GAMESCOPE_VULKAN_INIT_FAILURE",
    ],

    "VULKAN_INIT_FAILURE": [
        "DXVK_ADAPTER_FAILURE",
        "DXVK_RELATED_FAILURE",
        "VKD3D_RELATED_FAILURE",
        "GAMESCOPE_FAILURE",
    ],

    "DXVK_ADAPTER_FAILURE": [
        "DXVK_RELATED_FAILURE",
        "DXVK_D3D11_FAILURE",
        "DIRECTX11_RELATED",
    ],

    "VKD3D_RELATED_FAILURE": [
        "VKD3D_PROTON_FAILURE",
        "DIRECTX12_RELATED",
    ],

    "GAMEMODE_DAEMON_RELATED": [
        "GAMEMODE_REQUEST_FAILURE",
        "GAMEMODE_RELATED",
        "PKEXEC_PERMISSION_ISSUE",
    ],

    "MANGOHUD_CONFIG_RELATED": [
        "MANGOHUD_FAILURE",
    ],

    "PROTON_PREFIX_CORRUPTED": [
        "PROTON_WINEBOOT_FAILURE",
        "PROTON_REGISTRY_FAILURE",
        "WINEBOOT_EXECUTION_FAILURE",
        "WINE_CRASH",
    ],

    "PROTON_PREFIX_PERMISSION_ISSUE": [
        "PERMISSION_DENIED",
        "PROTON_WINEBOOT_FAILURE",
        "WINEBOOT_EXECUTION_FAILURE",
    ],

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

    "OUT_OF_MEMORY": [
        "MEMORY_ALLOCATION_FAILURE",
        "VK_ERROR_OUT_OF_DEVICE_MEMORY",
        "WINE_CRASH",
        "CORE_DUMPED",
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
