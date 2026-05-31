#Requires AutoHotkey v2.0
; clip_paste.ahk — 截圖貼進 Claude Code 用的熱鍵
; 流程：Win+Shift+S 截圖 → Ctrl+Alt+V → 自動存檔+貼路徑
; 搭配同資料夾的 clip2png.ps1（把剪貼簿二進位圖 → png 檔 → 路徑放回剪貼簿）

; 熱鍵：Ctrl + Alt + V （想換鍵改下面這行，^=Ctrl !=Alt +=Shift #=Win）
^!v:: {
    script := A_ScriptDir "\clip2png.ps1"
    ; 等 PowerShell 跑完（路徑已進剪貼簿），取得結束碼
    exitCode := RunWait('pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "' script '"', , "Hide")
    if (exitCode = 0) {
        Send("^v")                       ; 貼上剛放進剪貼簿的「路徑」
    } else {
        ToolTip("剪貼簿沒有圖片，先按 Win+Shift+S 截圖再試。")
        SetTimer(() => ToolTip(), -2500) ; 2.5 秒後關掉提示
    }
}
