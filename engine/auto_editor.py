import os
from engine.core.video_renderer import VideoRenderer


class AutoEditor:

    def __init__(self, photo_folder, music_file, output_file):
        self.photo_folder = photo_folder
        self.music_file = music_file
        self.output_file = output_file

        self.renderer = VideoRenderer()

    def run(self):

        print("🎬 Rendering video...")

        clips = self._load_frames()

        video = self.renderer.render(
            clips=clips,
            music_path=self.music_file,
            segment_duration=3
        )

        video.write_videofile(
            self.output_file,
            fps=30,
            codec="libx264",
            audio_codec="aac"
        )

        print(f"✅ Saved: {self.output_file}")

    def _load_frames(self):
        frames = []

        for f in sorted(os.listdir(self.photo_folder)):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                frames.append(os.path.join(self.photo_folder, f))

        return frames