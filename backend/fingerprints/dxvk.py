from fingerprints.models import FingerprintDefinition


DXVK_FINGERPRINTS = [

    FingerprintDefinition(
        id="DXVK_ADAPTER_FAILURE",
        display_name="DXVK Adapter Failure",
        short_description="DXVK could not initialize a usable Vulkan graphics adapter.",
        category="DXVK",
        severity="high",
        patterns=[
            "dxgi: failed to initialize adapter",
            "dxvkadapter: failed to initialize adapter",
            "dxgi_adapter: failed",
            "dxvk: no vulkan adapter found",
            "dxvk: failed to create device",
            "err:dxgi:dxgi_factory_create_swapchain",
        ],
        causes=["DXVK_RELATED_FAILURE", "DXVK_D3D11_FAILURE", "DIRECTX11_RELATED"],
        caused_by=["VULKAN_DRIVER_MISSING", "VULKAN_INIT_FAILURE"],
        known_fix=[
            "Fix Vulkan first — DXVK depends entirely on Vulkan.",
            "Run vulkaninfo and confirm Vulkan works.",
            "Update Mesa or NVIDIA Vulkan packages.",
            "Try a different Proton version.",
        ],
        safe_commands=[
            "vulkaninfo",
            "lspci | grep -E 'VGA|3D|Display'",
        ],
        icon="dxvk",
    ),

    FingerprintDefinition(
        id="DXVK_D3D11_FAILURE",
        display_name="DXVK D3D11 Failure",
        short_description="DXVK failed during Direct3D 11 initialization or operation.",
        category="DXVK",
        severity="medium",
        patterns=[
            "d3d11: failed",
            "dxvk: d3d11 error",
            "d3d11createdevice failed",
            "err:d3d11:",
            "d3d11 feature level",
            "dxvk err: d3d11",
        ],
        caused_by=["DXVK_ADAPTER_FAILURE"],
        known_fix=[
            "Update Proton — DXVK is bundled with it.",
            "Update Mesa or NVIDIA drivers.",
            "Try a different Proton version.",
            "Run vulkaninfo to confirm Vulkan works.",
        ],
        safe_commands=["vulkaninfo"],
        icon="dxvk",
    ),

    FingerprintDefinition(
        id="DXVK_GENERAL_FAILURE",
        display_name="DXVK Failure",
        short_description="DXVK reported a general DirectX-to-Vulkan translation failure.",
        category="DXVK",
        severity="medium",
        patterns=[
            "dxvk: failed",
            "dxvk err:",
            "dxvk: error:",
            "dxvk: critical error",
            "err:dxvk:",
        ],
        caused_by=["VULKAN_DRIVER_MISSING"],
        known_fix=[
            "Fix Vulkan first.",
            "Update GPU drivers.",
            "Try Proton Experimental or GE-Proton.",
            "Disable overlays while testing.",
        ],
        safe_commands=["vulkaninfo"],
        icon="dxvk",
    ),

    FingerprintDefinition(
        id="DXVK_SHADER_COMPILE_FAILURE",
        display_name="DXVK Shader Compilation Failure",
        short_description="DXVK failed to compile or cache a shader.",
        category="DXVK",
        severity="medium",
        patterns=[
            "dxvk: shader",
            "dxvk: failed to compile",
            "spirv: failed",
            "dxvk: pipeline compile error",
            "dxvk: failed to create pipeline",
        ],
        known_fix=[
            "Delete the DXVK shader cache and restart the game.",
            "Update Proton.",
            "Update Mesa or NVIDIA Vulkan drivers.",
            "Try disabling DXVK_ASYNC=1 if set.",
        ],
        safe_commands=[
            "find ~/.steam/steam/steamapps/shadercache/ -name '*.dxvk-cache' -delete",
        ],
        icon="dxvk",
    ),

    FingerprintDefinition(
        id="DIRECTX11_RELATED",
        display_name="DirectX 11 Issue",
        short_description="The log references DirectX 11, which Proton handles through DXVK.",
        category="DXVK",
        severity="low",
        patterns=[
            "direct3d 11",
            "d3d11 device",
            "directx 11",
            "dx11",
        ],
        caused_by=["DXVK_ADAPTER_FAILURE"],
        known_fix=[
            "If Vulkan errors also appear, fix Vulkan first.",
            "Update Proton and GPU drivers.",
            "Try a different Proton version.",
        ],
        safe_commands=["vulkaninfo"],
        icon="dxvk",
    ),

    FingerprintDefinition(
        id="DIRECTX12_RELATED",
        display_name="DirectX 12 Issue",
        short_description="The log references DirectX 12, which Proton handles through VKD3D-Proton.",
        category="VKD3D",
        severity="medium",
        patterns=[
            "direct3d 12",
            "d3d12 device",
            "directx 12",
            "dx12",
            "d3d12createdevice",
        ],
        caused_by=["VKD3D_RELATED_FAILURE"],
        known_fix=[
            "Update Proton and GPU drivers.",
            "Try Proton Experimental.",
            "Try DirectX 11 mode if the game supports it.",
        ],
        safe_commands=["vulkaninfo"],
        icon="vkd3d",
    ),

]
