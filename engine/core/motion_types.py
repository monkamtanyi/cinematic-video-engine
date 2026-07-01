import numpy as np


class MotionEngine:
    """
    v1.0 Unified Motion Engine
    Fully aligned with renderer segments (A–D)
    """

    def __init__(self):
        self.cx = 540
        self.cy = 960

    def ease(self, t):
        return 3*t**2 - 2*t**3

    # -------------------------------------------------
    # SEGMENT A — cinematic multi-phase motion
    # -------------------------------------------------
    def segment_a(self, t, i):
        e = self.ease(t)

        x = self.cx + 250 * np.sin(2*np.pi*e + i)
        y = self.cy + 150 * np.cos(2*np.pi*e + i * 0.5)
        z = 1 + 0.25 * np.sin(np.pi * e)

        return x, y, z

    # -------------------------------------------------
    # SEGMENT B — FORMATION APPROACH + SPLIT LOGIC
    # (THIS IS WHERE YOUR REAL REQUIREMENT LIVES)
    # -------------------------------------------------
    def segment_b(self, t, i):

        # two-line formation (implicit grouping)
        is_left_group = (i % 2 == 0)

        # approach viewer (depth illusion via scale + centering)
        y = self.cy + (1 - t) * 180

        # slight convergence toward center line
        x = self.cx + (-120 if is_left_group else 120) * (1 - t)

        # zoom in as they approach viewer
        z = 0.9 + 0.4 * t

        return x, y, z

    # -------------------------------------------------
    # SEGMENT C — MILITARY SPLIT (UPDATED CORRECTLY)
    # -------------------------------------------------
    def segment_c(self, t, i):

        direction = -1 if i % 2 == 0 else 1

        # approach center first
        approach = (1 - t)

        x = self.cx + direction * 220 * approach
        y = self.cy

        # stronger depth illusion
        z = 0.8 + 0.7 * t

        return x, y, z

    # -------------------------------------------------
    # SEGMENT D — GEOMETRIC COLLAPSE SYSTEM
    # -------------------------------------------------
    def segment_d(self, t, i):

        angle = 2 * np.pi * t + i
        radius = 300 * (1 - t)

        x = self.cx + radius * np.cos(angle)
        y = self.cy + radius * np.sin(angle)

        z = 1.2 - t

        return x, y, z