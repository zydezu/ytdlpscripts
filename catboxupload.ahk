#Requires AutoHotkey v2.0
; Hotkey: Ctrl+Alt+T
^!t::
{
    pythonFile := "C:\Users\User\Downloads\ytdlp\Upload File to Catbox.py"
    pythonDir := "C:\Users\User\Downloads\ytdlp"

    Run 'cmd.exe /c cd /d "' pythonDir '" && python "' pythonFile '"', pythonDir
    WinWaitActive("ahk_exe cmd.exe")

    if ProcessExist("python.exe") {
        ProcessWaitClose("python.exe")
    }

    if WinExist("ahk_exe cmd.exe") {
        WinClose("ahk_exe cmd.exe")
    }
}