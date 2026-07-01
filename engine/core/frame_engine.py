import cv2
import numpy as np


class FrameEngine:

    def load(self, path):
        img = cv2.imread(path)
        if img is None:
            raise Exception(f"Cannot load image: {path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def apply(self, img, x, y, zoom):

        H, W = 1920, 1080

        h, w = img.shape[:2]

        zoom = max(0.3, min(2.0, zoom))

        # crop center
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