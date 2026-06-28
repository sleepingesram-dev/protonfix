from dataclasses import dataclass, field

from confidence import evidence_weight
from evidence import Evidence, EvidenceKind
from fingerprints.dependencies import ROOT_CAUSE_GRAPH


@dataclass
class Hypothesis:
    node_id: str

    supporting_evidence: list[Evidence] = field(default_factory=list)
    contradictory_evidence: list[Evidence] = field(default_factory=list)

    direct_support_count: int = 0
    propagated_support_count: int = 0

    score: int = 0


def build_reverse_graph() -> dict[str, list[str]]:
    """
    Convert parent -> children relationships into child -> parents.

    Example:
    VULKAN_DRIVER_MISSING -> DXVK_ADAPTER_FAILURE

    becomes:

    DXVK_ADAPTER_FAILURE -> VULKAN_DRIVER_MISSING
    """

    reverse_graph: dict[str, list[str]] = {}

    for parent, children in ROOT_CAUSE_GRAPH.items():
        for child in children:
            if child not in reverse_graph:
                reverse_graph[child] = []

            reverse_graph[child].append(parent)

    return reverse_graph


def ensure_hypothesis(
    hypotheses: dict[str, Hypothesis],
    node_id: str,
) -> Hypothesis:
    if node_id not in hypotheses:
        hypotheses[node_id] = Hypothesis(node_id=node_id)

    return hypotheses[node_id]


def create_direct_hypotheses(
    evidence_items: list[Evidence],
) -> dict[str, Hypothesis]:
    """
    Stage 1:
    Create hypotheses directly supported by evidence.
    """

    hypotheses: dict[str, Hypothesis] = {}

    for evidence in evidence_items:
        for node_id in evidence.supports:
            hypothesis = ensure_hypothesis(hypotheses, node_id)

            if evidence not in hypothesis.supporting_evidence:
                hypothesis.supporting_evidence.append(evidence)
                hypothesis.direct_support_count += 1

    return hypotheses


def propagate_evidence(
    hypotheses: dict[str, Hypothesis],
    max_depth: int = 3,
) -> dict[str, Hypothesis]:
    """
    Stage 2:
    Propagate evidence upward through the causal graph.

    Important:
    This propagates evidence, not score.

    Scores are calculated later in one final scoring pass.
    That prevents runaway propagation loops.
    """

    reverse_graph = build_reverse_graph()

    queue: list[tuple[str, Evidence, int]] = []

    for hypothesis in hypotheses.values():
        for evidence in hypothesis.supporting_evidence:
            if evidence.kind == EvidenceKind.CONTEXT:
                continue

            queue.append((hypothesis.node_id, evidence, 0))

    visited: set[tuple[str, str, int]] = set()

    while queue:
        current_node_id, evidence, depth = queue.pop(0)

        if depth >= max_depth:
            continue

        parents = reverse_graph.get(current_node_id, [])

        for parent_id in parents:
            visit_key = (parent_id, evidence.id, depth + 1)

            if visit_key in visited:
                continue

            visited.add(visit_key)

            parent_hypothesis = ensure_hypothesis(hypotheses, parent_id)

            if evidence not in parent_hypothesis.supporting_evidence:
                parent_hypothesis.supporting_evidence.append(evidence)
                parent_hypothesis.propagated_support_count += 1

            queue.append((parent_id, evidence, depth + 1))

    return hypotheses


def calculate_hypothesis_scores(
    hypotheses: dict[str, Hypothesis],
) -> dict[str, Hypothesis]:
    """
    Stage 3:
    Calculate scores once after evidence aggregation is complete.
    """

    for hypothesis in hypotheses.values():
        score = 0

        for evidence in hypothesis.supporting_evidence:
            score += evidence_weight(evidence)

        for evidence in hypothesis.contradictory_evidence:
            score -= evidence_weight(evidence)

        hypothesis.score = max(score, 0)

    return hypotheses


def rank_hypotheses(
    hypotheses: dict[str, Hypothesis],
) -> list[Hypothesis]:
    """
    Stage 4:
    Rank hypotheses by final score.
    """

    ranked = list(hypotheses.values())

    ranked.sort(
        key=lambda hypothesis: (
            hypothesis.score,
            hypothesis.direct_support_count,
            hypothesis.propagated_support_count,
        ),
        reverse=True,
    )

    return ranked


def get_primary_hypothesis(
    hypotheses: dict[str, Hypothesis],
) -> Hypothesis | None:
    ranked = rank_hypotheses(hypotheses)

    if not ranked:
        return None

    return ranked[0]


def generate_hypotheses(
    evidence_items: list[Evidence],
) -> dict[str, Hypothesis]:
    """
    Full v0.8 inference pipeline.

    Stage 1: create direct hypotheses
    Stage 2: propagate evidence through causal relationships
    Stage 3: calculate scores once
    Stage 4: return hypotheses for ranking/selection
    """

    hypotheses = create_direct_hypotheses(evidence_items)
    hypotheses = propagate_evidence(hypotheses)
    hypotheses = calculate_hypothesis_scores(hypotheses)

    return hypotheses
