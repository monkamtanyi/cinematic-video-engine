import os
from engine.core.video_renderer import VideoRenderer


class AutoEditor:

    def __init__(self, photo_folder, music_file, output_file):

        self.photo_folder = photo_folder
        self.music_file = music_file
        self.output_file = output_file

        self.renderer = VideoRenderer(output_file)

    def _load_images(self):

        images = sorted([
            os.path.join(self.photo_folder, f)
            for f in os.listdir(self.photo_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])

        print(f"📸 Loaded {len(images)} images")

        return images

    def run(self):

        frames = self._load_images()

        print("🎬 Rendering v4.2 pipeline...")

        self.renderer.render(
            frames=frames,
            music_path=self.music_file,
            segment_duration=3
        )