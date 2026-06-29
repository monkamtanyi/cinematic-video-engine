class TrailerEngine:

    def __init__(self):
        pass

    # -----------------------------
    # BUILD TRAILER STRUCTURE
    # -----------------------------
    def build_trailer(self, frames, plan):

        total = len(plan)

        for i, item in enumerate(plan):

            progress = i / total if total > 0 else 0

            if progress < 0.1:
                phase = "hook"
            elif progress < 0.5:
                phase = "build"
            elif progress < 0.8:
                phase = "climax"
            else:
                phase = "ending"

            item["trailer_phase"] = phase

            motion = item["motion"]

            # 🎬 trailer intensity shaping
            if phase == "hook":
                item["intensity"] *= 1.5
                motion["strength"] *= 1.4

            elif phase == "build":
                item["intensity"] *= 1.0

            elif phase == "climax":
                item["intensity"] *= 1.8
                motion["strength"] *= 2.0

            elif phase == "ending":
                item["intensity"] *= 0.7
                motion["strength"] *= 0.6

            item["motion"] = motion

        return plan