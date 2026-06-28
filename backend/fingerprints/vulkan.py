from fingerprints.models import FingerprintDefinition


VULKAN_FINGERPRINTS = [
    FingerprintDefinition(
        id="VULKAN_DRIVER_MISSING",
        display_name="Missing Vulkan Driver",
        short_description="Vulkan could not find a working graphics driver.",
        category="Graphics Driver",
        severity="high",
        patterns=[
            "vk_error_incompatible_driver",
            "failed to create vulkan instance",
        ],
        causes=[
            "VULKAN_INIT_FAILURE",
            "DXVK_ADAPTER_FAILURE",
            "DXVK_RELATED_FAILURE",
            "VKD3D_RELATED_FAILURE",
            "VKD3D_PROTON_FAILURE",
            "GAMESCOPE_VULKAN_INIT_FAILURE",
        ],
        known_fix=[
            "Install or reinstall the Vulkan driver for your GPU.",
            "For AMD GPUs on Arch/CachyOS, install mesa, vulkan-radeon, and vulkan-tools.",
            "Reboot after updating graphics packages.",
            "Run vulkaninfo to confirm Vulkan is working.",
        ],
        safe_commands=[
            "sudo pacman -Syu mesa vulkan-radeon vulkan-tools",
            "vulkaninfo",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="VULKAN_INIT_FAILURE",
        display_name="Vulkan Initialization Failed",
        short_description="The game or compatibility layer failed to initialize Vulkan.",
        category="Graphics Driver",
        severity="high",
        patterns=[
            "vulkan initialization failed",
            "failed to initialize vulkan",
        ],
        causes=[
            "DXVK_ADAPTER_FAILURE",
            "DXVK_RELATED_FAILURE",
            "VKD3D_RELATED_FAILURE",
            "GAMESCOPE_FAILURE",
        ],
        known_fix=[
            "Verify Vulkan works outside the game.",
            "Update Mesa or your GPU driver.",
            "Try launching the game without overlays or Gamescope.",
        ],
        safe_commands=[
            "vulkaninfo",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="VK_ERROR_EXTENSION_NOT_PRESENT",
        display_name="Missing Vulkan Extension",
        short_description="A required Vulkan extension is missing or unavailable.",
        category="Graphics Driver",
        severity="high",
        patterns=[
            "VK_ERROR_EXTENSION_NOT_PRESENT",
        ],
        causes=[
            "GAMESCOPE_VULKAN_INIT_FAILURE",
            "DXVK_ADAPTER_FAILURE",
            "DXVK_RELATED_FAILURE",
        ],
        known_fix=[
            "Update Mesa or your GPU driver.",
            "Disable Gamescope and test the game directly.",
            "Check whether your GPU supports the required Vulkan extension.",
        ],
        safe_commands=[
            "vulkaninfo | grep extension",
        ],
        icon="gpu",
    ),
]
