from fingerprints.models import FingerprintDefinition


AMD_FINGERPRINTS = [

    FingerprintDefinition(
        id="AMDGPU_RESET",
        display_name="AMD GPU Reset",
        short_description="The AMD GPU driver triggered a GPU reset after a hang.",
        category="AMD Driver",
        severity="high",
        patterns=[
            "amdgpu: gpu reset",
            "amdgpu: gpu hang",
            "amdgpu: failed to reset gpu",
            "gpu reset begin",
            "gpu reset end",
            "amdgpu: gpu recovery succeeded",
            "amdgpu: gpu recovery failed",
        ],
        known_fix=[
            "Remove GPU overclocks or undervolts.",
            "Update Mesa and Vulkan packages.",
            "Reboot after updating.",
            "Check kernel logs for amdgpu errors.",
        ],
        safe_commands=[
            "sudo pacman -Syu mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon",
            "journalctl -k | grep -i amdgpu",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="AMDGPU_RING_TIMEOUT",
        display_name="AMD GPU Ring Timeout",
        short_description="The AMD GPU graphics command ring timed out.",
        category="AMD Driver",
        severity="high",
        patterns=[
            "ring gfx timeout",
            "ring sdma0 timeout",
            "ring sdma1 timeout",
            "ring vcn_dec timeout",
            "ring compute timeout",
            "amdgpu: gfx ring timeout",
            "amdgpu: ring timeout",
            "amdgpu job timeout",
        ],
        causes=["AMDGPU_RESET"],
        known_fix=[
            "Update Mesa and the Linux kernel together.",
            "Remove GPU overclocks or undervolts.",
            "Test without Gamescope or overlays.",
            "Check kernel logs for the full amdgpu error context.",
        ],
        safe_commands=[
            "journalctl -k | grep -i amdgpu",
            "uname -r",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="RADV_RELATED_FAILURE",
        display_name="RADV (AMD Mesa Vulkan) Issue",
        short_description="The RADV Mesa Vulkan driver for AMD GPUs reported a problem.",
        category="AMD Vulkan",
        severity="medium",
        patterns=[
            "radv",
            "radv: error",
            "radv: failed",
            "radv: gpu hang",
            "radv: pipeline",
            "radv: shader",
        ],
        known_fix=[
            "Update Mesa to the latest available version.",
            "Run vulkaninfo and check that RADV is the active Vulkan driver.",
            "Remove RADV_PERFTEST or RADV_DEBUG environment variables.",
        ],
        safe_commands=[
            "vulkaninfo | grep -i radv",
            "sudo pacman -Syu mesa vulkan-radeon",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="AMDGPU_FIRMWARE_MISSING",
        display_name="AMD GPU Firmware Missing",
        short_description="The AMD GPU could not load required firmware files.",
        category="AMD Driver",
        severity="high",
        patterns=[
            "amdgpu: failed to load firmware",
            "amdgpu: failed to create firmware",
            "direct firmware load for amdgpu",
            "amdgpu firmware",
            "failed to request firmware",
        ],
        known_fix=[
            "Install the linux-firmware package.",
            "Update the linux-firmware package to include firmware for your GPU.",
            "Reboot after installing firmware.",
        ],
        safe_commands=[
            "sudo pacman -Syu linux-firmware",
            "journalctl -k | grep -i firmware",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="AMDGPU_INIT_FAILURE",
        display_name="AMD GPU Initialization Failure",
        short_description="The AMD GPU driver failed during initialization.",
        category="AMD Driver",
        severity="high",
        patterns=[
            "amdgpu: failed to initialize",
            "amdgpu: probe failed",
            "amdgpu initialization failed",
            "amdgpu: failed to init",
        ],
        known_fix=[
            "Update the Linux kernel and Mesa.",
            "Install the linux-firmware package.",
            "Check kernel logs for the full amdgpu initialization error.",
            "Reboot after updating.",
        ],
        safe_commands=[
            "journalctl -k | grep -i amdgpu",
            "uname -r",
        ],
        icon="gpu",
    ),

]
