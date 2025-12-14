import numpy as np
from collections import deque
import time

class PlayerState:
    def __init__(self, player_id):
        self.player_id = player_id
        self.state = "Idle"
        self.landmarks = None
        self.prev_landmarks = None
        self.history = deque(maxlen=5)
        self.last_clap_time = 0

    def update_landmarks(self, landmarks):
        self.prev_landmarks = self.landmarks
        self.landmarks = landmarks
        if landmarks is not None:
            self.history.append(landmarks)

    def detect_clap(self):
        if self.prev_landmarks is None or self.landmarks is None:
            return False

        # Índices MediaPipe
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        LEFT_HIP = 23
        RIGHT_HIP = 24

        lw = self.landmarks[LEFT_WRIST]
        rw = self.landmarks[RIGHT_WRIST]
        lh = self.landmarks[LEFT_HIP]
        rh = self.landmarks[RIGHT_HIP]

        hip_center = (lh + rh) / 2

        # Distancias
        dist_l = np.linalg.norm(lw - hip_center)
        dist_r = np.linalg.norm(rw - hip_center)

        # Velocidad vertical
        prev_lw = self.prev_landmarks[LEFT_WRIST]
        speed_l = abs(lw[1] - prev_lw[1])

        threshold_dist = 0.15
        threshold_speed = 0.04

        clap_detected = (
            (dist_l < threshold_dist and speed_l > threshold_speed) or
            (dist_r < threshold_dist and speed_l > threshold_speed)
        )

        return clap_detected

    def update_state(self):
        clap = self.detect_clap()
        now = time.time()

        if self.state == "Idle" and clap:
            self.state = "ClapWait1"
            self.last_clap_time = now

        elif self.state == "ClapWait1":
            if clap and (now - self.last_clap_time) < 1.2:
                self.state = "AwaitAction"
            elif (now - self.last_clap_time) > 2:
                self.state = "Idle"

        elif self.state == "AwaitAction":
            # Aquí luego se clasificará la pose
            # Por ahora simulamos detección
            if len(self.history) >= 5:
                self.state = "ActionDetected"

        elif self.state == "ActionDetected":
            # Se puede resetear o avanzar
            self.state = "Idle"

