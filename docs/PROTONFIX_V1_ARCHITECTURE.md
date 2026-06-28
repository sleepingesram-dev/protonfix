# ProtonFix v1.0 Architecture

## Purpose

ProtonFix is a deterministic Linux gaming diagnosis engine with AI fallback.

The goal is not just to detect errors, but to explain failures through a structured knowledge graph built from Proton, Steam, Wine, DXVK, VKD3D, Gamescope, GameMode, MangoHud, Vulkan, GPU driver, filesystem, and system logs.

## Core Philosophy

AI is not the brain.

The knowledge graph is the brain.

AI is used only when deterministic diagnosis confidence is low, when unknown patterns are detected, or when summarizing complex evidence for humans.

## High-Level Flow

```txt
User Upload
    ↓
Raw Log Storage
    ↓
Evidence Extraction
    ↓
Pattern Matching
    ↓
Knowledge Node Resolution
    ↓
Root Cause Ranking
    ↓
Dependency / Causal Graph
    ↓
Reasoning Engine
    ↓
Known Fix Resolver
    ↓
AI Fallback if Needed
    ↓
Diagnosis Report
    ↓
Telemetry / Learning Pipeline
```
___

## Knowledge Node Schema

A Knowledge Node represents one diagnosable issue in ProtonFix.

A node is not just a fingerprint. It contains everything ProtonFix knows about a failure: how to detect it, how to explain it, what it causes, what causes it, how to fix it, and how confidence should be calculated.

### Required Fields

```python
@dataclass(frozen=True)
class KnowledgeNode:
    id: str
    display_name: str
    short_description: str
    category: str
    severity: str
    patterns: list[str]
```

### Relationship Fields

```python
    causes: list[str]
    caused_by: list[str]
    commonly_seen_with: list[str]
```

### Fix Fields

```python
    known_fix: list[str]
    safe_commands: list[str]
    unsafe_commands: list[str]
```

### Reasoning Fields

```python
    reasoning: dict[str, str]
    confidence_modifiers: dict[str, int]
```

### Metadata Fields

```python
    icon: str
    documentation_url: str | None
    tags: list[str]
```

### Telemetry Fields

```python
    seen_count: int
    confirmed_fix_count: int
    failed_fix_count: int
```
### Example Node

```python
KnowledgeNode(
    id="VK_ERROR_EXTENSION_NOT_PRESENT",
    display_name="Missing Vulkan Extension",
    short_description="A required Vulkan extension is missing or unavailable.",
    category="Graphics Driver",
    severity="high",
    patterns=[
        "VK_ERROR_EXTENSION_NOT_PRESENT",
    ],
    causes=[
        "VULKAN_INIT_FAILURE",
        "DXVK_ADAPTER_FAILURE",
        "GAMESCOPE_VULKAN_INIT_FAILURE",
    ],
    caused_by=[
        "OUTDATED_MESA_DRIVER",
        "UNSUPPORTED_GPU",
        "BROKEN_VULKAN_ICD",
    ],
    commonly_seen_with=[
        "GAMESCOPE_FAILURE",
        "DXVK_RELATED_FAILURE",
    ],
    known_fix=[
        "Update Mesa or your GPU driver.",
        "Disable Gamescope and test the game directly.",
        "Check whether your GPU supports the required Vulkan extension.",
    ],
    safe_commands=[
        "vulkaninfo",
        "vulkaninfo | grep extension",
    ],
    unsafe_commands=[],
    reasoning={
        "VULKAN_INIT_FAILURE": "Without the required Vulkan extension, Vulkan cannot initialize.",
        "DXVK_ADAPTER_FAILURE": "DXVK depends on a working Vulkan device.",
        "GAMESCOPE_VULKAN_INIT_FAILURE": "Gamescope cannot initialize Vulkan without the required extension.",
    },
    confidence_modifiers={
        "GAMESCOPE_FAILURE": 10,
        "DXVK_RELATED_FAILURE": 5,
    },
    icon="gpu",
    documentation_url=None,
    tags=["vulkan", "gpu", "mesa", "driver"],
    seen_count=0,
    confirmed_fix_count=0,
    failed_fix_count=0,
)
```
---

# Reasoning Engine

## Purpose

The Reasoning Engine converts raw evidence into an explainable diagnosis.

It never invents information.

Every statement must be backed by one or more Knowledge Nodes and their relationships.

The output should allow a user to understand:

- what failed first,
- what failures were downstream consequences,
- why ProtonFix believes this,
- what should be fixed first.

---

## Input

```python
{
    "primary_node": KnowledgeNode,
    "detected_nodes": list[KnowledgeNode],
    "dependency_chain": list[str],
}
```

---

## Output

```python
{
    "summary": str,
    "reasoning_steps": list[str],
    "recommended_fix_order": list[str],
    "confidence": int,
}
```

---

## Reasoning Rules

1. Begin with the highest-ranked primary node.

2. Walk the dependency graph.

3. Explain every edge using the source node's reasoning data.

4. Never invent missing relationships.

5. If no relationship exists, stop the chain.

6. AI may summarize the reasoning but must never replace it.

---

## Example

```text
Primary Cause

Missing Vulkan Extension

↓

Reasoning

A required Vulkan extension was unavailable.

↓

Because Vulkan could not initialize,
DXVK could not create a rendering device.

↓

Since DXVK failed,
VKD3D could not initialize DirectX 12.

↓

Recommendation

Resolve the Vulkan issue first.
The remaining failures are expected to disappear.
```
---

# Inference Engine

## Purpose

The Inference Engine converts Evidence into ranked Hypotheses.

It is responsible for determining which Knowledge Nodes best explain the observed evidence.

The Inference Engine does not extract evidence, store telemetry, or generate user-facing text. Its job is to evaluate possible explanations.

---

## Core Flow

```txt
Evidence Objects
    ↓
Candidate Hypothesis Generation
    ↓
Evidence Scoring
    ↓
Contradiction Handling
    ↓
Relationship Expansion
    ↓
Hypothesis Ranking
    ↓
Primary Hypothesis Selection

---

# Relationship Propagation

## Purpose

Relationship Propagation allows ProtonFix to reason from direct observations to higher-level explanations.

Evidence often supports a symptom node first.

The actual root cause may be a parent Knowledge Node connected through causal relationships.

Example:

```txt
DXVK adapter failure
    ↓
caused by
    ↓
Vulkan initialization failure
    ↓
caused by
    ↓
Missing Vulkan driver
