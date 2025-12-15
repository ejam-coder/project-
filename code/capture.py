import cv2
import mediapipe as mp
import numpy as np

from state_machine import PlayerState
from classify_rules import classify_pose

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Jugadores (Player 1 y Player 2)
players = {
    1: PlayerState(player_id=1),
    2: PlayerState(player_id=2)
}

def extract_landmarks(results):
    landmarks = []
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            landmarks.append(np.array([lm.x, lm.y, lm.z]))
    return landmarks

# =========================
# MAIN LOOP
# =========================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks_np = extract_landmarks(results)

        for pid, player in players.items():
            player.update_state(landmarks_np)

            # Clasificar SOLO cuando está listo
            if player.state == "AwaitAction":
                action = classify_pose(results.pose_landmarks.landmark)
                if action != "NONE":
                    player.state = "ActionDetected"
                    player.last_action = action

            # Dibujar esqueleto
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # UI
            cv2.putText(
                frame,
                f"Player {pid} - {player.state}",
                (20, 40 + (pid - 1) * 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Action: {player.last_action}",
                (20, 70 + (pid - 1) * 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

    cv2.imshow("Pose Detection - Day 3", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
