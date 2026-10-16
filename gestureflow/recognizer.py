
from dataclasses import dataclass
from typing import Optional

import math


@dataclass
class GestureResult:
    name: str
    confidence: float
    description: str


class GestureRecognizer:
    """Rule-based hand gesture recognition using MediaPipe landmarks."""

    GESTURES = {
        "OPEN PALM": "All four fingers extended",
        "FIST": "Fingers curled toward the palm",
        "THUMBS UP": "Thumb extended, other fingers curled",
        "PEACE": "Index and middle fingers extended",
        "POINTING": "Index finger extended",
        "PINCH": "Thumb and index finger close together",
        "UNKNOWN": "Gesture not confidently recognized",
    }

    def _distance(self, a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

    def recognize(self, hand_landmarks) -> GestureResult:
        """
        Accepts MediaPipe's 21 hand landmarks.
        Returns a gesture label, heuristic confidence and description.
        """
        lm = hand_landmarks.landmark

        # Finger landmarks: tip, PIP joint and MCP joint.
        # For the four non-thumb fingers, higher image y means lower on screen.
        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y
        ring_up = lm[16].y < lm[14].y
        pinky_up = lm[20].y < lm[18].y

        # Thumb extension uses horizontal displacement as a simple
        # first-pass heuristic. Hand orientation can affect this result.
        thumb_extended = (
            abs(lm[4].x - lm[2].x)
            > abs(lm[3].x - lm[2].x) * 1.25
        )

        extended_count = sum(
            [index_up, middle_up, ring_up, pinky_up]
        )

        # Pinch distance is normalized by the approximate palm width.
        palm_width = max(self._distance(lm[5], lm[17]), 0.001)
        pinch_ratio = self._distance(lm[4], lm[8]) / palm_width

        if pinch_ratio < 0.28:
            return GestureResult(
                "PINCH", 0.90, self.GESTURES["PINCH"]
            )

        if thumb_extended and extended_count == 0:
            return GestureResult(
                "THUMBS UP", 0.78, self.GESTURES["THUMBS UP"]
            )

        if (
            index_up and middle_up
            and not ring_up and not pinky_up
        ):
            return GestureResult(
                "PEACE", 0.88, self.GESTURES["PEACE"]
            )

        if index_up and not middle_up and not ring_up and not pinky_up:
            return GestureResult(
                "POINTING", 0.85, self.GESTURES["POINTING"]
            )

        if extended_count == 4:
            return GestureResult(
                "OPEN PALM", 0.92, self.GESTURES["OPEN PALM"]
            )

        if extended_count == 0 and not thumb_extended:
            return GestureResult(
                "FIST", 0.88, self.GESTURES["FIST"]
            )

        return GestureResult(
            "UNKNOWN", 0.50, self.GESTURES["UNKNOWN"]
        )
