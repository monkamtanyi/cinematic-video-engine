
import os
import subprocess

from motion_engine import MotionEngine


class VideoRenderer:

    def __init__(self, output_folder="output"):
        self.output_folder = output_folder
        self.engine = MotionEngine()

        os.makedirs(output_folder, exist_ok=True)

    # ==========================================
    # Render one image into one video clip
    # ==========================================
    def render_scene(self, image_path, output_path, motion, duration=3):

        cfg = self.engine.get_ffmpeg_zoompan(motion, duration)

        zoom_start = cfg["zoom_start"]
        zoom_end = cfg["zoom_end"]
        x = cfg["x"]
        y = cfg["y"]
        frames = cfg["frames"]

        # FFmpeg uses "on" (output frame number), not "t"
        zoom_expr = f"'{zoom_start}+({zoom_end}-{zoom_start})*on/{frames}'"

        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "fps=30,"
            f"zoompan=z={zoom_expr}:"
            f"x='{x}':"
            f"y='{y}':"
            f"d={frames}:"
            "s=1080x1920"
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", image_path,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            output_path
        ]

        print(f"🎬 {motion['type']} -> {image_path}")

        subprocess.run(cmd, check=True)

    # ==========================================
    # Render all scenes
    # ==========================================
    def render_timeline(self, timeline, duration=3):

        clips = []

        for i, scene in enumerate(timeline):

            image = scene["image"]
            motion = scene["motion"]

            clip_path = os.path.join(
                self.output_folder,
                f"clip_{i}.mp4"
            )

            self.render_scene(
                image_path=image,
                output_path=clip_path,
                motion=motion,
                duration=duration
            )

            clips.append(clip_path)

        return clips

    # ==========================================
    # Merge all clips into one video
    # ==========================================
    def merge_clips(self, clips, output_file="travel_video.mp4"):

        list_file = os.path.join(
            self.output_folder,
            "clips.txt"
        )

        with open(list_file, "w", encoding="utf-8") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_file
        ]

        subprocess.run(cmd, check=True)

        print()
        print("====================================")
        print("✅ VIDEO CREATED SUCCESSFULLY")
        print(f"📁 {output_file}")
        print("====================================")

