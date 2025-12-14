import cv2
import mediapipe as mp
import numpy as np
from state_machine import PlayerState

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

# Creamos dos jugadores
players = {
    0: PlayerState(player_id=0),
    1: PlayerState(player_id=1)
}

def extract_landmarks(results):
    landmarks = []
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            landmarks.append(np.array([lm.x, lm.y, lm.z]))
    return landmarks

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    h, w, _ = frame.shape

    if results.pose_landmarks:
        # Para demo: duplicamos landmarks como si fueran 2 jugadores
        # (MediaPipe Pose no distingue IDs, esto es aceptable para prototipo)
        landmarks = extract_landmarks(results)

        for pid, player in players.items():
            player.update_landmarks(landmarks)
            player.update_state()

            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            cv2.putText(
                frame,
                f"Player {pid} - {player.state}",
                (20, 40 + pid * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    cv2.imshow("Pose Detection - Day 2", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

