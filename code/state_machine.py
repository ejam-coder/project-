import time

RIGHT_WRIST = 16
RIGHT_SHOULDER = 12

class PlayerState:
    def __init__(self, player_id):
        self.player_id = player_id
        self.state = "Idle"
        self.prev_wrist_y = None
        self.last_clap_time = 0
        self.last_action = "NONE"

    def detect_clap(self, landmarks):
        now = time.time()

        # Cooldown entre palmadas
        if now - self.last_clap_time < 0.4:
            return False

        wrist = landmarks[RIGHT_WRIST]
        shoulder = landmarks[RIGHT_SHOULDER]

        wrist_y = wrist[1]
        shoulder_y = shoulder[1]

        if self.prev_wrist_y is None:
            self.prev_wrist_y = wrist_y
            return False

        delta_y = wrist_y - self.prev_wrist_y
        self.prev_wrist_y = wrist_y

        # Movimiento descendente controlado
        if delta_y > 0.045 and wrist_y > shoulder_y:
            self.last_clap_time = now
            return True

        return False

    def update_state(self, landmarks):
        if self.state == "Idle":
            if self.detect_clap(landmarks):
                self.state = "ClapWait1"

        elif self.state == "ClapWait1":
            if self.detect_clap(landmarks):
                self.state = "AwaitAction"

        elif self.state == "ActionDetected":
            # Reset automático
            self.state = "Idle"
