from fingerprints.models import FingerprintDefinition
from fingerprints.vulkan import VULKAN_FINGERPRINTS


ALL_FINGERPRINT_DEFINITIONS: list[FingerprintDefinition] = [
    *VULKAN_FINGERPRINTS,
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
