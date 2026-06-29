import argparse
from auto_editor import AutoEditor


def main():
    parser = argparse.ArgumentParser(description="Cinematic Video Engine")

    parser.add_argument("--photos", required=True)
    parser.add_argument("--music", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    editor = AutoEditor(
        photo_folder=args.photos,
        music_file=args.music,
        output_file=args.output
    )

    editor.run()


if __name__ == "__main__":
    main()