import os
import math
import numpy as np

from moviepy.editor import VideoClip, AudioFileClip

from engine.core.frame_engine import FrameEngine


class VideoRenderer:

    def __init__(self):

        self.frame = FrameEngine()

        # --------------------------------------------------
        # OPTION A:
        # Production default:
        #   1080 x 1920
        #
        # Local preview:
        #   VIDEO_WIDTH=540
        #   VIDEO_HEIGHT=960
        # --------------------------------------------------

        self.W = int(
            os.getenv(
                "VIDEO_WIDTH",
                960
            )
        )

        self.H = int(
            os.getenv(
                "VIDEO_HEIGHT",
                960
            )
        )


    # --------------------------------------------------
    # SAFE IMAGE LOADER
    # --------------------------------------------------

    def _load(self, path):

        img = self.frame.load(path)

        if img is None:
            raise Exception(
                f"Failed to load image: {path}"
            )

        return img


    # --------------------------------------------------
    # SAFE CANVAS
    # --------------------------------------------------

    def _canvas(self):

        return np.zeros(
            (
                self.H,
                self.W,
                3
            ),
            dtype=np.uint8
        )


    # --------------------------------------------------
    # SAFE BLIT
    # --------------------------------------------------

    def _blit(
        self,
        canvas,
        img,
        x,
        y,
        zoom
    ):

        """
        Uses FrameEngine canvas rendering
        when available.

        Falls back to OpenCV renderer.
        """

        if hasattr(
            self.frame,
            "apply_to_canvas"
        ):

            return self.frame.apply_to_canvas(
                canvas,
                img,
                x,
                y,
                zoom
            )


        try:

            import cv2


            if isinstance(
                img,
                np.ndarray
            ):

                h, w = img.shape[:2]


                new_w = int(
                    w * zoom*0.35
                )

                new_h = int(
                    h * zoom*0.35
                )


                if (
                    new_w <= 0
                    or new_h <= 0
                ):
                    return canvas


                resized = cv2.resize(
                    img,
                    (
                        new_w,
                        new_h
                    )
                )


                x = int(
                    x - new_w / 2
                )

                y = int(
                    y - new_h / 2
                )


                if (
                    x >= self.W
                    or y >= self.H
                    or x + new_w <= 0
                    or y + new_h <= 0
                ):
                    return canvas


                x1 = max(
                    0,
                    x
                )

                y1 = max(
                    0,
                    y
                )

                x2 = min(
                    self.W,
                    x + new_w
                )

                y2 = min(
                    self.H,
                    y + new_h
                )


                canvas[
                    y1:y2,
                    x1:x2
                ] = resized[
                    0:(y2-y1),
                    0:(x2-x1)
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

        images = [
            self._load(c)
            for c in clips
        ]


        HERO_DURATION = 12
        CONVEYOR_DURATION = 12
        SPLIT_DURATION = 12
        CIRCLE_DURATION = 12


        HERO_END = HERO_DURATION

        CONVEYOR_END = (
            HERO_END
            +
            CONVEYOR_DURATION
        )

        SPLIT_END = (
            CONVEYOR_END
            +
            SPLIT_DURATION
        )

        CIRCLE_END = (
            SPLIT_END
            +
            CIRCLE_DURATION
        )


        total_duration = CIRCLE_END



        def make_frame(t):

            canvas = self._canvas()



            # ==================================================
            # SEGMENT 1
            # HERO FLOW
            #
            # KEPT UNCHANGED
            # ==================================================

            if t < HERO_END:


                per_img = (
                    HERO_DURATION
                    /
                    total
                )


                for i, img in enumerate(images):


                    start = (
                        i
                        *
                        per_img
                    )

                    end = (
                        start
                        +
                        per_img
                    )


                    if not (
                        start
                        <=
                        t
                        <
                        end
                    ):
                        continue



                    local_t = (
                        t - start
                    ) / per_img



                    if local_t < 0.40:


                        p = (
                            local_t
                            /
                            0.40
                        )


                        x = self.W / 2

                        y = (
                            self.H
                            +
                            300
                            -
                            p *
                            (
                                self.H / 2
                                +
                                300
                            )
                        )


                        zoom = 0.22



                    elif local_t < 0.60:


                        x = self.W / 2

                        y = self.H / 2

                        zoom = 0.24



                    elif local_t < 0.80:


                        p = (
                            local_t
                            -
                            0.60
                        ) / 0.20


                        x = self.W / 2

                        y = self.H / 2


                        zoom = (
                            0.24
                            -
                            0.05 *
                            math.sin(
                                p *
                                math.pi
                            )
                        )



                    else:


                        p = (
                            local_t
                            -
                            0.80
                        ) / 0.20


                        x = self.W / 2


                        y = (
                            self.H / 2
                            -
                            p *
                            (
                                self.H / 2
                                +
                                400
                            )
                        )


                        zoom = 0.22



                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )

                        # ==================================================
            # SEGMENT 2
            # FILMSTRIP TABLE-SCROLL CONVEYOR
            #
            # Requirements:
            # - images move across like conveyor belt
            # - no overlap
            # - one image follows another
            # - center pause
            # - zoom out
            # - zoom in
            # - continue scrolling
            # ==================================================

            elif t < CONVEYOR_END:


                local = (
                    t - HERO_END
                ) / CONVEYOR_DURATION


                spacing = int(
                    self.W * 0.65
                )


                center_x = self.W / 2


                for i, img in enumerate(images):


                    # Each image has a fixed place
                    # on the conveyor track

                    start_position = (
                        self.W
                        +
                        spacing
                    )


                    travel = (
                        local
                        *
                        (
                            self.W
                            +
                            spacing
                            *
                            (
                                total
                                +
                                1
                            )
                        )
                    )


                    x = (
                        start_position
                        +
                        i * spacing
                        -
                        travel
                    )


                    y = self.H / 2


                    # Individual center focus
                    # when image reaches center

                    distance = abs(
                        x - center_x
                    )


                    if distance < self.W * 0.10:


                        zoom = (
                            0.22
                            -
                            0.02 *
                            math.sin(
                                local *
                                math.pi
                            )
                        )

                    else:

                        zoom = 0.20



                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )



            # ==================================================
            # SEGMENT 3
            # MILITARY FORMATION
            #
            # Formation:
            #
            # IMAGE       IMAGE
            # IMAGE       IMAGE
            # IMAGE       IMAGE
            #
            #             YOU
            #
            # Motion:
            #
            # \ \ \ \
            #
            #        YOU
            #
            # / / / /
            #
            # Creates corridor effect
            # ==================================================

            elif t < SPLIT_END:


                p = (
                    t
                    -
                    CONVEYOR_END
                ) / SPLIT_DURATION



                center_x = self.W / 2


                left_images = images[::2]

                right_images = images[1::2]



                # -----------------------------
                # LEFT COLUMN
                # -----------------------------

                for row, img in enumerate(left_images):


                    start_x = (
                        center_x
                        -
                        self.W * 0.30
                    )


                    if p < 0.55:


                        x = (
                            start_x
                            +
                            p *
                            (
                                self.W * 0.05
                            )
                        )


                        y = (
                            250
                            +
                            row *
                            260
                        )


                    else:


                        peel = (
                            p
                            -
                            0.55
                        ) / 0.45


                        x = (
                            start_x
                            -
                            peel *
                            self.W *
                            0.45
                        )


                        y = (
                            450
                            +
                            row *
                            120
                        )



                    zoom = (
                        0.16
                        +
                        p *
                        0.12
                    )


                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )



                # -----------------------------
                # RIGHT COLUMN
                # -----------------------------

                for row, img in enumerate(right_images):


                    start_x = (
                        center_x
                        +
                        self.W * 0.30
                    )


                    if p < 0.55:


                        x = (
                            start_x
                            -
                            p *
                            (
                                self.W * 0.05
                            )
                        )


                        y = (
                            250
                            +
                            row *
                            260
                        )


                    else:


                        peel = (
                            p
                            -
                            0.55
                        ) / 0.45


                        x = (
                            start_x
                            +
                            peel *
                            self.W *
                            0.45
                        )


                        y = (
                            450
                            +
                            row *
                            120
                        )



                    zoom = (
                        0.16
                        +
                        p *
                        0.12
                    )


                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )



            # ==================================================
            # SEGMENT 4
            # CIRCULAR MOTION
            #
            # All images remain inside canvas
            # ==================================================

            else:


                p = (
                    t
                    -
                    SPLIT_END
                ) / CIRCLE_DURATION



                radius = min(
                    self.W,
                    self.H
                ) * 0.25



                rotation = (
                    p
                    *
                    4
                    *
                    math.pi
                )



                for i, img in enumerate(images):


                    angle = (
                        (
                            2
                            *
                            math.pi
                            *
                            i
                            /
                            total
                        )
                        +
                        rotation
                    )



                    x = (
                        self.W / 2
                        +
                        radius *
                        math.cos(
                            angle
                        )
                    )


                    y = (
                        self.H / 2
                        +
                        radius *
                        math.sin(
                            angle
                        )
                    )



                    zoom = 0.16



                    canvas = self._blit(
                        canvas,
                        img,
                        x,
                        y,
                        zoom
                    )


            return canvas



        # --------------------------------------------------
        # CREATE VIDEO
        # --------------------------------------------------

        video = VideoClip(
            make_frame,
            duration=total_duration
        )


        # --------------------------------------------------
        # AUDIO
        # --------------------------------------------------

        if (
            music_path
            and
            os.path.exists(
                music_path
            )
        ):


            audio = AudioFileClip(
                music_path
            )


            if audio.duration > total_duration:

                audio = audio.subclip(
                    0,
                    total_duration
                )


            video = video.set_audio(
                audio
            )



        # --------------------------------------------------
        # EXPORT
        # --------------------------------------------------

        output_folder = os.path.dirname(
            output_file
        )


        if output_folder:

            os.makedirs(
                output_folder,
                exist_ok=True
            )


        video.write_videofile(
            output_file,
            fps=30,
            codec="libx264",
            bitrate="6000k",
            audio_codec="aac"
        )


        return output_file        

