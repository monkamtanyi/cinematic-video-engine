import math
import random


class MotionEngine:
    """
    V2 Cinematic Motion Engine (deterministic + segment-based)
    Replaces old hero() system entirely.
    """

    def drift(self, t, duration, seed=0):
        random.seed(seed)

        # base velocity per image
        vx = random.uniform(-80, 80)
        vy = random.uniform(-50, 50)

        progress = min(max(t / duration, 0), 1)

        # smooth cinematic easing (ease in-out)
        ease = 3 * progress**2 - 2 * progress**3

        return vx * ease, vy * ease

    def conveyor(self, t, speed=120):
        """
        horizontal cinematic scroll (like film strip)
        """
        return -speed * t, 0

    def split(self, t, duration, side="left"):
        """
        dual-lane separation motion
        """
        progress = min(max(t / duration, 0), 1)
        direction = -1 if side == "left" else 1

        x = direction * (120 * progress)
        y = 20 * math.sin(progress * math.pi)

        return x, y

    def wheel(self, t, radius=250, speed=2):
        """
        circular carousel motion
        """
        angle = speed * t

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        return x, y