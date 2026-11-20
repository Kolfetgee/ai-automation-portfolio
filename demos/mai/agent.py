"""Local deterministic agent-state mock, without an LLM or copyrighted character data."""
from __future__ import annotations

from collections import deque


class Agent:
    def __init__(self, memory_size: int = 5):
        if not 1 <= memory_size <= 20:
            raise ValueError("memory_size must be 1-20")
        self.notes: deque[str] = deque(maxlen=memory_size)
        self.state = "READY"

    def turn(self, message: str) -> dict:
        if not isinstance(message, str) or not (1 <= len(message) <= 500):
            raise ValueError("message must be a string of 1-500 characters")
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("blank messages are not supported")
        if cleaned.lower() == "stop":
            self.state = "STOP"
            return self._result("silence", None)
        if self.state == "STOP":
            return self._result("silence", None)
        if cleaned.lower().startswith("remember:"):
            note = cleaned[len("remember:"):].strip()
            if not 1 <= len(note) <= 100:
                raise ValueError("synthetic note must be 1-100 characters")
            self.notes.append(note)
            return self._result("reply", "Stored one local synthetic note.")
        if cleaned.lower() == "recall":
            text = "; ".join(self.notes) if self.notes else "No local notes stored."
            return self._result("reply", text)
        if cleaned.lower() in {"hello", "hi"}:
            return self._result("reply", "Hello. This is a deterministic offline agent-state demonstration.")
        return self._result("escalate", "No verified rule available; human review is required.")

    def resume(self, *, owner_confirmed: bool = False) -> None:
        if owner_confirmed is not True:
            raise PermissionError("Owner confirmation required to resume")
        self.state = "READY"

    def _result(self, action: str, text: str | None) -> dict:
        return {"action": action, "text": text, "state": self.state,
                "memory_items": len(self.notes), "model_called": False}
