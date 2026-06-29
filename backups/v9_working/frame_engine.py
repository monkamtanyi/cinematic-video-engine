import os
import cv2
import numpy as np
from motion_engine import apply_easing


class FrameEngine:
    """
    Version 5: Frame-by-frame cinematic motion engine
    """

    def __init__(self, output_dir="output/temp_frames"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def load_image(self, path):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def save_frame(self, img, path):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)

    def generate_frames(self, image_path, motion, duration=3, fps=30):
        """
        Generate smooth cinematic motion frames
        """

        img = self.load_image(image_path)

        h, w, _ = img.shape

        total_frames = duration * fps

        frames_dir = os.path.join(
            self.output_dir,
            os.path.basename(image_path).split(".")[0]
        )

        os.makedirs(frames_dir, exist_ok=True)

        mtype = motion["type"]
        easing = motion["easing"]
        intensity = motion["intensity"]

        zoom_start = 1.0
        zoom_end = 1.0 + (intensity * 0.3)

        for i in range(total_frames):
            t = i / (total_frames - 1)
            t_eased = apply_easing(t, easing)

            zoom = zoom_start + (zoom_end - zoom_start) * t_eased

            # movement ranges
            shift_x = 0
            shift_y = 0

            if mtype == "pan_left":
                shift_x = -int(w * 0.3 * t_eased)
            elif mtype == "pan_right":
                shift_x = int(w * 0.3 * t_eased)
            elif mtype == "pan_up":
                shift_y = -int(h * 0.3 * t_eased)
            elif mtype == "pan_down":
                shift_y = int(h * 0.3 * t_eased)
            elif mtype == "diagonal_up_right":
                shift_x = int(w * 0.25 * t_eased)
                shift_y = -int(h * 0.25 * t_eased)
            elif mtype == "diagonal_down_left":
                shift_x = -int(w * 0.25 * t_eased)
                shift_y = int(h * 0.25 * t_eased)

            # zoom crop
            new_w = int(w / zoom)
            new_h = int(h / zoom)

            x1 = max(0, (w - new_w) // 2 + shift_x)
            y1 = max(0, (h - new_h) // 2 + shift_y)

            x2 = min(w, x1 + new_w)
            y2 = min(h, y1 + new_h)

            frame = img[y1:y2, x1:x2]
            frame = cv2.resize(frame, (w, h))

            frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
            self.save_frame(frame, frame_path)

        print(f"✅ Frames generated: {frames_dir}")
        return frames_dir