import random


class SmartEngine:

    def __init__(self):
        # 🎬 Scene-based directing rules (THIS is the upgrade)
        self.scene_rules = {
            "beach": {
                "motions": ["slow_zoom_out", "drift", "pan_right"],
                "intensity": 0.9,
                "style": "emotional"
            },
            "city": {
                "motions": ["pan_left", "pan_right", "zoom_in"],
                "intensity": 1.2,
                "style": "cinematic"
            },
            "mountain": {
                "motions": ["slow_zoom_out", "drone_rise"],
                "intensity": 0.8,
                "style": "cinematic"
            },
            "sunset": {
                "motions": ["slow_zoom_in", "fade_focus"],
                "intensity": 0.7,
                "style": "emotional"
            },
            "night": {
                "motions": ["zoom_in", "slow_pan_left"],
                "intensity": 1.3,
                "style": "dramatic"
            },
            "generic": {
                "motions": ["zoom_in", "zoom_out"],
                "intensity": 1.0,
                "style": "cinematic"
            }
        }

    # -----------------------------
    # MAIN DIRECTOR API (v2)
    # -----------------------------
    def direct(self, frames, beats, scene_labels):

        plan = []

        for i, frame in enumerate(frames):

            scene = scene_labels[i] if i < len(scene_labels) else "generic"

            rule = self.scene_rules.get(scene, self.scene_rules["generic"])

            motion = self._choose_motion(rule)

            intensity = self._adjust_intensity(rule, beats, i)

            plan.append({
                "frame_index": i,
                "scene": scene,
                "motion": motion,
                "intensity": intensity,
                "style": rule["style"]
            })

        return plan

    # -----------------------------
    # MOTION SELECTION
    # -----------------------------
    def _choose_motion(self, rule):
        return {
            "type": random.choice(rule["motions"]),
            "strength": rule["intensity"]
        }

    # -----------------------------
    # INTENSITY CONTROL (music-aware)
    # -----------------------------
    def _adjust_intensity(self, rule, beats, i):

        if not beats or len(beats) < 2:
            return rule["intensity"]

        # simple rhythm mapping
        beat_factor = 1.0

        if i % 2 == 0:
            beat_factor = 1.1
        else:
            beat_factor = 0.9

        return round(rule["intensity"] * beat_factor, 2)