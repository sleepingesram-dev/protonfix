from fingerprints.models import FingerprintDefinition


GAMESCOPE_FINGERPRINTS = [

    FingerprintDefinition(
        id="GAMESCOPE_VULKAN_INIT_FAILURE",
        display_name="Gamescope Vulkan Failure",
        short_description="Gamescope could not initialize Vulkan.",
        category="Gamescope",
        severity="high",
        patterns=[
            "vcreatedevice failed",
            "gamescope: vcreateinstance failed",
            "gamescope: vkcreatedevice failed",
            "gamescope: failed to initialize vulkan",
            "gamescope: vulkan error",
            "gamescope: no vulkan device found",
            "gamescope: failed to create vulkan instance",
        ],
        caused_by=["VULKAN_DRIVER_MISSING", "VULKAN_INIT_FAILURE"],
        known_fix=[
            "Fix Vulkan first — run vulkaninfo and confirm it works outside Gamescope.",
            "Update Gamescope, Mesa, and Vulkan packages.",
            "Try launching the game without Gamescope.",
        ],
        safe_commands=[
            "vulkaninfo",
            "gamescope --version",
        ],
        icon="gamescope",
    ),

    FingerprintDefinition(
        id="GAMESCOPE_SWAPCHAIN_FAILURE",
        display_name="Gamescope Swapchain Failure",
        short_description="Gamescope could not create a Vulkan swapchain for display output.",
        category="Gamescope",
        severity="high",
        patterns=[
            "failed to create swapchain",
            "gamescope: swapchain error",
            "gamescope: failed to create swapchain",
            "vk_error_native_window_in_use",
            "swapchain creation failed",
        ],
        caused_by=["GAMESCOPE_VULKAN_INIT_FAILURE"],
        known_fix=[
            "Try launching without HDR or VRR Gamescope options.",
            "Use a simpler Gamescope command (e.g., gamescope -w 1920 -h 1080 -f).",
            "Update Gamescope and Vulkan drivers.",
            "Test whether the game works without Gamescope.",
        ],
        safe_commands=["gamescope --version"],
        icon="gamescope",
    ),

    FingerprintDefinition(
        id="GAMESCOPE_OUTPUT_FAILURE",
        display_name="Gamescope Output Failure",
        short_description="Gamescope failed to create its display output.",
        category="Gamescope",
        severity="high",
        patterns=[
            "failed to create gamescope output",
            "gamescope: failed to create output",
            "gamescope: output error",
            "gamescope: drm error",
            "gamescope: kms error",
        ],
        known_fix=[
            "Try launching the game without Gamescope.",
            "Update Gamescope, Mesa, and Vulkan packages.",
            "Switch between Wayland and X11 to compare behavior.",
        ],
        safe_commands=[
            "gamescope --version",
            "echo $XDG_SESSION_TYPE",
        ],
        icon="gamescope",
    ),

    FingerprintDefinition(
        id="GAMESCOPE_WAYLAND_RELATED",
        display_name="Gamescope Wayland Issue",
        short_description="Gamescope had a problem with the Wayland compositor.",
        category="Gamescope",
        severity="medium",
        patterns=[
            "gamescope: wayland",
            "gamescope: failed to connect to wayland",
            "gamescope: wl_display_connect failed",
            "wayland display not found",
        ],
        known_fix=[
            "Test without Gamescope.",
            "Try a simpler Gamescope launch option.",
            "Update Gamescope.",
            "Check whether the issue happens only on Wayland.",
        ],
        safe_commands=["echo $XDG_SESSION_TYPE", "echo $WAYLAND_DISPLAY"],
        icon="gamescope",
    ),

    FingerprintDefinition(
        id="GAMESCOPE_FAILURE",
        display_name="Gamescope Failure",
        short_description="Gamescope appeared in the log and may be involved in the launch failure.",
        category="Gamescope",
        severity="medium",
        patterns=[
            "gamescope: error",
            "gamescope: failed",
            "gamescope exited",
            "gamescope crashed",
        ],
        known_fix=[
            "Disable Gamescope temporarily.",
            "Remove Gamescope launch options and test.",
            "Update Gamescope.",
            "If the game launches without Gamescope, re-add options one at a time.",
        ],
        safe_commands=["gamescope --version"],
        icon="gamescope",
    ),

]
