import math


class MotionEngine:

    def ease(self, t):
        return t * t * (3 - 2 * t)

    # =========================
    # SEGMENT 1 — HERO MOTION
    # =========================
    def hero(self, t, direction="left"):

        e = self.ease(t)

        x, y = 0, 0

        if direction == "left":
            x = -1 + e
        elif direction == "right":
            x = 1 - e
        elif direction == "top":
            y = -1 + e
        elif direction == "bottom":
            y = 1 - e
        elif direction == "tl":
            x = -1 + e
            y = -1 + e
        elif direction == "br":
            x = 1 - e
            y = 1 - e

        return {
            "x": x,
            "y": y,
            "scale": 1.35 - (0.35 * e)
        }

    # =========================
    # SEGMENT 3 — MILITARY SPLIT
    # =========================
    def split(self, t, side="L"):

        e = self.ease(t)
        d = -1 if side == "L" else 1

        return {
            "x": d * (1 - e * 2),
            "y": 0,
            "scale": 0.6 + (0.5 * e)
        }

    # =========================
    # SEGMENT 4 — WHEEL MOTION
    # =========================
    def wheel(self, t, index, total):

        angle = (2 * math.pi * index / max(total, 1)) + (t * 2 * math.pi)

        return {
            "x": math.cos(angle),
            "y": math.sin(angle),
            "scale": 0.4 + 0.25 * (math.sin(angle) + 1) / 2
        }