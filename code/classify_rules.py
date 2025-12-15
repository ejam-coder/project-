import numpy as np

def angle(a, b, c):
    ba = a - b
    bc = c - b
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))

def is_forward(vec):
    return vec[2] < -0.15

def distance(a, b):
    return np.linalg.norm(a - b)

# Landmarks
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
NOSE = 0

# Poses
def classify_pose(landmarks):
    lm = [np.array([p.x, p.y, p.z]) for p in landmarks]

    ls, rs = lm[LEFT_SHOULDER], lm[RIGHT_SHOULDER]
    le, re = lm[LEFT_ELBOW], lm[RIGHT_ELBOW]
    lw, rw = lm[LEFT_WRIST], lm[RIGHT_WRIST]
    nose = lm[NOSE]

    left_forearm = lw - le
    right_forearm = rw - re

    angle_l = angle(ls, le, lw)
    angle_r = angle(rs, re, rw)

    # SHOOT
    if (
        angle_l > 150 and 
        is_forward(left_forearm) and 
        lw[2] < ls[2]
    ) or (
        angle_r > 150 and 
        is_forward(right_forearm) and 
        rw[2] < rs[2]
    ):
        return "SHOOT"

    # RELOAD
    if (
        lw[1] > nose[1] + 0.05 and
        angle_l < 130 and
        rw[1] < rs[1] - 0.05
    ) or (
        rw[1] > nose[1] + 0.05 and
        angle_r < 130 and
        lw[1] < ls[1] - 0.05
    ):
        return "RELOAD"

    # COVER
    if (
        distance(lw, rw) < 0.12 and
        lw[1] > ls[1] and
        abs(lw[1] - rw[1]) < 0.08
    ):
        return "COVER"

    return "NONE"
