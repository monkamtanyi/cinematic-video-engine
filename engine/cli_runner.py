import os
import sys
import yaml
import logging

from engine.auto_editor import AutoEditor


# -----------------------------
# LOGGING (Windows-safe)
# -----------------------------
def setup_logger():
    logger = logging.getLogger("cinematic-engine")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


log = setup_logger()


# -----------------------------
# CONFIG LOADER
# -----------------------------
def load_config(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -----------------------------
# ENGINE RUNNER
# -----------------------------
def run_engine(photo_folder=None, music_file=None, output_file=None, config_path=None):

    log.info("Cinematic Engine Starting...")

    # -----------------------------
    # LOAD CONFIG MODE
    # -----------------------------
    if config_path:
        log.info(f"Loading config: {config_path}")
        config = load_config(config_path)

        photo_folder = config.get("photos")
        music_file = config.get("music")
        output_file = config.get("output")

    # -----------------------------
    # VALIDATION
    # -----------------------------
    if not photo_folder:
        raise ValueError("photo_folder is required")

    if not output_file:
        raise ValueError("output_file is required")

    if not os.path.exists(photo_folder):
        raise FileNotFoundError(f"Photo folder not found: {photo_folder}")

    music_path = None
    if music_file:
        music_path = music_file
        if not os.path.exists(music_path):
            log.warning(f"Music file not found: {music_path}")
            music_path = None

    # ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    log.info(f"Photos: {photo_folder}")
    log.info(f"Music: {music_path}")
    log.info(f"Output: {output_file}")

    # -----------------------------
    # RUN ENGINE
    # -----------------------------
    try:
        editor = AutoEditor(
            photo_folder=photo_folder,
            music_file=music_path,
            output_file=output_file
        )

        editor.run()

        log.info("Render complete")

    except Exception as e:
        log.error(f"Render failed: {str(e)}")
        raise


# -----------------------------
# CLI TEST MODE
# -----------------------------
if __name__ == "__main__":
    run_engine(
        photo_folder="photos",
        music_file="music/background_music.mp3",
        output_file="output/final.mp4"
    )