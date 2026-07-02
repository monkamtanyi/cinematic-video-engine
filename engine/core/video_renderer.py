import os
import math
import numpy as np

from moviepy.editor import VideoClip, AudioFileClip

from engine.core.frame_engine import FrameEngine
from engine.core.motion_engine import MotionEngine


class VideoRenderer:

    def __init__(self):

        self.frame = FrameEngine()
        self.motion = MotionEngine()

        self.W = 1080
        self.H = 1920

    def render(self, clips, music_path=None, output_file="output/final.mp4"):

        total = len(clips)
        images = [self.frame.load(c) for c in clips]

        # ==================================================
        # BASE SEGMENT STRUCTURE
        # ==================================================
        HERO_DURATION = 12
        CONVEYOR_DURATION = 12
        SPLIT_DURATION = 12
        CIRCLE_DURATION = 12

        base_total = HERO_DURATION + CONVEYOR_DURATION + SPLIT_DURATION + CIRCLE_DURATION
        HERO_DURATION = base_total * 0.5

        HERO_END = HERO_DURATION
        CONVEYOR_END = HERO_END + CONVEYOR_DURATION
        SPLIT_END = CONVEYOR_END + SPLIT_DURATION
        CIRCLE_END = SPLIT_END + CIRCLE_DURATION

        total_duration = CIRCLE_END

        def make_frame(t):

            canvas = np.zeros((self.H, self.W, 3), dtype=np.uint8)

            # ❌ REMOVED: global slowdown (this was breaking segment timing)
            # t = t * 0.5

            # =========================
            # SEGMENT 1
            # =========================
            if t < HERO_END:

                image_time = (HERO_END * 1.75) / max(1, total)
                current_index = int(t / image_time)

                if current_index >= total:
                    current_index = total - 1

                img = images[current_index]

                local_t = (t - current_index * image_time) / image_time
                local_t = max(0.0, min(1.0, local_t))

                p = local_t * local_t * (3 - 2 * local_t)

                x = self.W / 2

                if p < 0.35:
                    phase = p / 0.35
                    y = self.H + 300 - phase * (self.H + 300 - self.H / 2)
                    zoom = 0.18

                elif p < 0.65:
                    y = self.H / 2
                    zoom = 0.18

                elif p < 0.80:
                    phase = (p - 0.65) / 0.15
                    y = self.H / 2
                    zoom = 0.18 - (phase * 0.03)

                elif p < 0.92:
                    phase = (p - 0.80) / 0.12
                    y = self.H / 2
                    zoom = 0.15 + (phase * 0.04)

                else:
                    phase = (p - 0.92) / 0.08
                    y = self.H / 2 - phase * (self.H + 300)
                    zoom = 0.19

                canvas = self.frame.apply_to_canvas(canvas, img, x, y, zoom)

            # =========================
            # SEGMENT 2
            # =========================
            elif t < CONVEYOR_END:

                p = (t - HERO_END) / CONVEYOR_DURATION

                spacing = 230
                travel = self.W + spacing * total + 900
                base_x = self.W + 450

                for i, img in enumerate(images):
                    x = base_x - (p * travel) + (i * spacing)
                    y = self.H / 2
                    zoom = 0.22
                    canvas = self.frame.apply_to_canvas(canvas, img, x, y, zoom)

            # =========================
            # SEGMENT 3
            # =========================
            elif t < SPLIT_END:

                raw_p = (t - CONVEYOR_END) / SPLIT_DURATION

                # kept subtle slow-motion only here (safe)
                p = raw_p * 0.75

                slot_time = 1.0 / max(1, total)
                idx = min(int(p / slot_time), total - 1)

                img = images[idx]

                local_p = (p - idx * slot_time) / slot_time
                local_p = max(0.0, min(1.0, local_p))

                e = local_p * local_p * (3 - 2 * local_p)

                depth = 1.0 + e * 2.5
                base_y = self.H / 2 + 300 * (1 - e)

                is_left = (idx % 2 == 0)
                spread = 80 + e * 500

                if is_left:
                    x = self.W / 2 - spread * depth
                    exit_x = -400
                else:
                    x = self.W / 2 + spread * depth
                    exit_x = self.W + 400

                if e > 0.75:
                    exit_p = (e - 0.75) / 0.25
                    x = x + (exit_x - x) * exit_p
                    base_y += exit_p * 50

                zoom = 0.20 + e * 0.35

                canvas = self.frame.apply_to_canvas(canvas, img, x, base_y, zoom)

            # =========================
            # SEGMENT 4
            # =========================
            else:

                p = (t - SPLIT_END) / CIRCLE_DURATION

                rot = p * 6 * math.pi
                radius = 900
                base_zoom = 0.09

                for i, img in enumerate(images):

                    angle = (2 * math.pi * i / max(1, total)) + rot

                    x = self.W / 2 + radius * math.cos(angle)
                    y = self.H / 2 + radius * math.sin(angle)

                    star_push = 1.0 + 0.25 * math.sin(5 * angle + p * 6)

                    x *= star_push
                    y *= star_push

                    canvas = self.frame.apply_to_canvas(canvas, img, x, y, base_zoom)

            return canvas

        # =========================
        # VIDEO + AUDIO (UNCHANGED WORKING FIX)
        # =========================
        video = VideoClip(make_frame, duration=total_duration)

        audio = None

        if music_path:
            music_path = os.path.abspath(music_path)

            if os.path.exists(music_path):
                audio = AudioFileClip(music_path)

                audio = audio.subclip(0, min(audio.duration, total_duration))

                video = video.set_audio(audio)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        video.write_videofile(
            output_file,
            fps=30,
            codec="libx264",
            audio=True,
            audio_codec="aac",
            bitrate="6000k",
            ffmpeg_params=[
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart"
            ]
        )

        if audio:
            audio.close()

        return output_file