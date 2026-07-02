import os
import tempfile
import gradio as gr

from engine.core.video_renderer import VideoRenderer

renderer = VideoRenderer()


def generate_video(files):

    if not files:
        raise ValueError("Please upload photos.")

    temp_dir = tempfile.mkdtemp()

    image_paths = []

    for f in files:
        image_paths.append(f.name)

    output_file = os.path.join(
        temp_dir,
        "travel_video.mp4"
    )

    music_path = r"D:\CinematicEngine\music\background_music.mp3"

    renderer.render(
        clips=image_paths,
        music_path=music_path,
        output_file=output_file
    )

    return output_file


demo = gr.Interface(
    fn=generate_video,
    inputs=gr.Files(
        label="Upload Travel Photos"
    ),
    outputs=gr.File(
        label="Download MP4"
    ),
    title="AI Cinematic Travel Video Creator",
    description="Upload photos and generate a cinematic travel video."
)

demo.launch(
    share=True
)