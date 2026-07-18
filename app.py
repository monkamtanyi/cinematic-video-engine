
import os
import shutil
import tempfile
import time

import gradio as gr
from PIL import Image

from engine.core.video_renderer import VideoRenderer
from engine.core.audio_utils import normalize_audio


# --------------------------------------------------
# INITIALIZE ENGINE
# --------------------------------------------------

renderer = VideoRenderer()

OUTPUT_DIR = "output"


# --------------------------------------------------
# VIDEO GENERATION FUNCTION
# --------------------------------------------------

def generate_video(images, music, progress=None):

    if progress is None:
        progress = lambda *args, **kwargs: None

    progress(0.0, desc="Starting AI Cinematic Engine...")

    if not images:
        raise gr.Error(
            "Please upload at least one image."
        )

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    temp_dir = tempfile.mkdtemp()

    try:

        image_paths = []

        # ------------------------------------------
        # COPY UPLOADED IMAGES
        # ------------------------------------------

        progress(0.10, desc="Preparing uploaded images...")

        total = len(images)

        for index, img in enumerate(images):

            filename = os.path.basename(img)

            destination = os.path.join(
                temp_dir,
                filename
            )

            image = Image.open(img)

            image.thumbnail(
                (1600,1600)
            )

            image.save(
                destination,
                quality=95
            )

            image_paths.append(destination)

            progress(
                0.10 + (0.20 * ((index + 1) / total)),
                desc=f"Loading image {index + 1} of {total}"
            )

        # ------------------------------------------
        # MUSIC FILE
        # ------------------------------------------

        music_path = None

        if music:
            music_path = music
        else:
            default_music = os.path.join(
                os.getcwd(),
                "music",
                "background_music.mp3"
            )

            if os.path.exists(default_music):
                music_path = default_music

        # ------------------------------------------
        # OUTPUT
        # ------------------------------------------

        output_file = os.path.join(
            OUTPUT_DIR,
            f"final_{int(time.time())}.mp4"
        )

        # Keep previous generated videos available
        # Do not delete existing output on refresh
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # ------------------------------------------
        # RENDER
        # ------------------------------------------

        progress(
            0.35,
            desc="Rendering cinematic video..."
        )

        music_path = normalize_audio(music)

        result = renderer.render(
            clips=image_paths,
            music_path=music_path,
            output_file=output_file
        )

        progress(
            0.95,
            desc="Finalizing video..."
        )

        if result is None:
            result = output_file

        if not os.path.exists(result):
            raise gr.Error(
                "Video generation completed but no output video was found."
            )

        progress(
            1.0,
            desc="Done!"
        )

        return result

    except Exception as e:

        raise gr.Error(
            f"Video generation failed:\n\n{str(e)}"
        )

    finally:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )


# --------------------------------------------------
# GRADIO INTERFACE
# --------------------------------------------------

with gr.Blocks(
    title="AI Cinematic Video Creator"
) as demo:

    gr.Markdown(
        """
# 🎬 AI Cinematic Video Creator

Upload your photos and optional background music.

The AI Cinematic Engine will automatically create a cinematic vertical video with professional camera motion.
"""
    )

    images = gr.File(
        label="Upload Images",
        file_count="multiple",
        file_types=["image"],
        type="filepath"
    )

    music = gr.File(
        label="Upload Background Music (Optional)",
        file_types=["audio"],
        type="filepath"
    )

    render_button = gr.Button(
        "🎥 Generate Video",
        variant="primary"
    )

    output_video = gr.Video(
        label="Generated Video"
    )

    render_button.click(
        fn=generate_video,
        inputs=[
            images,
            music
        ],
        outputs=output_video
    )


# --------------------------------------------------
# APPLICATION START
# --------------------------------------------------

if __name__ == "__main__":

    host = (
        "0.0.0.0"
        if os.getenv("SPACE_ID")
        else "127.0.0.1"
    )

    demo.launch(
        server_name=host,
        server_port=7860
    )