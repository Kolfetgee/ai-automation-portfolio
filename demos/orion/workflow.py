"""Deterministic Maker/Checker/Owner state machine, not an AI execution engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


class TransitionError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Workflow:
    task_id: str
    objective: str
    state: str = "AWAIT_MAKER"
    artifact: dict[str, Any] | None = None
    checker_note: str | None = None
    events: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.task_id, str) or not self.task_id.startswith("SYN-"):
            raise ValueError("Use an explicit SYN-* synthetic task ID")
        if not isinstance(self.objective, str) or not (5 <= len(self.objective.strip()) <= 250):
            raise ValueError("Objective must be between 5 and 250 characters")
        self._event("system", "TASK_CREATED")

    def _event(self, role: str, event: str) -> None:
        self.events.append({"at": _now(), "role": role, "event": event})

    def submit_maker(self, artifact: dict[str, Any]) -> None:
        if self.state != "AWAIT_MAKER":
            raise TransitionError("Maker may submit only when awaiting a candidate")
        if (not isinstance(artifact, dict) or set(artifact) != {"summary", "test_claims"}
                or not isinstance(artifact["summary"], str)
                or not (10 <= len(artifact["summary"].strip()) <= 500)
                or not isinstance(artifact["test_claims"], list)
                or len(artifact["test_claims"]) > 20
                or not all(isinstance(t, str) and 1 <= len(t) <= 100 for t in artifact["test_claims"])):
            raise ValueError("Artifact must have bounded summary and list of claimed tests")
        self.artifact = {"summary": artifact["summary"].strip(), "test_claims": list(artifact["test_claims"])}
        self.state = "AWAIT_CHECKER"
        self._event("maker", "CANDIDATE_SUBMITTED")

    def review_checker(self, verdict: str, evidence: str) -> None:
        if self.state != "AWAIT_CHECKER":
            raise TransitionError("Checker may review only a submitted candidate")
        if verdict not in {"PASS", "NEEDS_FIXES", "BLOCKED"}:
            raise ValueError("Unsupported verdict")
        if not isinstance(evidence, str) or not (15 <= len(evidence.strip()) <= 1000):
            raise ValueError("Checker evidence must be 15-1000 characters")
        self.checker_note = evidence.strip()
        self.state = {"PASS": "AWAIT_OWNER", "NEEDS_FIXES": "REJECTED", "BLOCKED": "REJECTED"}[verdict]
        self._event("checker", verdict)

    def owner_decide(self, approve: bool, reason: str) -> None:
        if self.state != "AWAIT_OWNER":
            raise TransitionError("Owner can approve only after independent checker PASS")
        if type(approve) is not bool:
            raise ValueError("Approval must be boolean")
        if not isinstance(reason, str) or not (5 <= len(reason.strip()) <= 300):
            raise ValueError("Owner must record a reason")
        self.state = "APPROVED" if approve else "REJECTED"
        self._event("owner", f"DECISION_{'APPROVED' if approve else 'REJECTED'}: {reason.strip()}")

    def stop(self, reason: str) -> None:
        if not isinstance(reason, str) or len(reason.strip()) < 5:
            raise ValueError("Reason required for STOP")
        self.state = "STOP"
        self._event("owner", "STOP: " + reason.strip())

    def snapshot(self) -> dict[str, Any]:
        return {"task_id": self.task_id, "objective": self.objective,
                "state": self.state, "artifact": self.artifact,
                "checker_note": self.checker_note, "events": list(self.events),
                "side_effects_executed": False}
