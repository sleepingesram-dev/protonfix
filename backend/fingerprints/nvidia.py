from fingerprints.models import FingerprintDefinition


NVIDIA_FINGERPRINTS = [

    FingerprintDefinition(
        id="NVIDIA_DRIVER_RELATED",
        display_name="NVIDIA Driver Issue",
        short_description="The NVIDIA driver encountered a problem.",
        category="NVIDIA Driver",
        severity="medium",
        patterns=[
            "nvidia driver",
            "nvidia: error",
            "nvidia: failed",
            "nvidia-modeset:",
            "nvidia: module",
            "failed to initialize nvml",
            "libnvidia",
        ],
        known_fix=[
            "Verify the NVIDIA driver is installed and loaded: run nvidia-smi.",
            "Install 32-bit NVIDIA libraries: lib32-nvidia-utils.",
            "Update the NVIDIA driver.",
            "Run vulkaninfo to confirm NVIDIA appears as a Vulkan device.",
            "Reboot after driver updates.",
        ],
        safe_commands=[
            "nvidia-smi",
            "vulkaninfo",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="NVIDIA_ICD_RELATED",
        display_name="NVIDIA Vulkan ICD Issue",
        short_description="The NVIDIA Vulkan ICD file is missing or not loaded.",
        category="NVIDIA Vulkan",
        severity="high",
        patterns=[
            "nvidia_icd",
            "nvidia_icd.json",
            "nvidia vulkan icd",
            "failed to load nvidia icd",
        ],
        caused_by=["VULKAN_DRIVER_MISSING"],
        known_fix=[
            "Install or reinstall nvidia-utils and lib32-nvidia-utils.",
            "Check that /usr/share/vulkan/icd.d/nvidia_icd.json exists.",
            "Reboot after reinstalling.",
            "Run vulkaninfo to confirm NVIDIA appears as a Vulkan device.",
        ],
        safe_commands=[
            "ls /usr/share/vulkan/icd.d/",
            "nvidia-smi",
            "vulkaninfo",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="NVIDIA_GPU_HANG",
        display_name="NVIDIA GPU Hang (XID Error)",
        short_description="The NVIDIA driver reported a GPU hang or XID error.",
        category="NVIDIA Driver",
        severity="high",
        patterns=[
            "nvrm: xid",
            "nvidia: gpu has fallen off",
            "gpu has fallen off the bus",
            "nvrm: rm_client_alloc_object",
            "nvidia: nvkm_pmu",
        ],
        known_fix=[
            "Update the NVIDIA driver to the latest available version.",
            "Remove GPU overclocks or undervolts.",
            "Check kernel logs for the full XID error context.",
            "If XID 79 appears, the GPU may be overheating — check cooling.",
            "If XID 13/31, try a clean driver reinstall.",
        ],
        safe_commands=[
            "nvidia-smi",
            "journalctl -k | grep -i nvidia",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="NVIDIA_GL_LIBRARY_RELATED",
        display_name="NVIDIA OpenGL/Vulkan Library Issue",
        short_description="An NVIDIA driver library could not be loaded.",
        category="NVIDIA Driver",
        severity="medium",
        patterns=[
            "libnvidia-gl",
            "libnvidia-glcore",
            "libnvidia-vulkan-producer",
            "libGL error: unable to load driver: nvidia",
            "failed to load nvidia libraries",
        ],
        known_fix=[
            "Update NVIDIA packages as a group to avoid version mismatches.",
            "Install lib32-nvidia-utils for 32-bit game and Steam support.",
            "Reboot after updating.",
        ],
        safe_commands=[
            "nvidia-smi",
        ],
        icon="gpu",
    ),

    FingerprintDefinition(
        id="NVIDIA_PRIME_RELATED",
        display_name="NVIDIA PRIME / Optimus Issue",
        short_description="NVIDIA PRIME or Optimus switching encountered a problem.",
        category="NVIDIA Driver",
        severity="medium",
        patterns=[
            "__nv_prime_render_offload",
            "prime-run",
            "optimus",
            "dri_prime",
            "failed to initialize prime",
        ],
        known_fix=[
            "Set DRI_PRIME=1 in launch options to force the discrete GPU.",
            "Use prime-run or the PRIME Render Offload method.",
            "Check that the NVIDIA driver and the Intel/AMD driver are both installed.",
            "Ensure the correct GPU is selected in the system settings.",
        ],
        safe_commands=[
            "nvidia-smi",
            "lspci | grep -E 'VGA|3D'",
        ],
        icon="gpu",
    ),

]
