import os
import cv2
import numpy as np
from motion_engine import MotionEngine

class FrameEngine:


 def __init__(self, output_dir="output/temp_frames"):

    self.output_dir = output_dir
    self.motion_engine = MotionEngine()

    os.makedirs(output_dir, exist_ok=True)

 def load_image(self, path):

    img = cv2.imread(path)

    if img is None:
        raise Exception(f"Cannot load image: {path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

 def save_frame(self, img, path):

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img)

 def crop_zoom(self, img, zoom):

    h, w = img.shape[:2]

    zoom = max(0.3, zoom)

    crop_w = int(w / zoom)
    crop_h = int(h / zoom)

    x1 = max(0, (w - crop_w) // 2)
    y1 = max(0, (h - crop_h) // 2)

    x2 = x1 + crop_w
    y2 = y1 + crop_h

    cropped = img[y1:y2, x1:x2]

    return cv2.resize(cropped, (w, h))

 def generate_frames(
    self,
    image_path,
    motion_func,
    duration=4,
    fps=30
):

    img = self.load_image(image_path)

    h, w = img.shape[:2]

    total_frames = duration * fps

    scene_name = os.path.splitext(
        os.path.basename(image_path)
    )[0]

    frames_dir = os.path.join(
        self.output_dir,
        scene_name
    )

    os.makedirs(frames_dir, exist_ok=True)

    canvas_w = w * 3
    canvas_h = h * 3

    for i in range(total_frames):

        t = i / fps

        x, y, zoom = motion_func(t)

        frame_img = self.crop_zoom(img, zoom)

        canvas = np.zeros(
            (canvas_h, canvas_w, 3),
            dtype=np.uint8
        )

        paste_x = int(canvas_w/2 - w/2 + x - self.motion_engine.w/2)
        paste_y = int(canvas_h/2 - h/2 + y - self.motion_engine.h/2)

        paste_x = max(
            0,
            min(canvas_w - w, paste_x)
        )

        paste_y = max(
            0,
            min(canvas_h - h, paste_y)
        )

        canvas[
            paste_y:paste_y+h,
            paste_x:paste_x+w
        ] = frame_img

        center_x = canvas_w // 2
        center_y = canvas_h // 2

        output = canvas[
            center_y-h//2:center_y+h//2,
            center_x-w//2:center_x+w//2
        ]

        frame_file = os.path.join(
            frames_dir,
            f"frame_{i:04d}.jpg"
        )

        self.save_frame(
            output,
            frame_file
        )

    print(f"✅ Frames generated -> {frames_dir}")

    return frames_dir

