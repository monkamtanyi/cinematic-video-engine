from pathlib import Path
import subprocess
import tempfile


SUPPORTED_AUDIO = {
    ".mp3",
    ".m4a",
    ".aac",
    ".wav",
    ".flac",
    ".ogg",
    ".opus",
}


def normalize_audio(audio_path):
    """
    Normalize uploaded audio into MP3 format for FFmpeg rendering.

    Supports:
    MP3, M4A, AAC, WAV, FLAC, OGG, OPUS

    Returns:
        Path to normalized MP3 file
    """

    if not audio_path:
        return None

    source = Path(audio_path)

    if not source.exists():
        raise FileNotFoundError(
            f"Audio file not found: {source}"
        )

    suffix = source.suffix.lower()

    if suffix not in SUPPORTED_AUDIO:
        raise RuntimeError(
            f"Unsupported audio format: {suffix}"
        )

    # Already compatible
    if suffix == ".mp3":
        return str(source)

    output_dir = Path(
        tempfile.mkdtemp(prefix="audio_normalized_")
    )

    output = output_dir / f"{source.stem}.mp3"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "2",
        str(output),
    ]

    print("NORMALIZING AUDIO:")
    print(" ".join(command))

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(result.stderr)

        raise RuntimeError(
            "Audio conversion failed"
        )

    print(
        f"AUDIO NORMALIZED: {output}"
    )

    return str(output)