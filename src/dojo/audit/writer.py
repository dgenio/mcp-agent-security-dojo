"""Audit trace writer."""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dojo.audit.trace import AuditTrace


def write_trace(trace: AuditTrace) -> str:
    trace_dir = Path(os.getenv("DOJO_TRACE_DIR", "traces"))
    trace_dir.mkdir(parents=True, exist_ok=True)
    # Microsecond precision plus a short random suffix so traces written within
    # the same second (tight loops, parallel runs) never overwrite each other
    # and audit evidence is preserved.
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    path = trace_dir / f"{trace.scenario}_{stamp}_{uuid.uuid4().hex[:8]}.json"
    payload = {
        "scenario": trace.scenario,
        "decisions": trace.decisions,
        "actions": trace.actions,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)
