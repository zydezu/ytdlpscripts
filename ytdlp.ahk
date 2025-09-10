#Requires AutoHotkey v2.0
; Hotkey: Ctrl+Alt+U
^!u::
{
    ; Step 1: Copy the current URL
    A_Clipboard := "" ; Clear clipboard
    Send "^l"        ; Focus address bar
    Sleep 150
    Send "^c"        ; Copy URL
    ClipWait 1       ; Wait for clipboard to have content
    if (A_Clipboard = "")
    {
        MsgBox "No URL copied. Aborting."
        return
    }

    ; Step 2: Run Python script in an interactive cmd
    pythonFile := "C:\Users\User\Downloads\ytdlp\Auto Determine.py"
    pythonDir := "C:\Users\User\Downloads\ytdlp"

    Run 'cmd.exe /k cd /d "' pythonDir '" && python "' pythonFile '"', pythonDir
    WinWaitActive("ahk_exe cmd.exe")

    ; Step 3: Paste the URL into the console
    Sleep 100  ; Give Python time to start
    Send A_Clipboard
    Send "{Enter}"

    ; Step 4: Wait until python.exe process ends
    ProcessWaitClose("python.exe")

    ; Step 5: Close the CMD window
    WinClose("ahk_exe cmd.exe")
}
