import math


class MotionEngine:

    def __init__(self):

        self.patterns = [
            "left_to_right",
            "right_to_left",
            "top_to_bottom",
            "bottom_to_top",
            "diag_down",
            "diag_up",
            "circle",
            "figure8",
            "spiral"
        ]

    def motion_for_clip(self, index):

        return self.patterns[index % len(self.patterns)]

    def path(self, pattern, p):

        p = max(0.0, min(1.0, p))

        # center pause
        if 0.40 < p < 0.60:
            p = 0.50

        if pattern == "left_to_right":
            return (-350 + p * 700, 0)

        if pattern == "right_to_left":
            return (350 - p * 700, 0)

        if pattern == "top_to_bottom":
            return (0, -220 + p * 440)

        if pattern == "bottom_to_top":
            return (0, 220 - p * 440)

        if pattern == "diag_down":
            return (
                -300 + p * 600,
                -180 + p * 360
            )

        if pattern == "diag_up":
            return (
                -300 + p * 600,
                180 - p * 360
            )

        if pattern == "circle":

            a = p * 2 * math.pi

            return (
                math.cos(a) * 180,
                math.sin(a) * 120
            )

        if pattern == "figure8":

            a = p * 2 * math.pi

            return (
                math.sin(a) * 200,
                math.sin(a * 2) * 100
            )

        if pattern == "spiral":

            a = p * 5 * math.pi
            r = 250 * (1 - p)

            return (
                math.cos(a) * r,
                math.sin(a) * r
            )

        return (0, 0)

    def generate(self, frames, beats=None, emotions=None):

        motions = []

        for i, frame in enumerate(frames):

            motions.append({
                "frame": frame,
                "pattern": self.motion_for_clip(i)
            })

        return motions