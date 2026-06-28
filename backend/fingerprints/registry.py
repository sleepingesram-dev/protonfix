from fingerprints.models import FingerprintDefinition
from fingerprints.vulkan import VULKAN_FINGERPRINTS
from fingerprints.proton import PROTON_FINGERPRINTS
from fingerprints.dxvk import DXVK_FINGERPRINTS
from fingerprints.nvidia import NVIDIA_FINGERPRINTS
from fingerprints.amd import AMD_FINGERPRINTS
from fingerprints.anticheat import ANTICHEAT_FINGERPRINTS
from fingerprints.audio import AUDIO_FINGERPRINTS
from fingerprints.memory import MEMORY_FINGERPRINTS
from fingerprints.gamescope import GAMESCOPE_FINGERPRINTS


ALL_FINGERPRINT_DEFINITIONS: list[FingerprintDefinition] = [
    *VULKAN_FINGERPRINTS,
    *PROTON_FINGERPRINTS,
    *DXVK_FINGERPRINTS,
    *NVIDIA_FINGERPRINTS,
    *AMD_FINGERPRINTS,
    *ANTICHEAT_FINGERPRINTS,
    *AUDIO_FINGERPRINTS,
    *MEMORY_FINGERPRINTS,
    *GAMESCOPE_FINGERPRINTS,
]


def build_error_patterns() -> dict[str, dict]:
    patterns: dict[str, dict] = {}

    for definition in ALL_FINGERPRINT_DEFINITIONS:
        for pattern in definition.patterns:
            patterns[pattern] = {
                "fingerprint": definition.id,
                "category": definition.category,
                "severity": definition.severity,
                "explanation": definition.short_description,
                "known_fix": definition.known_fix,
                "safe_commands": definition.safe_commands,
                "metadata": {
                    "display_name": definition.display_name,
                    "short_description": definition.short_description,
                    "icon": definition.icon,
                },
            }

    return patterns


ERROR_PATTERNS_V2 = build_error_patterns()

DEFINITION_MAP = {
    definition.id: definition
    for definition in ALL_FINGERPRINT_DEFINITIONS
}
