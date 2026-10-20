"""Host-side regression tests; no VM or UTM installation required."""

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run


class RunnerTests(unittest.TestCase):
    @patch("run.subprocess.run")
    def test_command_arguments_are_not_interpolated_into_a_host_shell(self, execute):
        execute.return_value = subprocess.CompletedProcess([], 0, b"ok", b"")
        self.assertEqual(run.command("Windows VM", "echo test"), b"ok")
        self.assertEqual(execute.call_args.args[0], [
            "utmctl", "exec", "Windows VM", "--cmd",
            r"C:\Windows\System32\cmd.exe", "/c", "echo test",
        ])
        self.assertNotIn("shell", execute.call_args.kwargs)

    @patch("run.subprocess.run")
    def test_cli_failure_is_reported(self, execute):
        execute.return_value = subprocess.CompletedProcess([], 1, b"", b"guest unavailable")
        with self.assertRaisesRegex(RuntimeError, "guest unavailable"):
            run.call(["list"])

    @patch("run.call")
    def test_utf8_bom_json(self, call):
        call.return_value = b'\xef\xbb\xbf{"ok":true}'
        self.assertEqual(run.pull_json("Windows", "result.json"), {"ok": True})

    @patch("run.call")
    def test_incomplete_json_is_retried(self, call):
        call.return_value = b'{"ok":'
        self.assertIsNone(run.pull_json("Windows", "result.json"))

    @patch("run.call", side_effect=RuntimeError("file locked"))
    def test_locked_file_is_retried(self, call):
        self.assertIsNone(run.pull_json("Windows", "result.json"))

    @patch("run.call")
    def test_invalid_status_shape_is_reported(self, call):
        for value in [[], None, {}, {"ok": "false"}]:
            with self.subTest(value=value):
                call.return_value = json.dumps(value).encode()
                with self.assertRaisesRegex(RuntimeError, "Invalid guest status"):
                    run.pull_json("Windows", "result.json")

    @patch("run.call", side_effect=subprocess.TimeoutExpired("utmctl", 20))
    def test_file_transfer_timeout_is_retried(self, call):
        self.assertIsNone(run.pull_json("Windows", "result.json"))

    @patch("run.command")
    def test_invalid_process_is_rejected_before_guest_execution(self, command):
        with patch("sys.argv", ["run.py", "--vm", "Windows", "--process",
                                "CrypTool';bad", "--output", "unused.json"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                run.main()
        command.assert_not_called()

    def test_invalid_arguments_do_not_contact_guest(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            existing = Path(directory) / "existing.json"
            existing.touch()
            cases = [
                ["--timeout", "nan"], ["--timeout", "inf"],
                ["--timeout", "0"], ["--timeout", "241"],
                ["--pid", "0"], ["--command-id", "0"],
                ["--command-id", "65536"], ["--process", "CrypTool.exe"],
                ["--output", str(existing)],
                ["--output", str(Path(directory) / "missing" / "out.json")],
                ["--screenshot", str(output)],
            ]
            for extra in cases:
                with self.subTest(extra=extra), patch("run.command") as command:
                    argv = ["run.py", "--vm", "Windows", "--process", "CrypTool",
                            "--output", str(output), *extra]
                    with patch("sys.argv", argv), contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            run.main()
                    command.assert_not_called()

    def invoke(self, directory, statuses, *, screenshot=False, command_error=None):
        """Run the real host lifecycle with all VM access mocked."""
        output = Path(directory) / "result.json"
        image = Path(directory) / "screen.png"
        argv = ["run.py", "--vm", "Windows", "--process", "CrypTool",
                "--output", str(output)]
        if screenshot:
            argv += ["--screenshot", str(image)]
        with patch("sys.argv", argv), patch("run.shutil.which", return_value="utmctl"), \
                patch("run.command", side_effect=command_error) as command, \
                patch("run.call", return_value=b"not a PNG") as call, \
                patch("run.pull_json", side_effect=statuses), \
                contextlib.redirect_stderr(io.StringIO()), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                run.main()
            finally:
                self.commands = [entry.args[1] for entry in command.call_args_list]
                self.transfers = call.call_args_list
        return output, image

    def test_success_uploads_scripts_writes_result_and_deletes_task(self):
        with tempfile.TemporaryDirectory() as directory:
            result = {"ok": True, "title": "Test window"}
            output, image = self.invoke(directory, [{"ok": True}, result])
            self.assertEqual(json.loads(output.read_text()), result)
            self.assertFalse(image.exists())
            self.assertEqual(len(self.transfers), 3)
            self.assertTrue(all(x.args[0][:2] == ["file", "push"] for x in self.transfers))
            self.assertIn("schtasks /Delete", self.commands[-1])
            self.assertFalse(any("schtasks /End" in text for text in self.commands))

    def test_launcher_failure_ends_and_deletes_task(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "Guest launcher failed: no desktop"):
                self.invoke(directory, [{"ok": False, "error": "no desktop"}])
            self.assertIn("schtasks /End", self.commands[-2])
            self.assertIn("schtasks /Delete", self.commands[-1])
            self.assertFalse((Path(directory) / "result.json").exists())

    def test_helper_failure_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "Desktop helper failed: stale target"):
                self.invoke(directory, [{"ok": True}, {"ok": False, "error": "stale target"}])
            self.assertIn("schtasks /Delete", self.commands[-1])
            self.assertFalse((Path(directory) / "result.json").exists())

    def test_deadline_ends_and_deletes_task(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("run.time.monotonic", side_effect=[0, 91]):
                with self.assertRaisesRegex(TimeoutError, "deadline exceeded"):
                    self.invoke(directory, [])
            self.assertIn("schtasks /End", self.commands[-2])
            self.assertIn("schtasks /Delete", self.commands[-1])

    def test_delete_is_attempted_even_if_end_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            # mkdir, launch, end (fails), delete.
            errors = [None, None, RuntimeError("end failed"), None]
            with self.assertRaisesRegex(RuntimeError, "Guest launcher failed"):
                self.invoke(directory, [{"ok": False}], command_error=errors)
            self.assertIn("schtasks /Delete", self.commands[-1])

    def test_invalid_screenshot_is_rejected_without_writing_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "not a PNG"):
                self.invoke(directory, [{"ok": True}, {"ok": True}], screenshot=True)
            self.assertFalse((Path(directory) / "result.json").exists())
            self.assertFalse((Path(directory) / "screen.png").exists())
            self.assertIn("schtasks /Delete", self.commands[-1])


if __name__ == "__main__":
    unittest.main()
