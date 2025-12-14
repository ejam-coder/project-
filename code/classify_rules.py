import numpy as np

def classify_pose(landmarks):
    """
    Clasificación simple por reglas.
    Retorna etiqueta de acción detectada.
    """
    LEFT_SHOULDER = 11
    LEFT_WRIST = 15

    shoulder = landmarks[LEFT_SHOULDER]
    wrist = landmarks[LEFT_WRIST]

    if wrist[1] < shoulder[1]:
        return "HandUp"

    return "Neutral"
