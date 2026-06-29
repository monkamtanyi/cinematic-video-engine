import os


class EmotionEngine:

    def __init__(self):

        self.rules = {
            "sunset": "warm",
            "beach": "travel",
            "mountain": "adventure",
            "city": "hype",
            "night": "cinematic",
            "lights": "cinematic",
            "people": "warm",
            "portrait": "warm",
            "sky": "calm",
            "road": "travel",
            "forest": "adventure",
            "water": "calm",
            "ocean": "travel",
            "lake": "calm",
            "bridge": "adventure",
            "downtown": "hype",
            "street": "hype"
        }

    # --------------------------------------------------
    # Detect emotion from filename
    # --------------------------------------------------
    def detect(self, frame_path):

        filename = os.path.basename(frame_path).lower()

        for keyword, emotion in self.rules.items():

            if keyword in filename:
                return emotion

        return "neutral"

    # --------------------------------------------------
    # Analyze all frames
    # --------------------------------------------------
    def analyze(self, frames):

        results = []

        for frame in frames:

            emotion = self.detect(frame)

            results.append(
                {
                    "frame": frame,
                    "emotion": emotion
                }
            )

        return results

    # --------------------------------------------------
    # Debug helper
    # --------------------------------------------------
    def print_summary(self, analysis):

        print("\n🧠 Emotion Analysis")

        for item in analysis:

            print(
                f"{os.path.basename(item['frame'])} "
                f"-> {item['emotion']}"
            )

        print("")