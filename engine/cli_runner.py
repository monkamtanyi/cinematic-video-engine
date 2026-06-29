import os
import yaml

from engine.auto_editor import AutoEditor
from engine.logger import get_logger


log = get_logger()


def load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_config(cfg):
    required = ["photos", "output"]

    for key in required:
        if key not in cfg:
            raise ValueError(f"Missing required config key: {key}")

    if not os.path.exists(cfg["photos"]):
        raise FileNotFoundError(f"Photos folder not found: {cfg['photos']}")

    if cfg.get("music") and not os.path.exists(cfg["music"]):
        raise FileNotFoundError(f"Music file not found: {cfg['music']}")


def ensure_output(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)


def run_engine(config_path):
    try:
        log.info("🚀 Cinematic Engine Starting...")

        cfg = load_config(config_path)
        validate_config(cfg)

        ensure_output(cfg["output"])

        log.info("Loading images...")

        editor = AutoEditor(
            photo_folder=cfg["photos"],
            music_file=cfg.get("music"),
            output_file=cfg["output"]
        )

        editor.run()

        log.info("✅ Render complete")

    except Exception as e:
        log.error(f"❌ Engine failed: {e}")
        raise