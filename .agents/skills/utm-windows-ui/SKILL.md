---
name: utm-windows-ui
description: Inspects Windows desktop applications in UTM through the QEMU guest agent, PowerShell, UI Automation, and Win32 APIs. Use for Windows VM screenshots, dialog and menu inspection, or verified UI commands, including CrypTool.
---

# Windows desktop automation through UTM

## Prerequisites

- macOS with UTM running and `utmctl` on PATH.
- Windows guest with the QEMU guest agent running.
- A logged-in, unlocked Windows desktop. The target application must be open.
- Python 3 on the host and Windows PowerShell 5.1 in the guest; no third-party Python packages.
- Permission to execute scripts in the guest and create a temporary scheduled task.

## Architecture

The guest agent runs as SYSTEM in session 0. It cannot directly inspect the user's
desktop. Upload a PowerShell helper and launch it with a scheduled task whose
principal uses the logged-in user's interactive token. The helper runs in the
desktop session. No password is needed. Do not change execution policy globally.

Use UI Automation for accessible controls and dialog text. Older applications
may need Win32 APIs for menu enumeration and command invocation. Prefer these
over screen coordinates. Inspect the resulting controls and, when authorized,
a screenshot before claiming an operation succeeded. For document operations,
verify the saved artifact as well; a window title alone is not proof of success.

## Usage

Resolve script paths relative to this skill's directory. Host output paths must
be in an approved location. Screenshots are explicit opt-in because they capture
the entire guest desktop, potentially including unrelated applications.

```sh
python3 scripts/run.py --vm Windows --process CrypTool --output /approved/path/inspection.json
python3 scripts/run.py --vm Windows --process CrypTool --screenshot /approved/path/desktop.png --output /approved/path/inspection.json
```

The runner discovers the account owning the target process. It refuses multiple
matching desktop processes: supply `--pid` in that case. `--process` is a process
name without `.exe`. Do not hardcode the account, PID, window handle, or session.

To invoke a menu command, first inspect `menus` in the JSON output, confirm its
meaning and the current document, then use:

```sh
python3 scripts/run.py --vm Windows --process CrypTool --command-id 33005 --output /approved/path/entropy.json
```

`33005` is an example, not a portable identifier. Always rediscover IDs and
check `menus[].enabled`. `--command-id` changes application state and must stay
within the user's authorization. The helper rejects disabled main windows and
disabled/absent menu entries; it cannot verify the user's intended document.
Inspection does not click, type, or modify application documents.

Results include `ok`, target PID/session/title, `menus`, and `windows[].controls`
(type, name, automation ID, enabled state, class, handle). Output is capped at
250 controls per root and 2,000 characters per name; absence is not conclusive.
Handles are diagnostic and must be rediscovered before use. Menu actions wait
1.5 seconds before inspection, not until application completion. Inspect again
if a dialog is still loading. See [dialog workflows](references/dialogs.md)
when extending the runner beyond menu commands.

## Execution and results

- Upload UTF-8 `.ps1` files using `utmctl file push` (stdin).
- Invoke PowerShell through `cmd.exe /c` with absolute executable paths and
  `-NoProfile -NonInteractive -ExecutionPolicy Bypass -File`.
- Use an interactive, limited-privilege scheduled task for UI access.
- Do not trust empty stdout or a zero host exit code as guest success. In the
  tested setup execution returned before guest scripts completed.
- `--timeout` bounds result polling (default 90 seconds, range 1–240); individual
  CLI calls and cleanup add time. Never resubmit a UI action while waiting.
- Retrieve screenshots as binary through the CLI, not a text-only MCP result.
- Task cleanup is attempted on success/failure; the guest task also has a
  five-minute execution limit. Guest artifacts remain in the printed run
  directory. Inspect `cleanup.log` if cleanup is uncertain. Outputs may contain
  document text or keys; keep them in approved locations, not the repository.

## Safety and limitations

- Do not unlock Windows, bypass UAC, change security settings, install software,
  or operate another user's session without explicit approval.
- The helper is not a sandbox: it runs code as SYSTEM to register the task, then
  code as the desktop user. Only run trusted, reviewed scripts.
- Avoid elevated target applications; a limited helper may not control them.
- Avoid parallel runs targeting the same application.
- If dialogs or documents change unexpectedly between inspections, stop sending
  actions and check for another automation session or human interaction. Resume
  only from a freshly inspected state; do not dismiss unfamiliar dialogs blindly.
- UI Automation text may be incomplete or garbled for custom/legacy controls.
  Use screenshots and targeted Win32 inspection rather than treating it as truth.
- Modal dialogs may block commands. Inspect existing dialogs first.
- A posted menu message is not proof that the command completed. Review the
  resulting controls/screenshot. Slow commands may require another inspection.
- Desktop capture requires an active graphical desktop; locked/minimized or
  disconnected environments can produce blank or stale images.

## Troubleshooting

1. Check `utmctl list` and that guest-agent file transfer works.
2. Check the retained `launch.log`, `launch.json`, and `result.json` files.
3. Confirm the target process belongs to a logged-in desktop session, not 0.
4. Check Task Scheduler availability and permissions. The helper needs an
   interactive token; no desktop login means no interactive automation.
5. Do not assume PowerShell command-line quoting survives every layer. Prefer
   uploaded script files over inline scripts or deeply nested quotes.

For CrypTool menus, round trips, and alphabet/encoding pitfalls, read
[the CrypTool reference](references/cryptool.md).

## Tests

Host-only tests (do not contact the VM):

```sh
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
```

For a live smoke test, use the read-only inspection command above with fresh
host output paths. Verify `ok`, the expected session/title, menu entries, and the
PNG if capture was authorized. Test menu invocation only with authorization:
verify its resulting dialog, not just `postedCommand`. For dialog extensions,
test a delayed save and exact artifact verification. Host tests mock UTM and do
not validate PowerShell or Windows UI behavior.
