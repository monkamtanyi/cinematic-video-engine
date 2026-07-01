import os
import math
import numpy as np

from moviepy.editor import VideoClip, AudioFileClip

from engine.core.frame_engine import FrameEngine


class VideoRenderer:

    def __init__(self):

        self.frame = FrameEngine()

        self.W = 1080
        self.H = 1920

    # --------------------------------------------------
    # SAFE IMAGE LOADER
    # --------------------------------------------------
    def _load(self, path):

        img = self.frame.load(path)

        # fallback if FrameEngine returns None
        if img is None:
            raise Exception(f"Failed to load image: {path}")

        return img

    # --------------------------------------------------
    # SAFE CANVAS
    # --------------------------------------------------
    def _canvas(self):

        return np.zeros((self.H, self.W, 3), dtype=np.uint8)

    # --------------------------------------------------
    # SAFE BLIT (manual image draw fallback)
    # --------------------------------------------------
    def _blit(self, canvas, img, x, y, zoom):

        """
        If FrameEngine has apply_to_canvas → use it.
        Otherwise fallback silently (no crash).
        """

        if hasattr(self.frame, "apply_to_canvas"):
            return self.frame.apply_to_canvas(canvas, img, x, y, zoom)

        # ---------------- fallback renderer ----------------
        try:
            import cv2

            if isinstance(img, np.ndarray):

                h, w = img.shape[:2]

                new_w = int(w * zoom)
                new_h = int(h * zoom)

                if new_w <= 0 or new_h <= 0:
                    return canvas

                resized = cv2.resize(img, (new_w, new_h))

                x = int(x - new_w / 2)
                y = int(y - new_h / 2)

                if (
                    x >= self.W
                    or y >= self.H
                    or x + new_w <= 0
                    or y + new_h <= 0
                ):
                    return canvas

                x1 = max(0, x)
                y1 = max(0, y)

                x2 = min(self.W, x + new_w)
                y2 = min(self.H, y + new_h)

                canvas[y1:y2, x1:x2] = resized[
                    0:(y2 - y1),
                    0:(x2 - x1)
                ]

        except Exception:
            pass

        return canvas

    # --------------------------------------------------
    # MAIN RENDER
    # --------------------------------------------------
    def render(
        self,
        clips,
        music_path=None,
        output_file="output/final.mp4"
    ):

        total = len(clips)

        images = [self._load(c) for c in clips]

        HERO_DURATION = 12
        CONVEYOR_DURATION = 12
        SPLIT_DURATION = 12
        CIRCLE_DURATION = 12

        HERO_END = HERO_DURATION
        CONVEYOR_END = HERO_END + CONVEYOR_DURATION
        SPLIT_END = CONVEYOR_END + SPLIT_DURATION
        CIRCLE_END = SPLIT_END + CIRCLE_DURATION

        total_duration = CIRCLE_END

        def make_frame(t):

            canvas = self._canvas()

            # ==================================================
            # SEGMENT 1 - SEQUENTIAL HERO FLOW
            # ==================================================
            if t < HERO_END:

                per_img = HERO_DURATION / total

                for i, img in enumerate(images):

                    start = i * per_img
                    end = start + per_img

                    if not (start <= t < end):
                        continue

                    local_t = (t - start) / per_img

                    if local_t < 0.40:
                        p = local_t / 0.40

                        x = self.W / 2
                        y = self.H + 300 - p * (self.H / 2 + 300)
                        zoom = 0.22

                    elif local_t < 0.60:
                        x = self.W / 2
                        y = self.H / 2
                        zoom = 0.24

                    elif local_t < 0.80:
                        p = (local_t - 0.60) / 0.20
                        x = self.W / 2
                        y = self.H / 2
                        zoom = 0.24 - 0.05 * math.sin(p * math.pi)

                    else:
                        p = (local_t - 0.80) / 0.20
                        x = self.W / 2
                        y = (self.H / 2) - p * (self.H / 2 + 400)
                        zoom = 0.22

                    canvas = self._blit(canvas, img, x, y, zoom)

            # ==================================================
            # SEGMENT 2 - CONVEYOR
            # ==================================================
            elif t < CONVEYOR_END:

                p = (t - HERO_END) / CONVEYOR_DURATION
                spacing = 260

                for i, img in enumerate(images):

                    x = (
                        self.W + 500
                        - p * (self.W + spacing * total + 1200)
                        + i * spacing
                    )

                    y = 450 + (i % 3) * 420
                    zoom = 0.22

                    canvas = self._blit(canvas, img, x, y, zoom)

            # ==================================================
            # SEGMENT 3 - SPLIT
            # ==================================================
            elif t < SPLIT_END:

                p = (t - CONVEYOR_END) / SPLIT_DURATION

                for i, img in enumerate(images):

                    left = (i % 2 == 0)
                    lane = -260 if left else 260
                    row = i // 2

                    if p < 0.60:

                        x = self.W / 2 + lane
                        y = self.H - row * 120 - p * 1200

                    else:

                        split = (p - 0.60) / 0.40

                        x = self.W / 2 + lane + lane * split * 2.5
                        y = 500 + row * 80

                    zoom = 0.20 + p * 0.15

                    canvas = self._blit(canvas, img, x, y, zoom)

            # ==================================================
            # SEGMENT 4 - WHEEL
            # ==================================================
            else:

                p = (t - SPLIT_END) / CIRCLE_DURATION
                radius = 850
                rot = p * 4 * math.pi

                for i, img in enumerate(images):

                    a = (2 * math.pi * i / total) + rot

                    x = self.W / 2 + radius * math.cos(a)
                    y = self.H / 2 + radius * math.sin(a)

                    zoom = 0.18

                    canvas = self._blit(canvas, img, x, y, zoom)

            return canvas

        video = VideoClip(make_frame, duration=total_duration)

        if music_path and os.path.exists(music_path):

            audio = AudioFileClip(music_path)

            if audio.duration > total_duration:
                audio = audio.subclip(0, total_duration)

            video = video.set_audio(audio)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        video.write_videofile(
            output_file,
            fps=30,
            codec="libx264",
            bitrate="6000k",
            audio_codec="aac"
        )

        return output_file