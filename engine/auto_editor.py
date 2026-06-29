import os
from engine.core.video_renderer import VideoRenderer


class AutoEditor:

    def __init__(self, photo_folder, music_file, output_file):

        self.photo_folder = photo_folder
        self.music_file = music_file
        self.output_file = output_file

        self.renderer = VideoRenderer(output_file)

    def _load_images(self):

        if not os.path.exists(self.photo_folder):
            raise FileNotFoundError("Photo folder not found")

        images = sorted([
            os.path.join(self.photo_folder, f)
            for f in os.listdir(self.photo_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])

        if not images:
            raise ValueError("No images found in folder")

        return images

    def run(self):

        frames = self._load_images()

        self.renderer.render(
            frames=frames,
            music_path=self.music_file
        )