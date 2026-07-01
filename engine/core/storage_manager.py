import os
import shutil


class StorageManager:

    def __init__(self):

        self.base_path = self._detect_base_path()

        self.photos = os.path.join(self.base_path, "photos")
        self.music = os.path.join(self.base_path, "music")
        self.output = os.path.join(self.base_path, "output")
        self.temp = os.path.join(self.base_path, "temp")

        self._create_dirs()

    def _detect_base_path(self):

        # Prefer external drive
        if os.path.exists("D:\\"):
            return "D:\\CinematicEngine"

        # fallback to C:
        return "C:\\CinematicEngine"

    def _create_dirs(self):

        for path in [self.photos, self.music, self.output, self.temp]:
            os.makedirs(path, exist_ok=True)

    def resolve_media_path(self, folder, filename):

        return os.path.join(folder, filename)

    def clear_temp(self):

        if os.path.exists(self.temp):
            shutil.rmtree(self.temp, ignore_errors=True)
            os.makedirs(self.temp, exist_ok=True)