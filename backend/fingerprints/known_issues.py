KNOWN_ISSUES = {
    "VULKAN_DRIVER_MISSING": {
        "title": "Missing or Broken Vulkan Driver",
        "summary": "The log shows Vulkan cannot find a compatible driver or GPU device.",
        "probable_cause": "The Vulkan driver is missing, broken, or incompatible with the installed GPU driver.",
        "confidence": "high",
        "severity": "high",
        "fix_steps": [
            "Install or reinstall the Vulkan driver for your GPU.",
            "For AMD GPUs on Arch/CachyOS, install mesa, vulkan-radeon, and vulkan-tools.",
            "Reboot after installing or updating graphics packages.",
            "Run vulkaninfo to confirm Vulkan is working.",
            "Try launching the game again after Vulkan works."
        ],
        "recommended_commands": [
            "sudo pacman -Syu mesa vulkan-radeon vulkan-tools",
            "vulkaninfo"
        ],
        "warnings": [
            "Do not troubleshoot Proton first if Vulkan itself is broken.",
            "DXVK depends on Vulkan, so DXVK errors may be symptoms of the same root problem."
        ]
    }
}
