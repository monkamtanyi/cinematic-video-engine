import numpy as np


class MotionEngine:

    def __init__(self):
        self.cx = 960
        self.cy = 540

    # -------------------------------------------------
    # SEGMENT 1 (FIXED)
    # bottom → center → pause → zoom → exit
    # -------------------------------------------------
    def segment_1(self, t, idx):

        # bottom → center
        y = 1080 - (t * 540)

        # pause + zoom pulse
        zoom = 1.0 + 0.05 * np.sin(t * np.pi * 2)

        # exit
        if t > 0.75:
            y -= (t - 0.75) * 1200

        return self.cx, y, zoom

    # -------------------------------------------------
    # SEGMENT 2 - FILMSTRIP
    # -------------------------------------------------
    def segment_2(self, t, idx):

        x = 1920 + idx * 200 - (t * 1200)
        y = self.cy

        zoom = 1.0 + 0.03 * np.sin(t * np.pi * 2)

        return x, y, zoom

    # -------------------------------------------------
    # SEGMENT 3 - CORRIDOR PEEL
    # -------------------------------------------------
    def segment_3(self, t, idx):

        offset = (idx % 2) * 120 - 60
        x = self.cx + offset + (t * (-300 if idx % 2 == 0 else 300))
        y = self.cy

        zoom = 1.0

        return x, y, zoom

    # -------------------------------------------------
    # SEGMENT 4 - WHEEL → STAR → CIRCLE
    # -------------------------------------------------
    def segment_4(self, t, idx, total):

        phase = t

        if phase < 0.33:
            angle = phase * 2 * np.pi
            x = self.cx + 200 * np.cos(angle + idx)
            y = self.cy + 200 * np.sin(angle + idx)

        elif phase < 0.66:
            # star
            star_map = [(0, -200), (-200, 0), (0, 200), (200, 0)]
            x, y = star_map[idx % 4]
            x += self.cx
            y += self.cy

        else:
            # circle
            angle = (idx / total) * 2 * np.pi
            x = self.cx + 180 * np.cos(angle)
            y = self.cy + 180 * np.sin(angle)

        return x, y, 1.0