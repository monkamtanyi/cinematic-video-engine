from auto_editor import AutoEditor


def main():

    print("🚀 Starting Fully AI Auto Editor...")

    editor = AutoEditor(
        photo_folder="photos",
        music_file="music/background_music.mp3",
        output_file="output/final.mp4"
    )

    # 🎬 RUN FULL PIPELINE (now returns beats-aware rendering)
    editor.render()

    print("🎉 Video generation complete!")


if __name__ == "__main__":
    main()