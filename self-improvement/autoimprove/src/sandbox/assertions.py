"""
Reusable deterministic assertions for v2 behavioral checks.

Each assertion returns (bool, str) where the string explains pass/fail.
Assertions NEVER call an LLM. They only inspect strings, files, and JSON.
"""

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# String assertions
# ---------------------------------------------------------------------------

def must_contain(output: str, needles: list[str]) -> tuple[bool, str]:
    """All strings in `needles` must appear (case-insensitive) in output."""
    missing = [n for n in needles if n.lower() not in output.lower()]
    if missing:
        return False, f"missing: {missing}"
    return True, f"found all {len(needles)}"


def must_contain_any(output: str, candidates: list[str]) -> tuple[bool, str]:
    """At least one string in `candidates` must appear in output."""
    found = [c for c in candidates if c.lower() in output.lower()]
    if not found:
        return False, f"none of {candidates} found"
    return True, f"found: {found[0]}"


def must_not_contain(output: str, forbidden: list[str]) -> tuple[bool, str]:
    """None of the forbidden strings may appear."""
    hits = [f for f in forbidden if f.lower() in output.lower()]
    if hits:
        return False, f"forbidden present: {hits}"
    return True, f"clean against {len(forbidden)} forbidden"


def forbidden_patterns_absent(output: str, patterns: list[str]) -> tuple[bool, str]:
    """No regex pattern in `patterns` matches."""
    hits = [p for p in patterns if re.search(p, output)]
    if hits:
        return False, f"pattern matches: {hits}"
    return True, f"no forbidden patterns"


def must_match_any_pattern(output: str, patterns: list[str]) -> tuple[bool, str]:
    """At least one regex pattern must match (case-insensitive by default)."""
    matched = [p for p in patterns if re.search(p, output, re.IGNORECASE)]
    if not matched:
        return False, f"none of {len(patterns)} patterns matched"
    return True, f"matched: {matched[0]!r}"


def must_contain_all_numbers(output: str, numbers: list[str]) -> tuple[bool, str]:
    """Every number string must appear verbatim."""
    missing = [n for n in numbers if n not in output]
    if missing:
        return False, f"missing numbers: {missing}"
    return True, f"all numbers present"


# ---------------------------------------------------------------------------
# Count-based assertions
# ---------------------------------------------------------------------------

def word_count_in_range(output: str, low: int, high: int) -> tuple[bool, str]:
    count = len(output.split())
    if low <= count <= high:
        return True, f"word count {count} in [{low}, {high}]"
    return False, f"word count {count} outside [{low}, {high}]"


def hashtag_count_max(output: str, maximum: int) -> tuple[bool, str]:
    count = len(re.findall(r'(?<!\w)#\w+', output))
    if count <= maximum:
        return True, f"hashtags {count} <= {maximum}"
    return False, f"hashtags {count} > {maximum}"


# ---------------------------------------------------------------------------
# File-system assertions (sandbox)
# ---------------------------------------------------------------------------

def files_exist(sandbox_root: Path, paths: list[str]) -> tuple[bool, str]:
    """Every relative path must exist under sandbox_root."""
    missing = [p for p in paths if not (sandbox_root / p).exists()]
    if missing:
        return False, f"missing files: {missing}"
    return True, f"all {len(paths)} files exist"


def files_preserved(sandbox_root: Path, paths: list[str]) -> tuple[bool, str]:
    """Files that should have been preserved (not overwritten)."""
    missing = [p for p in paths if not (sandbox_root / p).exists()]
    if missing:
        return False, f"preserved-files missing: {missing}"
    return True, f"all {len(paths)} preserved"


def files_not_created(sandbox_root: Path, paths: list[str]) -> tuple[bool, str]:
    """None of these paths should exist."""
    hits = [p for p in paths if (sandbox_root / p).exists()]
    if hits:
        return False, f"unexpected files created: {hits}"
    return True, f"no forbidden files created"


def no_placeholders_in_file(sandbox_root: Path, relpath: str,
                             forbidden: list[str]) -> tuple[bool, str]:
    """File must not contain placeholder/template strings."""
    path = sandbox_root / relpath
    if not path.exists():
        return False, f"file missing: {relpath}"
    text = path.read_text()
    hits = [f for f in forbidden if f in text]
    if hits:
        return False, f"{relpath} contains: {hits}"
    return True, f"{relpath} clean"


# ---------------------------------------------------------------------------
# Registry assertions (JSON state)
# ---------------------------------------------------------------------------

def entity_registry_has_entry(registry_path: Path, entry_match: dict
                               ) -> tuple[bool, str]:
    """
    Registry must contain an entity matching all keys in `entry_match`.
    `entry_match["required_fields"]` (if present) lists fields that must exist
    on the matched entity (non-empty).
    """
    if not registry_path.exists():
        return False, "entity-registry.json missing"
    data = json.loads(registry_path.read_text())
    projects = data.get("entities", {}).get("projects", [])
    required_fields = entry_match.pop("required_fields", [])
    for p in projects:
        if all(p.get(k) == v for k, v in entry_match.items()):
            missing_fields = [f for f in required_fields if not p.get(f)]
            if missing_fields:
                return False, f"entry found but missing fields: {missing_fields}"
            return True, f"entry for {entry_match.get('id')} complete"
    return False, f"no entry matching {entry_match}"


def relationship_map_has_entry(map_path: Path, rel_match: dict
                                ) -> tuple[bool, str]:
    if not map_path.exists():
        return False, "relationship-map.json missing"
    data = json.loads(map_path.read_text())
    rels = data.get("relationships", {}).get("project_to_project", [])
    for r in rels:
        if all(r.get(k) == v for k, v in rel_match.items()):
            return True, f"relationship {rel_match.get('source')}→{rel_match.get('target')} present"
    return False, f"no relationship matching {rel_match}"


def hierarchy_path_contains(map_path: Path, dotted_path: str,
                             needle: str) -> tuple[bool, str]:
    """Traverse relationships.hierarchy.<dotted_path> and verify `needle` is in it."""
    if not map_path.exists():
        return False, "relationship-map.json missing"
    data = json.loads(map_path.read_text())
    node = data.get("relationships", {}).get("hierarchy", {})
    for key in dotted_path.split("."):
        if not isinstance(node, dict) or key not in node:
            return False, f"hierarchy path {dotted_path} does not exist"
        node = node[key]
    if isinstance(node, list) and needle in node:
        return True, f"{needle} present at hierarchy.{dotted_path}"
    if isinstance(node, dict) and needle in node:
        return True, f"{needle} key present at hierarchy.{dotted_path}"
    return False, f"{needle} not found at hierarchy.{dotted_path}"


# ---------------------------------------------------------------------------
# Top-level runner
# ---------------------------------------------------------------------------

def run_behavioral_checks(output: str, checks: dict,
                           sandbox_root: Path | None = None) -> dict:
    """
    Execute the `behavioral_checks` block from a v2 test case.

    Returns:
      {
        "pass_rate": float,          # fraction of checks that passed
        "passed": int,
        "total": int,
        "results": [{"name": ..., "passed": bool, "detail": str}, ...]
      }
    """
    results: list[dict] = []

    text = checks.get("text_assertions", {})
    if (v := text.get("must_contain")):
        results.append(_wrap("must_contain", must_contain(output, v)))
    if (v := text.get("must_contain_any")):
        results.append(_wrap("must_contain_any", must_contain_any(output, v)))
    if (v := text.get("must_contain_any_process_evidence")):
        results.append(_wrap("process_evidence", must_contain_any(output, v)))
    if (v := text.get("forbidden_strings")):
        results.append(_wrap("forbidden_strings", must_not_contain(output, v)))
    if (v := text.get("forbidden_patterns")):
        results.append(_wrap("forbidden_patterns", forbidden_patterns_absent(output, v)))
    if (v := text.get("must_match_any_pattern")):
        results.append(_wrap("match_any_pattern", must_match_any_pattern(output, v)))
    if (v := text.get("must_contain_all_numbers")):
        results.append(_wrap("all_numbers", must_contain_all_numbers(output, v)))
    if (v := text.get("word_count_range")):
        results.append(_wrap("word_count", word_count_in_range(output, v[0], v[1])))
    if (v := text.get("hashtag_max")) is not None:
        results.append(_wrap("hashtag_max", hashtag_count_max(output, v)))

    files = checks.get("file_effects")
    if files and sandbox_root:
        if (v := files.get("expected_files_created")):
            results.append(_wrap("files_created", files_exist(sandbox_root, v)))
        if (v := files.get("expected_files_preserved")):
            results.append(_wrap("files_preserved", files_preserved(sandbox_root, v)))
        if (v := files.get("forbidden_files_created")):
            results.append(_wrap("forbidden_files", files_not_created(sandbox_root, v)))
        if (v := files.get("forbidden_placeholders_in")):
            forbidden = files.get("forbidden_strings",
                                   ["TODO", "TBD", "[placeholder]", "Lorem ipsum"])
            for f in v:
                results.append(_wrap(f"no_placeholders_{f}",
                                      no_placeholders_in_file(sandbox_root, f, forbidden)))

    registry = checks.get("registry_effects")
    if registry and sandbox_root:
        if (v := registry.get("entity_registry_added")):
            reg_path = sandbox_root / "knowledge" / "entity-registry.json"
            results.append(_wrap("entity_added", entity_registry_has_entry(reg_path, dict(v))))
        if (v := registry.get("relationship_map_added")):
            map_path = sandbox_root / "knowledge" / "relationship-map.json"
            results.append(_wrap("relationship_added", relationship_map_has_entry(map_path, dict(v))))
        if (v := registry.get("relationship_map_hierarchy_updated")):
            map_path = sandbox_root / "knowledge" / "relationship-map.json"
            needle = registry.get("entity_registry_added", {}).get("id", "")
            results.append(_wrap("hierarchy_updated",
                                  hierarchy_path_contains(map_path, v["path"], needle)))

    passed = sum(1 for r in results if r["passed"])
    total = len(results) or 1
    return {
        "pass_rate": passed / total,
        "passed": passed,
        "total": len(results),
        "results": results,
    }


def _wrap(name: str, result: tuple[bool, str]) -> dict:
    ok, detail = result
    return {"name": name, "passed": ok, "detail": detail}
