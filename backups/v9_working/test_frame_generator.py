from engine.frame_generator import FrameGenerator

generator = FrameGenerator()

folder = generator.generate_frames(
    "photos/PR01.jpeg",
    motion="zoom_in",
    duration=3,
    intensity=1.2
)

print("Frames saved to:")
print(folder)