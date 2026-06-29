class StoryArcEngine:

    def __init__(self):
        pass

    # -----------------------------
    # MAIN API
    # -----------------------------
    def build_arc(self, frames, plan):

        total = len(frames)

        arc_plan = []

        for i, item in enumerate(plan):

            progress = i / total

            phase = self._get_phase(progress)

            adjusted = self._apply_arc_rules(item, phase)

            arc_plan.append(adjusted)

        return arc_plan

    # -----------------------------
    # DETERMINE STORY PHASE
    # -----------------------------
    def _get_phase(self, progress):

        if progress < 0.2:
            return "intro"

        elif progress < 0.5:
            return "build"

        elif progress < 0.8:
            return "climax"

        else:
            return "outro"

    # -----------------------------
    # APPLY STORY RULES
    # -----------------------------
    def _apply_arc_rules(self, item, phase):

        motion = item["motion"]
        intensity = item["intensity"]

        if phase == "intro":
            intensity *= 0.8
            motion["strength"] *= 0.8

        elif phase == "build":
            intensity *= 1.0

        elif phase == "climax":
            intensity *= 1.4
            motion["strength"] *= 1.5

        elif phase == "outro":
            intensity *= 0.7
            motion["strength"] *= 0.6

        item["intensity"] = round(intensity, 2)
        item["motion"] = motion
        item["story_phase"] = phase

        return item