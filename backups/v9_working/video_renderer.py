import os

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)

from transition_engine import TransitionEngine
from motion_engine import MotionEngine


class VideoRenderer:

    def __init__(self, output_path="output/final.mp4"):

        self.output_path = output_path

        self.W = 1280
        self.H = 720

        self.fps = 30
        self.codec = "libx264"
        self.audio_codec = "aac"
        self.bitrate = "5000k"
        self.pix_fmt = "yuv420p"

        self.transition_engine = TransitionEngine()
        self.motion_engine = MotionEngine()

    # --------------------------------------------------
    # EVEN NUMBER FIX
    # --------------------------------------------------
    def _even(self, value):

        value = int(value)

        if value % 2 != 0:
            value -= 1

        return value

    # --------------------------------------------------
    # FIT IMAGE
    #
    # IMPORTANT:
    # Leave movement room around image
    # --------------------------------------------------
    def _fit_image(self, clip):

        target_w = int(self.W * 0.72)
        target_h = int(self.H * 0.72)

        scale = min(
            target_w / clip.w,
            target_h / clip.h
        )

        new_w = self._even(clip.w * scale)
        new_h = self._even(clip.h * scale)

        return clip.resize((new_w, new_h))

    # --------------------------------------------------
    # TRUE MOTION ENGINE
    # --------------------------------------------------
    def _camera(self, clip, index):

        pattern = self.motion_engine.motion_for_clip(index)

        duration = clip.duration

        def position(t):

            progress = t / duration

            if progress < 0:
                progress = 0

            if progress > 1:
                progress = 1

            dx, dy = self.motion_engine.path(
                pattern,
                progress
            )

            center_x = int((self.W - clip.w) / 2)
            center_y = int((self.H - clip.h) / 2)

            return (
                int(center_x + dx),
                int(center_y + dy)
            )

        return clip.set_position(position)

    # --------------------------------------------------
    # VARIABLE SPEEDS
    # --------------------------------------------------
    def _duration(self, index):

        durations = [
            4.0,
            4.5,
            5.0,
            5.5,
            6.0
        ]

        return durations[index % len(durations)]

    # --------------------------------------------------
    # CREATE ANIMATED CLIP
    # --------------------------------------------------
    def _build_clip(self, frame, index):

        image = ImageClip(frame)

        image = self._fit_image(image)

        image = image.set_duration(
            self._duration(index)
        )

        image = self._camera(
            image,
            index
        )

        canvas = CompositeVideoClip(
            [image],
            size=(self.W, self.H)
        )

        canvas = canvas.set_duration(
            image.duration
        )

        return canvas

    # --------------------------------------------------
    # BUILD ALL CLIPS
    # --------------------------------------------------
    def build_clips(self, frames):

        clips = []

        total = len(frames)

        for index, frame in enumerate(frames):

            print(
                f"🎬 Clip {index+1}/{total}"
            )

            clip = self._build_clip(
                frame,
                index
            )

            clips.append(clip)

        return clips

    # --------------------------------------------------
    # AUDIO
    # --------------------------------------------------
    def add_audio(self, video, music_path):

        if not music_path:
            return video

        if not os.path.exists(music_path):
            return video

        audio = AudioFileClip(music_path)

        if audio.duration > video.duration:

            audio = audio.subclip(
                0,
                video.duration
            )

        return video.set_audio(audio)

    # --------------------------------------------------
    # RENDER
    # --------------------------------------------------
    def render(
        self,
        frames,
        beats=None,
        motions=None,
        music_path=None
    ):

        print(
            "🎬 MOTION RENDER ENGINE START"
        )

        clips = self.build_clips(frames)

        print(
            "🎞 Applying transitions..."
        )

        clips = self.transition_engine.apply(clips)

        print(
            "🔗 Concatenating..."
        )

        video = concatenate_videoclips(
            clips,
            method="compose"
        )

        print(
            "🎵 Adding audio..."
        )

        video = self.add_audio(
            video,
            music_path
        )

        output_dir = os.path.dirname(
            self.output_path
        )

        if output_dir:

            os.makedirs(
                output_dir,
                exist_ok=True
            )

        print(
            "📤 Exporting..."
        )

        video.write_videofile(
            self.output_path,
            fps=self.fps,
            codec=self.codec,
            audio_codec=self.audio_codec,
            bitrate=self.bitrate,
            ffmpeg_params=[
                "-pix_fmt",
                self.pix_fmt
            ]
        )

        video.close()

        print(
            f"✅ COMPLETE: {self.out