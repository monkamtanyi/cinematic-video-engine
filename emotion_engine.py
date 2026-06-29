import math
import random


class MotionEngine:

    def rand(self):
        return random.choice([-1, 1])

    def ease(self, t):
        return t * t * (3 - 2 * t)

    # SEGMENT 1 — MULTI DIRECTION
    def hero(self, t, direction):

        e = self.ease(t)

        x = 0
        y = 0

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
            "scale": 1.3 - 0.3 * e
        }

    # SEGMENT 2 — CONVEYOR
    def conveyor(self, t, index):
        return {
            "x": index * 1.2 - (t * 3.0),
            "y": 0,
            "scale": 0.35
        }

    # SEGMENT 3 — MILITARY SPLIT
    def split(self, t, side):

        e = self.ease(t)

        direction = -1 if side == "L" else 1

        return {
            "x": direction * (1 - e * 2),
            "y": 0,
            "scale": 0.5 + e * 0.4
        }

    # SEGMENT 4 — WHEEL
    def wheel(self, t, index, total):

        angle = (2 * math.pi * index / total) + (t * 2 * math.pi)

        return {
            "x": math.cos(angle),
            "y": math.sin(angle),
            "scale": 0.4 + 0.2 * math.sin(angle)
        }