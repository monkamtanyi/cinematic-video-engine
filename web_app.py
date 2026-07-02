import os
import tempfile
import gradio as gr

from engine.core.video_renderer import VideoRenderer

renderer = VideoRenderer()


def create_video(files):

    temp_dir = tempfile.mkdtemp()

    image_paths = []

    for f in files:

        image_paths.append(f.name)

    output_file = os.path.join(
        temp_dir,
        "travel_video.mp4"
    )

    renderer.render(
        clips=image_paths,
        music_path=r"D:\CinematicEngine\music\background_music.mp3",
        output_file=output_file
    )

    return output_file


app = gr.Interface(
    fn=create_video,
    inputs=gr.Files(
        label="Upload Photos"
    ),
    outputs=gr.File(
        label="Download Video"
    ),
    title="AI Cinematic Travel Video Creator",
    description="Upload photos and generate a cinematic travel video."
)

app.launch()