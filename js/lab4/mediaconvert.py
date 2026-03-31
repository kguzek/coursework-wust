import os
import sys
from datetime import datetime
from typing import Optional, Tuple
import utils


def get_output_filename(original_path: str, output_format: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d")
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    return f"{timestamp}-{base_name}.{output_format}"


def convert_file(
    input_path: str, output_format: str, converted_dir: str
) -> Tuple[Optional[str], Optional[str]]:
    output_filename = get_output_filename(input_path, output_format)
    output_path = os.path.join(converted_dir, output_filename)

    success: bool
    program: str
    if utils.is_image(input_path):
        success = utils.run_imagemagick(input_path, output_path)
        program = "imagemagick"
    elif utils.is_media(input_path):
        success = utils.run_ffmpeg(input_path, output_path)
        program = "ffmpeg"
    else:
        success = utils.run_ffmpeg(input_path, output_path)
        program = "ffmpeg"

    if success:
        return output_path, program
    return None, None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: mediaconvert.py <directory> [output_format]", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    output_format: str = sys.argv[2] if len(sys.argv) > 2 else "webm"

    if not os.path.isdir(directory):
        print(f"Not a directory: {directory}", file=sys.stderr)
        sys.exit(1)

    converted_dir = utils.ensure_converted_dir()
    history_file = os.path.join(converted_dir, "history.json")

    files = utils.find_files(directory, utils.ALL_CONVERTIBLE_EXTENSIONS)

    for filepath in files:
        output_path, program = convert_file(filepath, output_format, converted_dir)
        if output_path and program:
            utils.log_conversion(
                history_file, filepath, output_format, output_path, program
            )
            print(f"Converted: {filepath} -> {output_path}")
        else:
            print(f"Failed: {filepath}", file=sys.stderr)


if __name__ == "__main__":
    main()
