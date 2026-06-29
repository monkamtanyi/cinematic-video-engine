from engine.motion_engine import MotionEngine
import os

class TimelineBuilder:
    def __init__(self):
        self.motion_engine = MotionEngine()

    def load_images(self, folder):
        images = []
        for file in sorted(os.listdir(folder)):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                images.append(os.path.join(folder, file))
        return images

    def build_timeline(self, image_folder):
        images = self.load_images(image_folder)

        timeline = self.motion_engine.assign_motions(images)

        print(f"🎬 Timeline created with {len(timeline)} scenes")

        for i, item in enumerate(timeline):
            print(f"{i+1}. {item['image']} -> {item['motion']}")

        return timeline