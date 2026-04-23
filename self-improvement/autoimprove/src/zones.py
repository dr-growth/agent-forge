"""
Path zone classifier for autoimprove.

Every filesystem path the loop touches is classified GREEN / YELLOW / RED.
The loop can write autonomously to GREEN, must escalate to David for YELLOW,
and must refuse RED even if a proposal asks for it.

Design principles:
  - Fail closed. Unknown paths return UNKNOWN and are treated as RED by callers.
  - Red-zone checks take precedence. A path under a red prefix is never green.
  - Path comparison uses resolved filesystem paths to defeat symlink tricks.

See: projects/autoimprove/GOVERNANCE.md for the full spec.
"""

from pathlib import Path


HOME = Path.home()
AUTOIMPROVE = HOME / "os" / "projects" / "autoimprove"


# Paths the loop can write autonomously.
# Git-tracked, reversible, scoped to the loop's own scratch area.
GREEN_PREFIXES = [
    AUTOIMPROVE / "work",
    AUTOIMPROVE / "results",
]


# Paths the loop can propose to but must not write without approval.
# Structural changes here compound and are hard to diff-review casually.
YELLOW_PREFIXES = [
    AUTOIMPROVE / "test-cases",
    AUTOIMPROVE / "directives",
]


# Paths the loop must never touch, even if a proposal tries.
RED_PREFIXES = [
    # Governance and rules (the Gödel rule: system cannot modify its own rules)
    HOME / ".claude" / "rules",
    HOME / "os" / "projects" / "agent-forge" / "governance",

    # Identity (values, TELOS, personality)
    HOME / "os" / "identity",

    # The autoimprove loop and evaluator itself (the scored cannot become the scorer)
    AUTOIMPROVE / "src",
    AUTOIMPROVE / "pyproject.toml",
    AUTOIMPROVE / "uv.lock",

    # Hooks (full shell access at session boundaries)
    HOME / "os" / "infrastructure" / "hooks",
    HOME / ".claude" / "hooks",

    # Work vault (cross-boundary prohibition: pai-os never writes to wrk-os)
    HOME / "wrk-os",

    # Live skill/agent/command files (loop operates on work/ copies only)
    HOME / ".claude" / "skills",
    HOME / ".claude" / "agents",
    HOME / ".claude" / "commands",
    HOME / ".claude" / "settings.json",
    HOME / ".claude" / "settings.local.json",
]


# Filename patterns that are always red regardless of location.
RED_FILENAME_FRAGMENTS = [
    ".env",
    "credential",
    "secret",
    "api_key",
    "apikey",
]


def _is_under(path: Path, prefix: Path) -> bool:
    """True if resolved path lives under resolved prefix."""
    try:
        path.resolve().relative_to(prefix.resolve())
        return True
    except (ValueError, OSError, FileNotFoundError):
        return False


def zone_of(path: str | Path) -> str:
    """
    Classify a path as RED, GREEN, YELLOW, or UNKNOWN.

    Order matters: red prefixes are checked first so nothing under a red
    prefix can accidentally be classified as green. Unknown paths fail closed.
    """
    p = Path(path).expanduser()

    # Red filename fragments apply anywhere
    name_lower = p.name.lower()
    for fragment in RED_FILENAME_FRAGMENTS:
        if fragment in name_lower:
            return "RED"

    # Red prefix checks
    for prefix in RED_PREFIXES:
        if _is_under(p, prefix) or p.resolve() == prefix.resolve():
            return "RED"

    # Green prefix checks
    for prefix in GREEN_PREFIXES:
        if _is_under(p, prefix):
            return "GREEN"

    # Yellow prefix checks
    for prefix in YELLOW_PREFIXES:
        if _is_under(p, prefix):
            return "YELLOW"

    return "UNKNOWN"


def is_writable_autonomously(path: str | Path) -> bool:
    """True only if the loop can write this path without David's approval."""
    return zone_of(path) == "GREEN"


class ZoneViolation(Exception):
    """Raised when the loop tries to write outside the green zone."""

    def __init__(self, path: str | Path, zone: str, reason: str = ""):
        self.path = str(path)
        self.zone = zone
        self.reason = reason
        message = (
            f"zone violation: path={self.path} zone={zone}. "
            f"autoimprove may only write autonomously to GREEN zone paths. "
            f"see projects/autoimprove/GOVERNANCE.md."
        )
        if reason:
            message = f"{message} context: {reason}"
        super().__init__(message)


def assert_writable(path: str | Path, reason: str = "") -> None:
    """Raise ZoneViolation unless the path is writable autonomously."""
    zone = zone_of(path)
    if zone != "GREEN":
        raise ZoneViolation(path, zone, reason)


def assert_source_readable(path: str | Path) -> None:
    """
    Loop-startup check. The loop reads skill source files from ~/.claude/skills/
    which are RED for writes but allowed for reads. This guard rejects source
    paths whose parent directory is suspicious (hooks, governance, identity).

    Rationale: the skill-source-path helper in loop_v2 could in principle be
    pointed at a red-zone file like a hook or governance doc. We fail the run
    at startup rather than silently copying it into work/.
    """
    p = Path(path).expanduser()
    forbidden_read_parents = [
        HOME / ".claude" / "rules",
        HOME / "os" / "identity",
        HOME / "os" / "infrastructure" / "hooks",
        HOME / ".claude" / "hooks",
        HOME / "os" / "projects" / "agent-forge" / "governance",
        HOME / "wrk-os",
    ]
    for prefix in forbidden_read_parents:
        if _is_under(p, prefix):
            raise ZoneViolation(
                p,
                "RED",
                "source path lives under a forbidden directory; "
                "autoimprove cannot read this file as a skill source",
            )
