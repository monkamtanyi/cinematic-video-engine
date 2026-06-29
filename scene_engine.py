import os


class SceneEngine:

    def __init__(self):
        # simple keyword-based intelligence (v1 approach)
        self.labels = {
            "beach": ["beach", "sea", "ocean", "sand"],
            "city": ["city", "build", "street", "urban"],
            "mountain": ["mountain", "hill", "forest"],
            "sunset": ["sunset", "sunrise", "sky"],
            "night": ["night", "dark", "lights"]
        }

    # -----------------------------
    # MAIN API
    # -----------------------------
    def analyze(self, frames):
        scenes = []

        for frame in frames:

            label = self._classify(frame)

            scenes.append({
                "frame": frame,
                "scene": label
            })

        return scenes

    # -----------------------------
    # SIMPLE CLASSIFIER (V1)
    # -----------------------------
    def _classify(self, frame_path):

        name = os.path.basename(frame_path).lower()

        for label, keywords in self.labels.items():
            for kw in keywords:
                if kw in name:
                    return label

        # default fallback
        return "generic"