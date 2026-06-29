import numpy as np


class MotionEngine:

    def __init__(self):
        self.cx = 960
        self.cy = 540

    # smooth easing (important for cinematic feel)
    def ease(self, t):
        return 3*t**2 - 2*t**3

    # SEGMENT 1 — HERO MOTION (multi-directional + zoom wave)
    def field_motion(self, t, i):

        e = self.ease(t)

        x = self.cx + 300*np.sin(2*np.pi*e + i)
        y = self.cy + 180*np.cos(2*np.pi*e + i*0.5)

        zoom = 1 + 0.25*np.sin(np.pi * e)

        return x, y, zoom

    # SEGMENT 2 — CONVEYOR BELT
    def conveyor(self, t, i):

        spacing = 250

        x = 1920 - (1920 + spacing) * t + (i % 8) * spacing
        y = self.cy + 60*np.sin(i + t*2*np.pi)

        zoom = 0.85 + 0.15*np.sin(t*np.pi)

        return x, y, zoom

    # SEGMENT 3 — 3D SPLIT
    def split_depth(self, t, i):

        side = -1 if i % 2 == 0 else 1

        depth = 1 + t*1.2

        x = self.cx + side * (400 * (1 - t))
        y = self.cy + 80*np.sin(i + t*np.pi)

        zoom = depth

        return x, y, zoom

    # SEGMENT 4 — RADIAL CLIMAX
    def radial_motion(self, t, i):

        angle = 2*np.pi*t + i

        radius = 400 * (1 - t)

        x = self.cx + radius * np.cos(angle)
        y = self.cy + radius * np.sin(angle)

        zoom = 1.3 - t

        return x, y, zoom