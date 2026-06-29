import subprocess


class FrameRenderer:

    def render_folder(self, frames_dir, output_file="output/final.mp4", fps=30):

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", str(fps),
            "-i", f"{frames_dir}/frame_%04d.jpg",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "slow",
            "-movflags", "+faststart",
            output_file
        ]

        subprocess.run(cmd, check=True)

        print(f"🎬 Video created: {output_file}")