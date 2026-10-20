param([Parameter(Mandatory=$true)][string]$RunDir)
$ErrorActionPreference = 'Stop'
try {
    $request = Get-Content -Raw -LiteralPath "$RunDir\request.json" | ConvertFrom-Json
    $target = Get-Content -Raw -LiteralPath "$RunDir\target.json" | ConvertFrom-Json
    $session = [System.Diagnostics.Process]::GetCurrentProcess().SessionId
    if ($session -ne $target.session) { throw 'Helper is not in the target desktop session.' }
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes
    Add-Type -TypeDefinition @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class UTMDesktop {
    [DllImport("user32.dll")] public static extern IntPtr GetMenu(IntPtr hwnd);
    [DllImport("user32.dll")] public static extern int GetMenuItemCount(IntPtr menu);
    [DllImport("user32.dll")] public static extern IntPtr GetSubMenu(IntPtr menu, int pos);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetMenuString(IntPtr menu, uint item, StringBuilder text, int max, uint flags);
    [DllImport("user32.dll")] public static extern uint GetMenuItemID(IntPtr menu, int pos);
    [DllImport("user32.dll")] public static extern uint GetMenuState(IntPtr menu, uint item, uint flags);
    [DllImport("user32.dll")] public static extern bool IsWindowEnabled(IntPtr hwnd);
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr hwnd, uint msg, IntPtr w, IntPtr l);
}
'@
    function Read-Menu([IntPtr]$Menu, [string]$Prefix, [int]$Depth = 0) {
        if ($Depth -gt 12) { return }
        for ($i = 0; $i -lt [UTMDesktop]::GetMenuItemCount($Menu); $i++) {
            $text = New-Object System.Text.StringBuilder 512
            [void][UTMDesktop]::GetMenuString($Menu, $i, $text, 512, 1024)
            $path = $Prefix + '/' + $text.ToString()
            $id = [UTMDesktop]::GetMenuItemID($Menu, $i)
            $state = [UTMDesktop]::GetMenuState($Menu, $i, 1024)
            @{ id = [long]$id; path = $path; enabled = (($state -band 3) -eq 0) }
            $sub = [UTMDesktop]::GetSubMenu($Menu, $i)
            if ($sub -ne [IntPtr]::Zero) { Read-Menu $sub $path ($Depth + 1) }
        }
    }
    $process = Get-Process -Id $target.pid
    if ($process.SessionId -ne $session -or $process.ProcessName -ne $request.process) {
        throw 'Target process identity changed.'
    }
    $handle = $process.MainWindowHandle
    if ($handle -eq [IntPtr]::Zero) { throw 'Target has no accessible main window.' }
    $menus = @(Read-Menu ([UTMDesktop]::GetMenu($handle)) '')
    if ($null -ne $request.commandId) {
        if (![UTMDesktop]::IsWindowEnabled($handle)) {
            throw 'Main window is disabled, possibly by a modal dialog. Inspect before acting.'
        }
        if (!($menus | Where-Object { $_.id -eq $request.commandId -and $_.enabled })) {
            throw 'Requested command ID is absent or disabled in the current main menu.'
        }
        if (![UTMDesktop]::PostMessage($handle, 273, [IntPtr]([int]$request.commandId), [IntPtr]::Zero)) {
            throw 'Posting WM_COMMAND failed.'
        }
        Start-Sleep -Milliseconds 1500
    }
    $condition = New-Object System.Windows.Automation.PropertyCondition `
        ([System.Windows.Automation.AutomationElement]::ProcessIdProperty), ([int]$target.pid)
    $roots = [System.Windows.Automation.AutomationElement]::RootElement.FindAll(
        [System.Windows.Automation.TreeScope]::Children, $condition)
    $windows = @(foreach ($root in $roots) {
        $controls = @($root.FindAll([System.Windows.Automation.TreeScope]::Descendants,
            [System.Windows.Automation.Condition]::TrueCondition) | Select-Object -First 250 |
            ForEach-Object {
                try {
                    $current = $_.Current
                    $name = $current.Name
                    if ($name.Length -gt 2000) { $name = $name.Substring(0, 2000) }
                    @{ type = $current.ControlType.ProgrammaticName; name = $name;
                       automationId = $current.AutomationId; enabled = $current.IsEnabled;
                       className = $current.ClassName; handle = $current.NativeWindowHandle }
                } catch { @{ error = 'Control disappeared during inspection.' } }
            })
        @{ title = $root.Current.Name; controls = $controls }
    })
    if ($request.screenshot) {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
        $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        try {
            $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bitmap.Size)
            $bitmap.Save("$RunDir\screen.png", [System.Drawing.Imaging.ImageFormat]::Png)
        } finally { $graphics.Dispose(); $bitmap.Dispose() }
    }
    $result = @{ ok = $true; pid = $target.pid; session = $session;
        title = $process.MainWindowTitle; menus = $menus; windows = $windows;
        postedCommand = $request.commandId; screenshot = [bool]$request.screenshot;
        timestamp = (Get-Date).ToString('o') }
} catch {
    $result = @{ ok = $false; error = ($_ | Out-String) }
}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath "$RunDir\result.pending.json" -Encoding UTF8
Move-Item -LiteralPath "$RunDir\result.pending.json" -Destination "$RunDir\result.json"
