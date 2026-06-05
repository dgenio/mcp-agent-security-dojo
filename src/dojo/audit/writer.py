"""Audit trace writer."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dojo.audit.trace import AuditTrace


def write_trace(trace: AuditTrace) -> str:
    trace_dir = Path(os.getenv("DOJO_TRACE_DIR", "traces"))
    trace_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = trace_dir / f"{trace.scenario}_{stamp}.json"
    payload = {
        "scenario": trace.scenario,
        "decisions": trace.decisions,
        "actions": trace.actions,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)
