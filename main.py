import os
import logging

from engine.core.video_renderer import VideoRenderer

logging.basicConfig(level=logging.INFO)


def main():

    print("🎬 Cinematic Engine V5 Starting...")

    image_folder = r"D:\CinematicEngine\photos"

    clips = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    clips.sort()

    if not clips:
        raise Exception(f"No images found in {image_folder}")

    # ✅ FIXED MUSIC PATH
    music = r"D:\CinematicEngine\music\background_music.mp3"

    renderer = VideoRenderer()

    output = renderer.render(
        clips=clips,
        music_path=music,
        output_file="output/final.mp4"
    )

    print("\n===================================")
    print("✅ VIDEO CREATED SUCCESSFULLY")
    print(f"📁 {output}")
    print("===================================")


if __name__ == "__main__":
    main()