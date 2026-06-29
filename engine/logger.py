import logging
import os


def get_logger(name="cinematic"):
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/engine.log"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)