import yaml
from engine.auto_editor import AutoEditor


def main():

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    editor = AutoEditor(
        photo_folder=config["photos"],
        music_file=config["music"],
        output_file=config["output"]
    )

    print("🎬 Cinematic Engine v4.2 (Production)")

    editor.run()


if __name__ == "__main__":
    main()