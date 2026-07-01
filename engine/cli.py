import os

from engine.auto_editor import AutoEditor
from engine.core.storage_manager import StorageManager


def main():

    storage = StorageManager()

    print("🎬 Cinematic Engine v4.3 (Auto Storage Enabled)")
    print(f"📦 Using base path: {storage.base_path}")

    editor = AutoEditor(
        photo_folder=storage.photos,
        music_file=os.path.join(storage.music, "background_music.mp3"),
        output_file=os.path.join(storage.output, "final.mp4")
    )

    editor.run()


if __name__ == "__main__":
    main()