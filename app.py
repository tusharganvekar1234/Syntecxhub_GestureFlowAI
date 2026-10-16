
import time
from collections import Counter, deque

import cv2
import mediapipe as mp

from gestureflow.recognizer import GestureRecognizer
from gestureflow.actions import ActionEngine


# DroidCam was detected at camera index 2 on this laptop.
CAMERA_INDEX = 2


def main():
    # Use DirectShow on Windows to access the DroidCam virtual camera.
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print(f"ERROR: Could not open camera at index {CAMERA_INDEX}.")
        print("Check that DroidCam is running on your phone and laptop.")
        camera.release()
        return

    # Request a reasonable resolution for real-time processing.
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Verify that the camera actually supplies a frame.
    success, test_frame = camera.read()

    if not success or test_frame is None:
        print("ERROR: Camera opened, but no video frame was received.")
        print("Check the DroidCam connection and try again.")
        camera.release()
        return

    print("DroidCam connected successfully!")
    print(f"Camera resolution: {test_frame.shape[1]} x {test_frame.shape[0]}")

    recognizer = GestureRecognizer()
    action_engine = ActionEngine(cooldown=1.0)

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    history = deque(maxlen=7)
    gesture_counts = Counter()
    recent_actions = deque(maxlen=4)

    previous_gesture = "UNKNOWN"
    last_time = time.perf_counter()
    fps = 0.0
    notification = "Show a gesture to begin"
    notification_until = 0.0

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.65,
            min_tracking_confidence=0.65,
        ) as hands:

            print("\nGestureFlow AI — Smart Action Mode")
            print("Camera: DroidCam")
            print("Q = quit | R = reset session")

            while True:
                success, frame = camera.read()

                if not success or frame is None:
                    print("ERROR: Could not read a camera frame.")
                    break

                # Mirror the image for a natural webcam-style experience.
                frame = cv2.flip(frame, 1)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                now = time.perf_counter()
                elapsed = now - last_time
                last_time = now

                if elapsed > 0:
                    instant_fps = 1.0 / elapsed
                    fps = (
                        instant_fps
                        if fps == 0
                        else 0.85 * fps + 0.15 * instant_fps
                    )

                gesture = "NO HAND"
                confidence = 0.0
                description = "Show your hand to begin"

                if results.multi_hand_landmarks:
                    # Use the first detected hand for action control.
                    hand = results.multi_hand_landmarks[0]
                    result = recognizer.recognize(hand)

                    history.append(result.name)
                    gesture = Counter(history).most_common(1)[0][0]
                    confidence = result.confidence
                    description = result.description

                    # Draw landmarks for all detected hands.
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                        )

                    if gesture not in ("UNKNOWN", "NO HAND"):
                        if gesture != previous_gesture:
                            gesture_counts[gesture] += 1

                        event = action_engine.process(gesture)

                        if event:
                            recent_actions.appendleft(
                                f"{event.gesture} -> {event.action}"
                            )
                            notification = f"ACTION: {event.action}"
                            notification_until = now + 1.5

                    previous_gesture = gesture

                else:
                    history.clear()
                    previous_gesture = "NO HAND"
                    action_engine.process("NO HAND")

                # Dark header
                cv2.rectangle(
                    frame, (0, 0), (frame.shape[1], 90),
                    (20, 24, 34), -1
                )
                cv2.putText(
                    frame, "GESTUREFLOW AI", (24, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 255), 2
                )
                cv2.putText(
                    frame, "REAL-TIME GESTURE & ACTION ENGINE", (25, 67),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (120, 220, 210), 1
                )

                # Current gesture panel
                cv2.rectangle(
                    frame, (20, 115), (400, 255),
                    (28, 34, 48), -1
                )
                cv2.putText(
                    frame, "DETECTED GESTURE", (38, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (170, 185, 200), 1
                )
                cv2.putText(
                    frame, gesture, (38, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (80, 240, 190), 2
                )
                cv2.putText(
                    frame, f"Heuristic score: {confidence:.0%}", (38, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (220, 225, 235), 1
                )
                cv2.putText(
                    frame, description[:38], (38, 242),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42,
                    (170, 185, 200), 1
                )

                # Performance and tracking
                right = frame.shape[1] - 20
                cv2.rectangle(
                    frame, (right - 250, 110), (right, 215),
                    (28, 34, 48), -1
                )
                cv2.putText(
                    frame, f"FPS: {fps:.1f}", (right - 225, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (80, 240, 190), 2
                )
                cv2.putText(
                    frame,
                    "TRACKING: ACTIVE"
                    if results.multi_hand_landmarks
                    else "TRACKING: SEARCHING",
                    (right - 225, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.43,
                    (80, 240, 190)
                    if results.multi_hand_landmarks
                    else (150, 170, 190),
                    1,
                )
                cv2.putText(
                    frame, f"ACTIONS: {action_engine.total_actions}",
                    (right - 225, 202),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.43,
                    (220, 225, 235), 1
                )

                # Action notification
                if now < notification_until:
                    cv2.rectangle(
                        frame, (20, 275), (440, 325),
                        (24, 75, 65), -1
                    )
                    cv2.putText(
                        frame, notification, (35, 306),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                        (130, 255, 205), 2
                    )

                # Recent action events
                panel_top = 345
                cv2.rectangle(
                    frame, (20, panel_top), (440, panel_top + 145),
                    (28, 34, 48), -1
                )
                cv2.putText(
                    frame, "RECENT ACTION EVENTS",
                    (35, panel_top + 27),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                    (170, 185, 200), 1
                )

                if recent_actions:
                    for i, action_text in enumerate(recent_actions):
                        cv2.putText(
                            frame, action_text[:35],
                            (35, panel_top + 57 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (100, 240, 190), 1
                        )
                else:
                    cv2.putText(
                        frame, "No actions triggered yet",
                        (35, panel_top + 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (180, 190, 205), 1
                    )

                # Session gesture statistics
                bottom = frame.shape[0] - 20
                cv2.rectangle(
                    frame, (20, bottom - 100),
                    (frame.shape[1] - 20, bottom),
                    (20, 24, 34), -1
                )
                cv2.putText(
                    frame, "SESSION GESTURE COUNTS",
                    (35, bottom - 72),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                    (170, 185, 200), 1
                )

                names = [
                    "OPEN PALM", "FIST", "THUMBS UP",
                    "PEACE", "POINTING", "PINCH"
                ]

                for i, name in enumerate(names):
                    col = i % 3
                    row = i // 3
                    x = 35 + col * 260
                    y = bottom - 43 + row * 24

                    cv2.putText(
                        frame, f"{name}: {gesture_counts[name]}",
                        (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.43,
                        (230, 235, 240), 1
                    )

                cv2.putText(
                    frame, "Q: QUIT  |  R: RESET SESSION",
                    (frame.shape[1] - 315, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42,
                    (220, 225, 235), 1
                )

                cv2.imshow(
                    "GestureFlow AI | Smart Action Engine",
                    frame
                )

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break

                elif key == ord("r"):
                    history.clear()
                    gesture_counts.clear()
                    recent_actions.clear()
                    action_engine.reset()

                    notification = "Session reset"
                    notification_until = time.perf_counter() + 1.5

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("GestureFlow AI stopped. Camera released.")


if __name__ == "__main__":
    main()
