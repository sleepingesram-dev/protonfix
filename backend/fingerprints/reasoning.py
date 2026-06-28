from fingerprints.models import FingerprintDefinition


def explain_reasoning(
    definitions: dict[str, FingerprintDefinition],
    chain: list[str],
) -> list[str]:
    """
    Convert a dependency chain into human-readable reasoning.
    """

    if not chain:
        return []

    reasoning: list[str] = []

    for i, fingerprint_id in enumerate(chain):
        definition = definitions.get(fingerprint_id)

        if not definition:
            reasoning.append(fingerprint_id)
            continue

        if i == 0:
            reasoning.append(
                f"Primary cause detected: {definition.display_name}."
            )
        else:
            reasoning.append(
                f"{definition.display_name} is likely a consequence of the previous failure."
            )

    return reasoning
