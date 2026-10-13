"""Pure saved-ranking evidence for the approved T-028 codebook, sections 4-6.

No reader, method runner, label file or filesystem write is used here.  A record is
one method output and one seed.  Case/seed aggregation belongs to the caller.
``src.p3.danh_gia`` is used only for the two approved exact tie helpers.

All dictionaries are JSON-ready.  Top-k maps use decimal string keys (``"1"``,
``"5"``).  Missing measurements are null with availability ``"N/A"`` and a
reason; non-OK records never receive a zero ranking measurement.
"""

from fractions import Fraction
from math import comb

from src.p3.danh_gia import LoiBanGhi, khoi_tu_ban_ghi, phan_bo_hang


def _ks(ks):
    values = tuple(ks)
    if not values or any(type(k) is not int or k <= 0 for k in values):
        raise ValueError("ks must contain positive integers")
    if len(set(values)) != len(values):
        raise ValueError("ks must not contain duplicates")
    return values


def _ratio(value):
    """Preserve the exact arithmetic result alongside its display float."""
    return {"numerator": value.numerator, "denominator": value.denominator}


def _unavailable_pair(k, reason):
    return {
        "k": k, "D": None, "D0": None, "delta": None, "V": None,
        "availability": "N/A", "reason": reason,
    }


def ranking_summary(rec, ks=(1, 5)):
    """Summarize O/R and exact top-k probabilities without knowing any root.

    ``entity_keys`` keeps every component of the saved entity key.  ``blocks``
    and ``entity_locations`` retain block/group membership, which cannot be
    replaced by rank intervals for TORAI.  Eligibility follows codebook §6:
    OK, unique returned entities, 0<L<=|O|, and R subset O, plus validity of the
    saved native tie/key representation checked by the P3 helper.
    """
    ks = _ks(ks)
    status = rec.get("status")
    observed = rec.get("sets", {}).get("observed_entities")
    violations = []
    if observed is None:
        observed = []
        violations.append("observed_entities_missing")
    O = sorted(set(observed))
    summary = {
        "status": status, "O": O, "R": [], "n": len(O), "L": 0,
        "availability": "N/A", "reason": None,
        "invariant": {"value": None, "availability": "N/A", "reason": None,
                      "violations": violations},
        "entity_keys": {}, "entity_locations": {}, "blocks": [],
        "p_by_k": {str(k): None for k in ks},
        "p_by_k_exact": {str(k): None for k in ks},
        "m_by_k": {str(k): None for k in ks},
        "mass_by_k_exact": {str(k): None for k in ks},
    }
    if status != "OK":
        reason = "unsupported" if status == "UNSUPPORTED" else "non_OK"
        summary["reason"] = reason
        summary["invariant"]["reason"] = reason
        return summary

    try:
        blocks = khoi_tu_ban_ghi(rec)
    except (LoiBanGhi, KeyError, TypeError, ValueError, ArithmeticError) as exc:
        # The approved helper raises its own LoiBanGhi.  Preserve the message as
        # evidence and return N/A instead of correcting the stored ranking.
        violations.append("saved_key_or_tie_invalid: " + str(exc))
        summary["reason"] = "invalid_ranking_invariant"
        summary["invariant"].update(value=False, availability="available",
                                    reason=summary["reason"])
        return summary

    branches = rec.get("extra", {}).get("nhanh_khoi") or []
    for block_index, block in enumerate(blocks):
        groups = [list(group) for group in block["groups"]]
        metadata = {
            "block_index": block_index, "key": list(block["key"]),
            "groups": groups, "size": sum(map(len, groups)),
            "branch": branches[block_index] if block_index < len(branches) else None,
        }
        summary["blocks"].append(metadata)
        for group_index, group in enumerate(groups):
            for entity in group:
                summary["R"].append(entity)
                summary["entity_keys"][entity] = list(block["key"])
                summary["entity_locations"][entity] = {
                    "block_index": block_index, "group_index": group_index,
                    "group_size": len(group), "block_size": metadata["size"],
                }

    R = summary["R"]
    summary["L"] = len(R)
    if not R:
        violations.append("empty_returned_set")
    if len(R) != len(set(R)):
        violations.append("duplicate_returned_entity")
    if len(R) > len(O):
        violations.append("returned_count_exceeds_observed")
    if not set(R).issubset(O):
        violations.append("returned_entity_outside_observed")
    if any(not group for block in blocks for group in block["groups"]):
        violations.append("empty_saved_tie_group")
    if any(not block["groups"] for block in blocks):
        violations.append("empty_saved_block")

    if violations:
        summary["reason"] = "invalid_ranking_invariant"
        summary["invariant"].update(value=False, availability="available",
                                    reason=summary["reason"])
        return summary

    probabilities = {str(k): {} for k in ks}
    exact = {str(k): {} for k in ks}
    totals = {str(k): Fraction(0) for k in ks}
    for entity in O:
        dist = phan_bo_hang(blocks, entity)
        if entity in R and (not dist or sum(dist.values()) != 1):
            violations.append("rank_distribution_not_normalized: " + entity)
        for k in ks:
            p = sum((probability for rank, probability in dist.items() if rank <= k),
                    Fraction(0))
            probabilities[str(k)][entity] = float(p)
            exact[str(k)][entity] = _ratio(p)
            totals[str(k)] += p
    for k in ks:
        if totals[str(k)] != min(k, len(R)):
            violations.append("top_k_probability_mass_invalid: " + str(k))
    if violations:
        summary["reason"] = "invalid_ranking_invariant"
        summary["invariant"].update(value=False, availability="available",
                                    reason=summary["reason"])
        return summary

    summary.update(
        availability="available", reason=None, p_by_k=probabilities,
        p_by_k_exact=exact, m_by_k={str(k): min(k, len(R)) for k in ks},
        mass_by_k_exact={str(k): _ratio(totals[str(k)]) for k in ks},
    )
    summary["invariant"].update(value=True, availability="available", reason=None)
    return summary


def certain_before(rec, root):
    """Return entities definitely before root, or None when this is N/A.

    Full keys compare lexicographically and exactly.  Inside a single block,
    only a strictly earlier group is certain; distinct blocks with equal keys
    can permute and therefore are never certain before each other.  A valid
    record with root first (or entirely tied) returns the measured empty list.
    """
    summary = ranking_summary(rec)
    if summary["availability"] != "available" or root not in summary["R"]:
        return None
    root_location = summary["entity_locations"][root]
    root_key = tuple(summary["entity_keys"][root])
    result = []
    for entity in summary["R"]:
        if entity == root:
            continue
        location = summary["entity_locations"][entity]
        if (tuple(summary["entity_keys"][entity]) > root_key or
                (location["block_index"] == root_location["block_index"] and
                 location["group_index"] < root_location["group_index"])):
            result.append(entity)
    return result


def p0_value(n, a, b):
    """Exact-combination descriptive P0 (§5.1), returned as a display float.

    n counts O, a counts ancestors in O excluding root, and b counts entities
    certainly before root.  Validate eligibility outside this scalar helper.
    No significance threshold, p-value or seed aggregation is applied.
    """
    if (any(type(value) is not int for value in (n, a, b)) or n < 1 or
            not 0 <= a <= n - 1 or not 0 <= b <= n - 1):
        raise ValueError("P0 requires integer n>=1 and 0<=a,b<=n-1")
    denominator = comb(n - 1, b)
    numerator = comb(n - 1 - a, b) if b <= n - 1 - a else 0
    return float(Fraction(denominator - numerator, denominator))


def _exact_probability(summary, k, entity):
    ratio = summary["p_by_k_exact"][str(k)].get(entity)
    if ratio is None:
        return Fraction(0)
    return Fraction(ratio["numerator"], ratio["denominator"])


def dice_pair(summary_i, summary_j, k):
    """One eligible saved-record pair's D, D0, delta and V (§6).

    This does not average seeds, cases or cells.  The caller must keep each case
    pair as one unit and average only eligible seed combinations.  Two draws
    from identical ties can have D<1 because tie breaking is independent.
    """
    _ks((k,))
    for side, summary in (("i", summary_i), ("j", summary_j)):
        if summary.get("availability") != "available":
            return _unavailable_pair(k, side + ":" + (summary.get("reason") or
                                                     "invalid_ranking_invariant"))
        if str(k) not in summary["p_by_k"] or summary["p_by_k"][str(k)] is None:
            return _unavailable_pair(k, side + ":top_k_probability_not_computed")
    O_i, O_j = set(summary_i["O"]), set(summary_j["O"])
    m_i, m_j = min(k, summary_i["L"]), min(k, summary_j["L"])
    if not O_i or not O_j or m_i + m_j == 0:
        return _unavailable_pair(k, "invalid_ranking_invariant")
    overlap = len(O_i & O_j)
    product = sum((_exact_probability(summary_i, k, entity) *
                   _exact_probability(summary_j, k, entity)
                   for entity in O_i & O_j), Fraction(0))
    D = 2 * product / (m_i + m_j)
    D0 = Fraction(2 * m_i * m_j * overlap,
                  len(O_i) * len(O_j) * (m_i + m_j))
    delta, V = D - D0, 1 - D
    return {
        "k": k, "D": float(D), "D0": float(D0), "delta": float(delta),
        "V": float(V), "availability": "available", "reason": None,
        "n_i": len(O_i), "n_j": len(O_j), "L_i": summary_i["L"],
        "L_j": summary_j["L"], "m_i": m_i, "m_j": m_j,
        "observed_intersection_n": overlap,
        "exact": {"D": _ratio(D), "D0": _ratio(D0), "delta": _ratio(delta),
                  "V": _ratio(V)},
    }
