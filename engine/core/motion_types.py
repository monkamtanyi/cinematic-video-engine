import numpy as np


class MotionEngine:
    """
    Motion System v3 - Frame-Based Cinematic Engine

    Instead of MoviePy FX:
    → returns (x, y, scale) per frame
    """

    def __init__(self):
        self.center = (960, 540)

    def _ease(self, t):
        return 3 * t**2 - 2 * t**3

    # --------------------------------------------------
    # 🎬 SEGMENT 1: FULL MOTION FIELD (50%)
    # --------------------------------------------------
    def segment_1(self, t, i):
        e = self._ease(t)

        # multi-directional motion
        x = 960 + 200 * np.sin(e * 2 * np.pi + i)
        y = 540 + 120 * np.cos(e * 2 * np.pi + i * 0.7)

        # zoom breathing
        scale = 1.0 + 0.3 * np.sin(e * np.pi)

        return x, y, scale

    # --------------------------------------------------
    # 🎬 SEGMENT 2: CONVEYOR BELT (15%)
    # --------------------------------------------------
    def segment_2(self, t, i):
        x = 1920 - (1920 * t) + (i % 5) * 220
        y = 540

        scale = 0.8 + 0.2 * np.sin(t * np.pi)

        return x, y, scale

    # --------------------------------------------------
    # 🎬 SEGMENT 3: 3D SPLIT APPROACH (15%)
    # --------------------------------------------------
    def segment_3(self, t, i):
        z = 1 + (1 - t) * 2  # fake depth

        x = 960 + ((i % 2) * 2 - 1) * 300 * (1 - t)
        y = 540 + np.sin(i + t * np.pi) * 50

        scale = z

        return x, y, scale

    # --------------------------------------------------
    # 🎬 SEGMENT 4: SPIN + STAR EXPLOSION (20%)
    # --------------------------------------------------
    def segment_4(self, t, i):
        angle = t * 6 * np.pi + i

        radius = 300 * (1 - t)

        x = 960 + radius * np.cos(angle)
        y = 540 + radius * np.sin(angle)

        scale = 1.2 - t

        return x, y, scale