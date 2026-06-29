from dataclasses import dataclass

@dataclass
class MotionState:
    x: float
    y: float
    vx: float
    vy: float
    scale: float
    rotation: float