from dataclasses import dataclass
from PIL import Image

@dataclass
class Frame:
    image: Image.Image
    duration: float
    motion_type: str