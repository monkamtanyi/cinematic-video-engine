import cv2
import numpy as np


class FrameEngine:

    def load(self, path):
        img = cv2.imread(path)
        if img is None:
            raise Exception(f"Cannot load image: {path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ==================================================
    # ORIGINAL (kept for backward compatibility)
    # ==================================================
    def apply(self, img, x, y, zoom):

        H, W = 1920, 1080

        h, w = img.shape[:2]

        zoom = max(0.3, min(2.0, zoom))

        crop_w = max(2, int(w / zoom))
        crop_h = max(2, int(h / zoom))

        cx, cy = w // 2, h // 2

        x1 = max(0, min(w - crop_w, cx - crop_w // 2))
        y1 = max(0, min(h - crop_h, cy - crop_h // 2))

        cropped = img[y1:y1 + crop_h, x1:x1 + crop_w]

        resized = cv2.resize(cropped, (w, h))

        canvas = np.zeros((H, W, 3), dtype=np.uint8)

        x = int(max(0, min(W - w, x - w // 2)))
        y = int(max(0, min(H - h, y - h // 2)))

        x2 = min(W, x + w)
        y2 = min(H, y + h)

        canvas[y:y2, x:x2] = resized[0:(y2 - y), 0:(x2 - x)]

        return canvas

    # ==================================================
    # REQUIRED BY RENDERER (FIXED & SAFE)
    # ==================================================
    def apply_to_canvas(self, canvas, img, x, y, zoom):

        H, W = canvas.shape[:2]

        h, w = img.shape[:2]

        zoom = max(0.3, min(2.0, zoom))

        new_w = int(w * zoom)
        new_h = int(h * zoom)

        if new_w < 2 or new_h < 2:
            return canvas

        resized = cv2.resize(img, (new_w, new_h))

        x1 = int(x - new_w // 2)
        y1 = int(y - new_h // 2)

        x2 = x1 + new_w
        y2 = y1 + new_h

        if x2 <= 0 or y2 <= 0 or x1 >= W or y1 >= H:
            return canvas

        x1c = max(0, x1)
        y1c = max(0, y1)
        x2c = min(W, x2)
        y2c = min(H, y2)

        rx1 = x1c - x1
        ry1 = y1c - y1
        rx2 = rx1 + (x2c - x1c)
        ry2 = ry1 + (y2c - y1c)

        canvas[y1c:y2c, x1c:x2c] = resized[ry1:ry2, rx1:rx2]

        return canvas

    # ==================================================
    # SPEED OPTIMIZATION (NEW V6 FEATURE)
    # ==================================================
    def preload(self, images, scale=0.22):

        cached = []

        for img in images:

            h, w = img.shape[:2]

            new_w = int(w * scale)
            new_h = int(h * scale)

            resized = cv2.resize(img, (new_w, new_h))

            cached.append(resized)

        return cached