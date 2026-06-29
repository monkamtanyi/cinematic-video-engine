import os
import numpy as np
from PIL import Image

from moviepy.editor import VideoClip, AudioFileClip

from engine.core.motion_engine import MotionEngine
from engine.core.segment_engine import SegmentEngine


class VideoRenderer:

    def __init__(self, output_path, fps=24):

        self.output_path = output_path
        self.fps = fps

        self.motion = MotionEngine()
        self.segmenter = SegmentEngine()

        self.size = (1920, 1080)

    def _load(self, frames):

        return [
            Image.open(f).convert("RGB").resize(self.size)
            for f in frames
        ]

    def render(self, frames, music_path=None, segment_duration=3):

        images = self._load(frames)
        total = len(images)

        duration = total * segment_duration

        def make_frame(t):

            idx = min(int(t / segment_duration), total - 1)
            local_t = (t % segment_duration) / segment_duration

            seg = self.segmenter.resolve(idx, total)

            img = np.array(images[idx])

            if seg == "field_motion":
                x, y, z = self.motion.field_motion(local_t, idx)

            elif seg == "conveyor":
                x, y, z = self.motion.conveyor(local_t, idx)

            elif seg == "split_depth":
                x, y, z = self.motion.split_depth(local_t, idx)

            else:
                x, y, z = self.motion.radial_motion(local_t, idx)

            pil = Image.fromarray(img)

            w = max(1, int(1920 * z))
            h = max(1, int(1080 * z))

            pil = pil.resize((w, h))

            canvas = Image.new("RGB", self.size)

            x_pos = int(x - w / 2)
            y_pos = int(y - h / 2)

            canvas.paste(pil, (x_pos, y_pos))

            return np.array(canvas)

        clip = VideoClip(make_frame, duration=duration)

        if music_path and os.path.exists(music_path):
            audio = AudioFileClip(music_path)
            audio = audio.audio_loop(duration=clip.duration)
            clip = clip.set_audio(audio)

        clip.write_videofile(
            self.output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            threads=2
        )