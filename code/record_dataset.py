import cv2
import mediapipe as mp
import csv
import os
import time

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)

PLAYER_ID = 2
SAVE_ROOT = f"../data/landmarks_csv/player_{PLAYER_ID}"
FRAMES_TO_RECORD = 250
COUNTDOWN_TIME = 5

os.makedirs(SAVE_ROOT, exist_ok=True)

def flatten_landmarks(landmarks):
    row = []
    for lm in landmarks:
        row.extend([lm.x, lm.y, lm.z])
    return row

print("1=SHOOT | 2=RELOAD | 3=COVER | q=Salir")

mode = "IDLE"
current_label = None
start_time = None
frames_recorded = 0
writer = None
file_handle = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    key = cv2.waitKey(1) & 0xFF

    if mode == "IDLE":
        if key == ord("1"):
            current_label = "SHOOT"
        elif key == ord("2"):
            current_label = "RELOAD"
        elif key == ord("3"):
            current_label = "COVER"
        elif key == ord("q"):
            break

        if current_label:
            mode = "COUNTDOWN"
            start_time = time.time()
            frames_recorded = 0

    if mode == "COUNTDOWN":
        remaining = int(COUNTDOWN_TIME - (time.time() - start_time))
        cv2.putText(frame, f"Get ready: {remaining}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        if remaining <= 0:
            mode = "RECORDING"
            file_handle = open(f"{SAVE_ROOT}/{current_label}.csv", "a", newline="")
            writer = csv.writer(file_handle)

    if mode == "RECORDING" and results.pose_landmarks:
        row = flatten_landmarks(results.pose_landmarks.landmark)
        row.append(current_label)
        writer.writerow(row)
        frames_recorded += 1

        cv2.putText(frame, f"{current_label}: {frames_recorded}/{FRAMES_TO_RECORD}",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if frames_recorded >= FRAMES_TO_RECORD:
            file_handle.close()
            mode = "IDLE"
            current_label = None

    cv2.imshow("Dataset Recorder", frame)

cap.release()
cv2.destroyAllWindows()
