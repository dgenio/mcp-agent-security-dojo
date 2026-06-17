"""Plausible-but-inadequate logging (the unsafe baseline's idea of an audit log).

Real teams usually *do* log — they just log the wrong things. A free-text
"handled request" line feels like coverage on a dashboard, yet it omits
everything an audit or incident reconstruction needs: which actor ran the step,
which resource it touched, the decision rationale, the tool arguments, and a
reliable timestamp.

This makes the gap to the governed structured trace (an ``effect`` + ``reason``
per decision, see ``src/dojo/audit/trace.py``) a concrete teaching point rather
than a presence-vs-absence one. It complements the side-effect ledger
(``src/dojo/audit/side_effects.py``), which records *that* an action happened:
this shows that the unsafe *decision/reasoning* record is missing.
"""

from dataclasses import dataclass, field


@dataclass
class InadequateLog:
    """A log that looks instrumented but is useless for audit."""

    lines: list[str] = field(default_factory=list)

    def handled(self) -> str:
        """Append a generic line. Deliberately records no actor, no resource, no
        decision rationale, no tool arguments, and no timestamp."""
        line = "INFO: handled request"
        self.lines.append(line)
        return line
