import os
from video_renderer import VideoRenderer


class AutoEditor:

    def __init__(self, photo_folder, music_file, output_file):

        self.photo_folder = photo_folder
        self.music_file = music_file
        self.output_file = output_file

        self.renderer = VideoRenderer(output_file)

    def _load_images(self):

        return sorted([
            os.path.join(self.photo_folder, f)
            for f in os.listdir(self.photo_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])

    def run(self):

        print("Loading images...")

        frames = self._load_images()

        if not frames:
            raise Exception("No images found")

        print("Rendering video...")

        self.renderer.render(
            frames=frames,
            music_path=self.music_file
        )

        print("DONE")