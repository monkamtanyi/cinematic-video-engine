from PIL import Image
import os
import math


class FrameGenerator:
    """
    TravelVideoStudio
    Version 4.2

    High-quality frame generator with oversampling and
    cinematic ease-in/ease-out zoom.
    """

    # Final output size
    WIDTH = 1080
    HEIGHT = 1920

    # Render internally at higher resolution
    WORK_WIDTH = 1620
    WORK_HEIGHT = 2880

    FPS = 30

    def __init__(self, temp_folder="output/temp_frames"):
        self.temp_folder = temp_folder
        os.makedirs(temp_folder, exist_ok=True)

    # --------------------------------------------------
    # Easing
    # --------------------------------------------------

    def ease_in_out(self, t):
        """
        Smooth cinematic easing.
        """
        return t * t * (3 - 2 * t)

    # --------------------------------------------------
    # Resize image so it completely fills the canvas
    # --------------------------------------------------

    def prepare_image(self, image):

        scale = max(
            self.WORK_WIDTH / image.width,
            self.WORK_HEIGHT / image.height
        )

        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        return image.resize(
            (new_width, new_height),
            Image.LANCZOS
        )

    # --------------------------------------------------
    # Generate frames
    # --------------------------------------------------

    def generate_frames(
        self,
        image_path,
        motion="zoom_in",
        duration=3,
        intensity=1.0
    ):

        total_frames = duration * self.FPS

        image = Image.open(image_path).convert("RGB")

        image = self.prepare_image(image)

        frames_folder = os.path.join(
            self.temp_folder,
            os.path.splitext(
                os.path.basename(image_path)
            )[0]
        )

        os.makedirs(frames_folder, exist_ok=True)

        for frame in range(total_frames):

            progress = frame / (total_frames - 1)

            progress = self.ease_in_out(progress)

            # -----------------------------
            # Zoom
            # -----------------------------

            if motion == "zoom_in":

                zoom = 1 + (0.25 * intensity * progress)

            elif motion == "zoom_out":

                zoom = 1.25 - (0.25 * intensity * progress)

            else:

                zoom = 1.0

            crop_width = int(image.width / zoom)
            crop_height = int(image.height / zoom)

            left = (image.width - crop_width) // 2
            top = (image.height - crop_height) // 2

            cropped = image.crop(
                (
                    left,
                    top,
                    left + crop_width,
                    top + crop_height
                )
            )

            # Resize from oversampled image down to final output
            final = cropped.resize(
                (self.WIDTH, self.HEIGHT),
                Image.LANCZOS
            )

            filename = os.path.join(
                frames_folder,
                f"frame_{frame:04d}.jpg"
            )

            final.save(
                filename,
                quality=98,
                optimize=True
            )

        return frames_folder