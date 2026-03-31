import json
import os
import subprocess
from datetime import datetime
from typing import Optional, Set, List, Dict


IMAGE_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
MEDIA_EXTENSIONS: Set[str] = {
    ".mp4",
    ".avi",
    ".mkv",
    ".mov",
    ".wmv",
    ".webm",
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    ".m4a",
}
ALL_CONVERTIBLE_EXTENSIONS: Set[str] = IMAGE_EXTENSIONS | MEDIA_EXTENSIONS


def find_files(directory: str, extensions: Optional[Set[str]] = None) -> List[str]:
    files: List[str] = []
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                if extensions:
                    ext = os.path.splitext(entry.name)[1].lower()
                    if ext in extensions:
                        files.append(entry.path)
                else:
                    files.append(entry.path)
    except PermissionError:
        pass
    return files


def get_converted_dir() -> str:
    return os.environ.get("CONVERTED_DIR", os.path.join(os.getcwd(), "converted"))


def ensure_converted_dir() -> str:
    converted_dir = get_converted_dir()
    os.makedirs(converted_dir, exist_ok=True)
    return converted_dir


def log_conversion(
    history_file: str,
    original_path: str,
    output_format: str,
    output_path: str,
    program: str,
) -> None:
    entry: Dict[str, str] = {
        "timestamp": datetime.now().isoformat(),
        "original_path": original_path,
        "output_format": output_format,
        "output_path": output_path,
        "program": program,
    }

    history: List[Dict[str, str]]
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def run_ffmpeg(input_path: str, output_path: str) -> bool:
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, output_path],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def run_imagemagick(input_path: str, output_path: str) -> bool:
    result = subprocess.run(
        ["magick", input_path, output_path],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def is_image(filepath: str) -> bool:
    ext = os.path.splitext(filepath)[1].lower()
    return ext in IMAGE_EXTENSIONS


def is_media(filepath: str) -> bool:
    ext = os.path.splitext(filepath)[1].lower()
    return ext in MEDIA_EXTENSIONS
