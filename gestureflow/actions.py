
from collections import deque
from dataclasses import dataclass
from time import monotonic
from typing import Optional


@dataclass
class ActionEvent:
    gesture: str
    action: str
    timestamp: float


class ActionEngine:
    """Maps stable gestures to safe, simulated demo actions."""

    GESTURE_ACTIONS = {
        "OPEN PALM": "PLAY",
        "FIST": "PAUSE",
        "THUMBS UP": "VOLUME UP",
        "PEACE": "NEXT SLIDE",
        "POINTING": "PREVIOUS SLIDE",
        "PINCH": "SELECT",
    }

    def __init__(self, cooldown: float = 1.0):
        self.cooldown = cooldown
        self.last_action_time = 0.0
        self.last_gesture = None
        self.events = deque(maxlen=10)
        self.total_actions = 0

    def process(self, gesture: str) -> Optional[ActionEvent]:
        """Emit an event only for a new gesture after the cooldown."""
        now = monotonic()

        if gesture not in self.GESTURE_ACTIONS:
            self.last_gesture = None
            return None

        if gesture == self.last_gesture:
            return None

        self.last_gesture = gesture

        if now - self.last_action_time < self.cooldown:
            return None

        event = ActionEvent(
            gesture=gesture,
            action=self.GESTURE_ACTIONS[gesture],
            timestamp=now,
        )

        self.last_action_time = now
        self.events.appendleft(event)
        self.total_actions += 1

        return event

    def reset(self):
        """Clear session event history and counters."""
        self.events.clear()
        self.total_actions = 0
        self.last_action_time = 0.0
        self.last_gesture = None
