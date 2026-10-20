#!/usr/bin/env python3
"""Run a narrowly scoped Windows UI inspection through UTM. Standard library only."""

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path


def call(args, *, data=None, timeout=20):
    result = subprocess.run(
        ["utmctl", *args], input=data, capture_output=True, timeout=timeout
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def pull_json(vm, path):
    try:
        result = json.loads(call(["file", "pull", vm, path]).decode("utf-8-sig"))
    except (RuntimeError, ValueError, subprocess.TimeoutExpired):
        return None  # Missing, still being written, or temporarily locked.
    if not isinstance(result, dict) or not isinstance(result.get("ok"), bool):
        raise RuntimeError(f"Invalid guest status document: {path}")
    return result


def command(vm, text):
    return call(["exec", vm, "--cmd", r"C:\Windows\System32\cmd.exe", "/c", text])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vm", required=True, help="UTM VM name or UUID")
    parser.add_argument("--process", required=True, help="Process name without .exe")
    parser.add_argument("--pid", type=int, help="Disambiguate multiple matching processes")
    parser.add_argument("--output", required=True, type=Path, help="New host JSON file")
    parser.add_argument("--screenshot", type=Path, help="New host PNG; entire guest desktop")
    parser.add_argument("--command-id", type=int, help="Post a verified WM_COMMAND once")
    parser.add_argument("--timeout", type=float, default=90, help="Guest result wait, 1-240 seconds")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", args.process):
        parser.error("process must contain only letters, numbers, _, -, or .")
    if args.process.lower().endswith(".exe"):
        parser.error("omit .exe from the process name")
    # The guest task has a five-minute lifetime; reserve time for cleanup.
    if not math.isfinite(args.timeout) or not 1 <= args.timeout <= 240:
        parser.error("timeout must be finite and between 1 and 240 seconds")
    if args.pid is not None and args.pid <= 0:
        parser.error("pid must be positive")
    if args.command_id is not None and not 1 <= args.command_id <= 65535:
        parser.error("command-id must be between 1 and 65535")
    for path in (args.output, args.screenshot):
        if path and (path.exists() or not path.parent.is_dir()):
            parser.error(f"output must be a new file in an existing directory: {path}")
    if args.screenshot and args.output.resolve() == args.screenshot.resolve():
        parser.error("JSON and screenshot paths must differ")
    if not shutil.which("utmctl"):
        parser.error("utmctl not found on PATH")

    token = uuid.uuid4().hex
    directory = rf"C:\Windows\Temp\opencode-ui-{token}"
    task = f"OpenCode-UI-{token}"
    print(f"Guest artifacts: {directory}\nTemporary task: {task}", file=sys.stderr)
    request = {
        "process": args.process,
        "pid": args.pid,
        "commandId": args.command_id,
        "screenshot": bool(args.screenshot),
        "task": task,
    }
    scripts = Path(__file__).resolve().parent
    submitted = False
    completed = False
    try:
        command(args.vm, f"mkdir {directory}")
        for name, content in (
            ("request.json", json.dumps(request).encode()),
            ("launch.ps1", (scripts / "launch.ps1").read_bytes()),
            ("inspect.ps1", (scripts / "inspect.ps1").read_bytes()),
        ):
            call(["file", "push", args.vm, directory + "\\" + name], data=content)
        executable = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        submitted = True
        command(
            args.vm,
            f"{executable} -NoProfile -NonInteractive -ExecutionPolicy Bypass "
            f"-File {directory}\\launch.ps1 -RunDir {directory} "
            f"> {directory}\\launch.log 2>&1",
        )
        deadline = time.monotonic() + args.timeout
        result = None
        while time.monotonic() < deadline:
            launch = pull_json(args.vm, directory + r"\launch.json")
            if launch is not None and not launch.get("ok"):
                raise RuntimeError(f"Guest launcher failed: {launch.get('error')}")
            result = pull_json(args.vm, directory + r"\result.json")
            if result is not None:
                completed = True
                break
            time.sleep(1)
        if result is None:
            raise TimeoutError("Guest result deadline exceeded; inspect retained launch.log")
        if not result.get("ok"):
            raise RuntimeError(f"Desktop helper failed: {result.get('error')}")
        if args.screenshot:
            png = call(["file", "pull", args.vm, directory + r"\screen.png"])
            if not png.startswith(b"\x89PNG\r\n\x1a\n"):
                raise RuntimeError("Guest screenshot is not a PNG")
            with args.screenshot.open("xb") as file:
                file.write(png)
        with args.output.open("x", encoding="utf-8") as file:
            json.dump(result, file, indent=2, ensure_ascii=False)
            file.write("\n")
        print(f"Inspection saved: {args.output}")
    finally:
        if submitted:
            cleanup = []
            if not completed:
                cleanup.append(f"schtasks /End /TN {task} > {directory}\\end.log 2>&1")
            cleanup.append(f"schtasks /Delete /TN {task} /F > {directory}\\cleanup.log 2>&1")
            for text in cleanup:
                try:
                    command(args.vm, text)
                except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
                    print(f"WARNING: verify task cleanup manually ({task}): {error}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, TimeoutError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
