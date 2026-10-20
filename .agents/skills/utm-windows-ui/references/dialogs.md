# Dialog actions and artifact verification

The runner only inspects UI and posts menu commands. For dialog workflows,
extend a reviewed helper narrowly; preserve process/session checks, limited
interactive execution, unique run directories, result publication, and cleanup.
Parameterize paths instead of copying a one-off script with fixed handles.

## Discover → act once → verify

1. Inspect the active document and modal dialogs. Scope searches to the target
   process and expected dialog; require one enabled match.
2. Prefer UI Automation value/invoke patterns. Legacy controls may appear as
   `ControlType.Pane` with no usable pattern. Inspect their native handles and
   enumerate native children, recording class, control ID, and text before using
   `WM_SETTEXT` or posting `WM_COMMAND` to the verified dialog.
3. Read back entered values before confirming. Open and Save As can use
   different layouts; rediscover handles/IDs rather than replaying them.
4. Confirm once and poll for the expected state with a bounded deadline. A
   timeout means "not verified"; inspect again before retrying the action.

`EnumChildWindows(mainWindow)` excludes owned top-level modal dialogs. Also
inspect the process's UI Automation roots/descendants, then enumerate the native
children of the actual dialog. Incomplete UI Automation output is not evidence
that no dialog exists.

## Wait for saved output

Choose a fresh path and refuse overwrites **before** invoking Save. After that
single action, poll for a readable file rather than sleeping a fixed interval:

```powershell
# $path is the expected new output; 30 seconds is an example workflow budget.
$deadline = [DateTime]::UtcNow.AddSeconds(30)
$bytes = $null
do {
    try {
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $bytes = [System.IO.File]::ReadAllBytes($path)
            break
        }
    } catch [System.IO.IOException] {
        # Retry while the application's exclusive lock is held.
    }
    Start-Sleep -Milliseconds 250
} while ([DateTime]::UtcNow -lt $deadline)
if ($null -eq $bytes) { throw "Output not verified before deadline: $path" }
```

Readability is not a completion signal. Also verify the picker closed and the
application finished, then validate expected contents/length. Streamed outputs
need an application completion signal; stable size alone is insufficient. Keep
the overall helper/task deadline longer than the workflow's polling budget.

## Verify document round trips

Use explicit encoding with no implicit newline for test input. Save transformed
and recovered output separately through the application. Custom-editor text
reads can be garbled; compare the saved bytes instead:

```powershell
$original = [System.IO.File]::ReadAllBytes($originalPath)
$recovered = [System.IO.File]::ReadAllBytes($recoveredPath)
$match = [Convert]::ToBase64String($original) -ceq [Convert]::ToBase64String($recovered)
if (!$match) { throw 'Round-trip byte comparison failed' }
```

For small test files this is an exact comparison, including encoding and
newlines. Record the match, lengths, transformation settings, and artifact paths
in verification JSON. Use only public test keys/data in encryption examples.
A matching round trip proves recovery, not algorithm conformance or security.
