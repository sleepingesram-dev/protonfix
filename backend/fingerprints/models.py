from dataclasses import dataclass, field


@dataclass(frozen=True)
class FingerprintDefinition:
    id: str
    display_name: str
    short_description: str
    category: str
    severity: str
    patterns: list[str]

    causes: list[str] = field(default_factory=list)
    caused_by: list[str] = field(default_factory=list)
    commonly_seen_with: list[str] = field(default_factory=list)

    known_fix: list[str] = field(default_factory=list)
    safe_commands: list[str] = field(default_factory=list)
    icon: str = "unknown"
