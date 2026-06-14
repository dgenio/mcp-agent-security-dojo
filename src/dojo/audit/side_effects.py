"""Side-effect ledger.

A durable record of every side-effecting tool call an agent makes (action,
target, args, timestamp). The unsafe baseline executes side effects with no
approval gate and no decision record — the ledger is what makes that blast
radius visible and comparable against the governed path.

Entries can be persisted to ``DOJO_LEDGER_DIR`` (mirroring ``DOJO_TRACE_DIR``);
when the env var is unset the ledger is kept in memory only.
"""

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class SideEffectLedger:
    entries: list[dict] = field(default_factory=list)

    def record(self, action: str, target: str, args: dict) -> dict:
        """Append a side-effect record. No approval or decision is consulted."""
        entry = {
            "action": action,
            "target": target,
            "args": args,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.entries.append(entry)
        return entry

    def write(self, scenario: str) -> str | None:
        """Persist the ledger to ``DOJO_LEDGER_DIR`` if configured."""
        ledger_dir = os.getenv("DOJO_LEDGER_DIR")
        if not ledger_dir:
            return None
        path = Path(ledger_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        # Sanitize scenario to prevent path traversal
        safe_scenario = Path(scenario).name or "unknown_scenario"
        out = path / f"{safe_scenario}_ledger_{uuid.uuid4().hex[:8]}.json"
        
        out.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")
        return str(out)
