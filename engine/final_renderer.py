import subprocess
import os

class FinalRenderer:

    def __init__(self, output_file="output/travel_video.mp4"):
        self.output_file = output_file

    def create_concat_file(self, clips):
        """
        FFmpeg concat list
        """
        list_path = "output/clips.txt"

        with open(list_path, "w") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")

        return list_path

    def render_final_video(self, clips, music_path=None):
        list_file = self.create_concat_file(clips)

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy"
        ]

        # If music exists, add audio properly
        if music_path and os.path.exists(music_path):
            cmd = [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-i", music_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                self.output_file
            ]

        else:
            cmd.append(self.output_file)

        subprocess.run(cmd, check=True)

        print(f"\n🎉 FINAL VIDEO CREATED: {self.output_file}")