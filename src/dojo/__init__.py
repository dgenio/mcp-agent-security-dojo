"""MCP agent security dojo."""

from dojo.agents.governed_agent import run_governed_scenario
from dojo.agents.unsafe_agent import run_unsafe_scenario

__all__ = ["run_unsafe_scenario", "run_governed_scenario"]
