
import os
import shutil
import tempfile

import gradio as gr

from engine.core.video_renderer import VideoRenderer


# --------------------------------------------------
# INITIALIZE ENGINE
# --------------------------------------------------

renderer = VideoRenderer()

OUTPUT_DIR = "output"


# --------------------------------------------------
# VIDEO GENERATION FUNCTION
# --------------------------------------------------

def generate_video(images, music):

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

        for img in images:

            filename = os.path.basename(img)

            destination = os.path.join(
                temp_dir,
                filename
            )

            shutil.copy(
                img,
                destination
            )

            image_paths.append(
                destination
            )


        # ------------------------------------------
        # MUSIC FILE
        # ------------------------------------------

        music_path = None

        if music:
            music_path = music


        # ------------------------------------------
        # OUTPUT
        # ------------------------------------------

        output_file = os.path.join(
            OUTPUT_DIR,
            "final.mp4"
        )


        # ------------------------------------------
        # RENDER CINEMATIC VIDEO
        # ------------------------------------------

        result = renderer.render(
            clips=image_paths,
            music_path=music_path,
            output_file=output_file
        )


        return result


    except Exception as e:

        raise gr.Error(
            f"Video generation failed: {str(e)}"
        )


    finally:

        # Remove temporary upload folder
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

        The AI Cinematic Engine will generate a vertical cinematic video.
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


    # Local Windows:
    # http://127.0.0.1:7860
    #
    # Hugging Face:
    # automatically uses 0.0.0.0

    host = (
        "0.0.0.0"
        if os.getenv("SPACE_ID")
        else "127.0.0.1"
    )


    demo.launch(
        server_name=host,
        server_port=7860
    )
