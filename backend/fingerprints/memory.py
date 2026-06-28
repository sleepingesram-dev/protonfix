from fingerprints.models import FingerprintDefinition


MEMORY_FINGERPRINTS = [

    FingerprintDefinition(
        id="OUT_OF_MEMORY",
        display_name="Out of System Memory",
        short_description="The system or game ran out of available RAM or swap.",
        category="Memory",
        severity="high",
        patterns=[
            "out of memory",
            "cannot allocate memory",
            "failed to allocate memory",
            "memory allocation failed",
            "enomem",
        ],
        causes=["MEMORY_ALLOCATION_FAILURE", "VK_ERROR_OUT_OF_DEVICE_MEMORY", "WINE_CRASH", "CORE_DUMPED"],
        known_fix=[
            "Close background applications before launching the game.",
            "Lower game settings that use a lot of memory.",
            "Check RAM and swap usage.",
            "Consider adding or increasing swap space.",
        ],
        safe_commands=[
            "free -h",
            "swapon --show",
        ],
        icon="memory",
    ),

    FingerprintDefinition(
        id="OOM_KILLER_TRIGGERED",
        display_name="OOM Killer Triggered",
        short_description="The Linux kernel OOM killer terminated a process due to memory exhaustion.",
        category="Memory",
        severity="high",
        patterns=[
            "oom-killer",
            "out of memory: kill process",
            "oom_kill_process",
            "killed process",
            "memory cgroup out of memory",
        ],
        causes=["MEMORY_ALLOCATION_FAILURE"],
        known_fix=[
            "Close background applications before launching.",
            "Lower memory-intensive game settings.",
            "Add or increase swap space if the system has none.",
            "Check kernel logs to see which process was killed.",
        ],
        safe_commands=[
            "free -h",
            "journalctl -k | grep -i oom",
        ],
        icon="memory",
    ),

    FingerprintDefinition(
        id="VK_ERROR_OUT_OF_DEVICE_MEMORY",
        display_name="GPU Out of Memory (VRAM)",
        short_description="Vulkan ran out of GPU-accessible VRAM.",
        category="Vulkan",
        severity="high",
        patterns=[
            "vk_error_out_of_device_memory",
            "out of device memory",
            "vkdevicememory: out of memory",
            "failed to allocate device memory",
        ],
        known_fix=[
            "Lower texture quality and resolution.",
            "Disable high-resolution texture packs or mods.",
            "Close other GPU-heavy applications.",
            "Lower anti-aliasing and shadow settings.",
        ],
        safe_commands=[
            "radeontop",
            "nvidia-smi",
        ],
        icon="memory",
    ),

    FingerprintDefinition(
        id="VK_ERROR_OUT_OF_HOST_MEMORY",
        display_name="Vulkan Out of Host Memory",
        short_description="Vulkan ran out of system (CPU-side) memory.",
        category="Vulkan",
        severity="high",
        patterns=[
            "vk_error_out_of_host_memory",
            "out of host memory",
        ],
        caused_by=["OUT_OF_MEMORY"],
        known_fix=[
            "Close background applications.",
            "Check RAM and swap usage.",
            "Reboot and try again.",
        ],
        safe_commands=["free -h"],
        icon="memory",
    ),

]
