from moviepy.editor import *
import os
import math
from engine.core.motion_engine import MotionEngine


class VideoRenderer:

    def __init__(self, output_path, w=1080, h=1920):
        self.output_path = output_path
        self.w = w
        self.h = h
        self.m = MotionEngine()

    def cover(self, clip):
        iw, ih = clip.size
        s = max(self.w / iw, self.h / ih)

        clip = clip.resize(s)

        return clip.crop(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=self.w,
            height=self.h
        )

    def to_pos(self, m):
        return (
            (m["x"] * self.w / 2) + self.w / 2,
            (m["y"] * self.h / 2) + self.h / 2
        )

    # SEGMENT 1
    def seg1(self, frames, duration):

        clips = []
        per = duration / len(frames)

        dirs = ["left", "right", "top", "bottom", "tl", "br"]

        for i, f in enumerate(frames):

            clip = self.cover(ImageClip(f)).set_duration(per)

            d = dirs[i % len(dirs)]

            def pos(t, i=i, d=d):
                m = self.m.hero(t / per, d)
                return self.to_pos(m)

            def scale(t):
                m = self.m.hero(t / per, d)
                return m["scale"]

            clips.append(clip.set_position(pos).resize(scale))

        return concatenate_videoclips(clips, method="compose")

    # SEGMENT 2
    def seg2(self, frames, duration):

        clips = []
        per = duration

        spacing = self.w * 0.3

        for i, f in enumerate(frames):

            clip = self.cover(ImageClip(f)).resize(width=self.w * 0.3).set_duration(per)

            def pos(t, i=i):
                x = (i * spacing) - (t * self.w * 0.8)
                return (x, self.h * 0.35)

            clips.append(clip.set_position(pos))

        return CompositeVideoClip(clips, size=(self.w, self.h)).set_duration(per)

    # SEGMENT 3
    def seg3(self, frames, duration):

        clips = []
        pairs = [frames[i:i+2] for i in range(0, len(frames), 2)]
        per = duration / len(pairs)

        for pair in pairs:

            if len(pair) < 2:
                continue

            left = self.cover(ImageClip(pair[0])).resize(width=self.w * 0.4)
            right = self.cover(ImageClip(pair[1])).resize(width=self.w * 0.4)

            def lpos(t):
                m = self.m.split(t / per, "L")
                return self.to_pos(m)

            def rpos(t):
                m = self.m.split(t / per, "R")
                return self.to_pos(m)

            clips.append(left.set_duration(per).set_position(lpos))
            clips.append(right.set_duration(per).set_position(rpos))

        return CompositeVideoClip(clips, size=(self.w, self.h)).set_duration(duration)

    # SEGMENT 4
    def seg4(self, frames, duration):

        clips = []
        per = duration

        total = len(frames)

        for i, f in enumerate(frames):

            clip = self.cover(ImageClip(f)).resize(width=self.w * 0.3).set_duration(per)

            def pos(t, i=i):
                m = self.m.wheel(t / per, i, total)
                return self.to_pos(m)

            clips.append(clip.set_position(pos))

        return CompositeVideoClip(clips, size=(self.w, self.h)).set_duration(per)

    # RENDER
    def render(self, frames, music_path=None):

        total = max(len(frames) * 3, 30)

        seg1 = self.seg1(frames, total * 0.50)
        seg2 = self.seg2(frames, total * 0.15)
        seg3 = self.seg3(frames, total * 0.15)
        seg4 = self.seg4(frames, total * 0.20)

        final = concatenate_videoclips([seg1, seg2, seg3, seg4], method="compose")

        if music_path and os.path.exists(music_path):
            audio = AudioFileClip(music_path)
            final = final.set_audio(audio.subclip(0, final.duration))

        final.write_videofile(
            self.output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac"
        )