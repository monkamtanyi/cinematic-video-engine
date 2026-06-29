import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    afx
)

from engine.core.motion_engine import MotionEngine


class VideoRenderer:
    """
    Cinematic Engine V2 - Stable Production Renderer

    Features:
    - 4 cinematic motion segments
    - deterministic motion engine
    - robust audio sync (loop/trim + fade)
    - FFmpeg-safe export pipeline
    """

    def __init__(self, output_file):
        self.output_file = output_file
        self.m = MotionEngine()

        self.seed = 42

    # ---------------- CLIP BUILDER ---------------- #

    def _make_clip(self, frame_path, duration, motion_fn):
        clip = ImageClip(frame_path).set_duration(duration)

        def pos(t):
            dx, dy = motion_fn(t)
            return (dx, dy)

        return clip.set_position(pos)

    # ---------------- SEGMENT 1 ---------------- #

    def seg1(self, frames, duration):
        clips = []
        per = duration / len(frames)

        for i, f in enumerate(frames):

            def motion(t, i=i):
                return self.m.drift(t + i * 0.1, per, seed=self.seed + i)

            clips.append(self._make_clip(f, per, motion))

        return concatenate_videoclips(clips, method="compose")

    # ---------------- SEGMENT 2 ---------------- #

    def seg2(self, frames, duration):
        clips = []
        per = duration / len(frames)

        for f in frames:
            clips.append(
                self._make_clip(
                    f,
                    per,
                    lambda t: self.m.conveyor(t, speed=120)
                )
            )

        return concatenate_videoclips(clips, method="compose")

    # ---------------- SEGMENT 3 ---------------- #

    def seg3(self, frames, duration):
        clips = []
        per = duration / len(frames)

        for i, f in enumerate(frames):
            side = "left" if i % 2 == 0 else "right"

            clips.append(
                self._make_clip(
                    f,
                    per,
                    lambda t, s=side: self.m.split(t, per, side=s)
                )
            )

        return concatenate_videoclips(clips, method="compose")

    # ---------------- SEGMENT 4 ---------------- #

    def seg4(self, frames, duration):
        clips = []
        per = duration / len(frames)

        for i, f in enumerate(frames):
            clips.append(
                self._make_clip(
                    f,
                    per,
                    lambda t, i=i: self.m.wheel(t + i * 0.2, radius=250, speed=2)
                )
            )

        return concatenate_videoclips(clips, method="compose")

    # ---------------- AUDIO ENGINE ---------------- #

    def _attach_audio(self, final, music_path):

        if not music_path or not os.path.exists(music_path):
            print("⚠️ No audio found:", music_path)
            return final

        print("🎵 Loading audio:", music_path)

        audio = AudioFileClip(music_path)

        print("🎵 Audio duration:", audio.duration)
        print("🎬 Video duration:", final.duration)

        # match durations safely
        if audio.duration < final.duration:
            audio = afx.audio_loop(audio, duration=final.duration)
        else:
            audio = audio.subclip(0, final.duration)

        audio = audio.audio_fadein(1.0).audio_fadeout(1.0)

        final = final.set_audio(audio)

        print("🎵 AUDIO ATTACHED SUCCESSFULLY")

        return final

    # ---------------- RENDER PIPELINE ---------------- #

    def render(self, frames, music_path=None):

        print("Rendering video...")

        total = 8  # seconds per segment block

        seg1 = self.seg1(frames, total * 0.5)
        seg2 = self.seg2(frames, total * 0.5)
        seg3 = self.seg3(frames, total * 0.5)
        seg4 = self.seg4(frames, total * 0.5)

        final = concatenate_videoclips(
            [seg1, seg2, seg3, seg4],
            method="compose"
        )

        final = self._attach_audio(final, music_path)

        print("FINAL DURATION:", final.duration)
        print("HAS AUDIO:", final.audio is not None)

        final.write_videofile(
            self.output_file,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            threads=4,
            ffmpeg_params=[
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart"
            ]
        )

        print("DONE")