import gradio as gr
from engine.core.video_renderer import VideoRenderer

renderer = VideoRenderer()

def generate(files):
    if not files:
        return None

    # Convert Gradio file objects to file paths
    paths = [f.name for f in files]

    # Render video
    output_path = renderer.render(paths)

    return output_path

demo = gr.Interface(
    fn=generate,
    inputs=gr.File(file_count="multiple", type="filepath"),
    outputs=gr.Video(),
    title="Cinematic Travel Engine v5",
    description="Upload images → generate cinematic travel video"
)

if __name__ == "__main__":
    demo.launch()