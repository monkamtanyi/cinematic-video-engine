import os
import math
import numpy as np
import gc
import subprocess

from engine.core.frame_engine import FrameEngine


class VideoRenderer:
    """
    Stable production renderer (NO blank frames, NO silent failures)
    """

    def __init__(self):
        self.frame = FrameEngine()
        self.W = 360
        self.H = 640

    # ----------------------------
    # LOAD IMAGE (STRICT)
    # ----------------------------
    def _load(self, path):
        img = self.frame.load(path)
        if img is None:
            raise RuntimeError(f"Failed to load image: {path}")
        return img

    # ----------------------------
    # BLIT (HARDENED - NO SILENT FAILS)
    # ----------------------------
    def _blit(self, canvas, img, x, y, zoom):
        zoom = zoom * 0.30
        import cv2

        h, w = img.shape[:2]

        nw = max(2, int(w * zoom))
        nh = max(2, int(h * zoom))

        resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)

        x = int(x - nw * 0.5)
        y = int(y - nh * 0.5)

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(self.W, x + nw)
        y2 = min(self.H, y + nh)

        if x1 >= x2 or y1 >= y2:
            return canvas

        roi_w = x2 - x1
        roi_h = y2 - y1

        canvas[y1:y2, x1:x2] = resized[:roi_h, :roi_w]

        return canvas

    # ----------------------------
    # MOTION
    # ----------------------------
    def _hero(self, t):

        # Segment 1 speed reduced to 75%
        t = min(t * 0.70, 1.0)

        if t < 0.4:
            p = t / 0.4
            return (
                self.W / 2,
                self.H + 80 - p * 350,
                0.22
            )

        if t < 0.50:
            return (
                self.W / 2,
                self.H / 2,
                0.24
            )

        if t < 0.75:
            return (
                self.W / 2,
                self.H / 2,
                0.23
            )

        p = (t - 0.75) / 0.25

        return (
            self.W / 2,
            self.H / 2 - p * 250,
            0.22
        )

    # ----------------------------
    # MAIN RENDER (FIXED FRAME PIPELINE)
    # ----------------------------
    def render(
        self,
        clips,
        music_path=None,
        output_file="output/out.mp4",
        progress_callback=None,
        segment_duration=None,
        **kwargs
    ):

        if not clips:
            raise ValueError("No input clips")

        print("[RENDER] loading images...")

        images = [self._load(c) for c in clips]

        # =========================================================
        # ✅ FIX: TRUE 25% SEGMENT TIMELINE
        # =========================================================
        fps = 15

        total_duration = 32  # 4 cinematic segments × 8s each
        seg_duration = total_duration / 4

        t1 = seg_duration
        t2 = t1 + seg_duration
        t3 = t2 + seg_duration
        t4 = t3 + seg_duration

        total_frames = int(total_duration * fps)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        output_file = os.path.abspath(output_file)

        # ----------------------------
        # FFmpeg PIPE (SAFE)
        # ----------------------------
        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel", "error",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{self.W}x{self.H}",
            "-r", str(fps),
            "-i", "-",
        ]

        if music_path:
            music_path = os.path.abspath(music_path)

        if music_path and os.path.exists(music_path):
            print(f"ADDING AUDIO TRACK: {music_path}")
            cmd += ["-i", music_path]
        else:
            print("NO AUDIO FILE FOUND")

        cmd += [
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "veryfast",
            "-movflags", "+faststart",
            "-b:v", "2500k",
        ]

        if music_path and os.path.exists(music_path):
            cmd += [
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-af",
                "volume=1.0",
                "-shortest"
            ]
        else:
            cmd += ["-an"]

        cmd += [output_file]

        print("FFMPEG COMMAND:")
        print(" ".join(cmd))

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            bufsize=0
        )

        def report(p, m):
            if progress_callback:
                try:
                    progress_callback(p, m)
                except:
                    pass

        report(0.01, "render started")

        images_local = images

        # ----------------------------
        # MAIN LOOP
        # ----------------------------
        for i in range(total_frames):

            if process.poll() is not None:
                err = process.stderr.read().decode("utf-8", errors="ignore")
                raise RuntimeError(err)

            # normalized time
            t = (i / total_frames) * total_duration

            canvas = np.zeros((self.H, self.W, 3), dtype=np.uint8)

            # segment index + local progress
            seg = int(t // seg_duration)
            p = ((t % seg_duration) / seg_duration) * 0.65

            # ----------------------------
            # SEGMENT 1
            # ----------------------------
            if seg == 0:
                per = seg_duration / len(images_local)
                for idx, img in enumerate(images_local):
                    s = idx * per
                    if s <= t < s + per:
                        lt = (t - s) / per
                        x, y, z = self._hero(lt)
                        canvas = self._blit(canvas, img, x, y, z)

            # ----------------------------
            # SEGMENT 2
            # FILMSTRIP TABLE-SCROLL CONVEYOR
            #
            # Requirements:
            # - one image follows another
            # - no overlap
            # - center pause
            # - zoom out
            # - zoom in
            # - continuous scrolling
            # ----------------------------
            elif seg == 1:

                spacing = 220
                card_y = self.H / 2

                conveyor_width = len(images_local) * spacing

                for idx, img in enumerate(images_local):

                    start_x = self.W + 400 + (idx * spacing)

                    travel = (p * 0.20) * (conveyor_width + self.W)

                    x = start_x - travel

                    distance = abs(x - (self.W / 2))

                    # approaching center
                    if distance > 500:
                        zoom = 0.18

                    # center pause + zoom out
                    elif distance > 120:
                        zoom = 0.20

                    # center focus zoom in
                    else:
                        zoom = 0.24

                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        card_y,
                        zoom
                    )

            # ----------------------------
            # SEGMENT 3
            # MILITARY CORRIDOR
            # ----------------------------
            elif seg == 2:

                left_x = self.W * 0.33
                right_x = self.W * 0.67

                row_spacing = 110
                start_y = 220

                for idx, img in enumerate(images_local):

                    row = idx // 2
                    left = (idx % 2 == 0)

                    x0 = left_x if left else right_x
                    y0 = start_y + row * row_spacing

                    if p < 0.65:

                        q = p / 0.50

                        x = x0
                        y = y0 + q * 180

                        zoom = 0.14 + (0.12 * q)

                    else:

                        q = (p - 0.50) / 0.50

                        if left:
                            x = x0 - q * 340
                        else:
                            x = x0 + q * 340

                        y = y0 + 180

                        zoom = 0.26

                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )

            # ----------------------------
            # SEGMENT 4
            # ----------------------------
            else:

                p = min(p, 1.0)

                if p < 0.33:

                    q = p / 0.33
                    rotation = q * 4.0 * math.pi
                    radius = 60

                    for idx, img in enumerate(images_local):

                        angle = (2.0 * math.pi * idx / len(images_local)) + rotation

                        x = self.W / 2 + radius * math.cos(angle)
                        y = self.H / 2 + radius * math.sin(angle)

                        canvas = self._blit(
                            canvas,
                            img,
                            x,
                            y,
                            0.22
                        )

                elif p < 0.66:

                    q = (p - 0.33) / 0.33

                    outer_radius = 60 - (60 * q)
                    inner_radius = outer_radius * 0.45

                    for idx, img in enumerate(images_local):

                        angle = 2.0 * math.pi * idx / len(images_local)

                        if idx % 2 == 0:
                            radius = outer_radius
                        else:
                            radius = inner_radius

                        x = self.W / 2 + radius * math.cos(angle)
                        y = self.H / 2 + radius * math.sin(angle)

                        canvas = self._blit(
                            canvas,
                            img,
                            x,
                            y,
                            0.22
                        )

                else:

                    q = (p - 0.66) / 0.34
                    radius = 40 * (1.0 - (q * 0.5))

                    for idx, img in enumerate(images_local):

                        angle = 2.0 * math.pi * idx / len(images_local)

                        x = self.W / 2 + radius * math.cos(angle)
                        y = self.H / 2 + radius * math.sin(angle)

                        canvas = self._blit(
                            canvas,
                            img,
                            x,
                            y,
                            0.22
                        )

            # ----------------------------
            # PIPE WRITE
            # ----------------------------
            try:
                process.stdin.write(canvas.tobytes())

            except BrokenPipeError:

                process.stdin.close()

                err = process.stderr.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                print("\n========== FFMPEG ERROR ==========")
                print(err)
                print("==================================")

                raise RuntimeError(err)

            if i % 10 == 0:
                report(i / total_frames, f"{i}/{total_frames}")

        process.stdin.close()
        process.wait()

        gc.collect()

        report(1.0, "done")

        return output_file







