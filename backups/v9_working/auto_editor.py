import os

from motion_engine import MotionEngine
from video_renderer import VideoRenderer
from emotion_engine import EmotionEngine


class AutoEditor:

    def __init__(self, photo_folder, music_file, output_file):

        self.photo_folder = photo_folder
        self.music_file = music_file
        self.output_file = output_file

        self.motion_engine = MotionEngine()
        self.emotion_engine = EmotionEngine()

        self.renderer = VideoRenderer(output_path=output_file)

    # -----------------------------
    # 📸 LOAD FRAMES
    # -----------------------------
    def _load_frames(self):

        frames = []

        for f in sorted(os.listdir(self.photo_folder)):

            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                frames.append(os.path.join(self.photo_folder, f))

        return frames

    # -----------------------------
    # 🎵 SAFE MUSIC LOADER (OPTIONAL)
    # -----------------------------
    def _load_music(self):

        if not self.music_file:
            return None

        if not os.path.exists(self.music_file):
            print(f"⚠️ Music file not found: {self.music_file}")
            return None

        return self.music_file

    # -----------------------------
    # 🧠 FULL RENDER PIPELINE
    # -----------------------------
    def render(self):

        print("🚀 Starting Fully AI Auto Editor...")

        # 📸 LOAD MEDIA
        print("📸 Loading media...")
        frames = self._load_frames()

        if not frames:
            raise ValueError("No images found in photo folder")

        # 🧠 EMOTION ANALYSIS
        print("🧠 Analyzing scenes...")
        emotions = self.emotion_engine.analyze(frames)

        # 🎵 MUSIC
        print("🎵 Processing music...")
        music = self._load_music()

        beats = []

        # NOTE:
        # beats are generated inside renderer or motion system fallback
        # we keep safe empty list here to avoid crashes
        beats = []

        # 🎬 MOTION ENGINE (emotion-aware)
        print("🎬 Directing film...")

        motions = self.motion_engine.generate(
            frames=frames,
            beats=beats,
            emotions=emotions
        )

        # 📖 STORY STEP (placeholder for future expansion)
        print("📖 Building story arc...")

        # 🎞 RENDER VIDEO
        print("🎥 Rendering video...")

        self.renderer.render(
            frames=frames,
            beats=beats,
            motions=motions,
            music_path=music
        )

        print(f"🎉 DONE: {self.output_file}")