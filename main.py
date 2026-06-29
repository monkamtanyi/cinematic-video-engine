from auto_editor import AutoEditor


def main():

    editor = AutoEditor(
        photo_folder="photos",
        music_file="music.mp3",
        output_file="output/final.mp4"
    )

    editor.run()


if __name__ == "__main__":
    main()