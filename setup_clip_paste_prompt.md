# 截圖一鍵貼進 Claude Code — 跨機器設定 Prompt

把下面「--- PROMPT 開始 ---」到「--- PROMPT 結束 ---」之間整段，貼給另一台 Windows 機器上的 Claude Code，它就會把整套工具建好並設定完成。

已內含踩過的雷：pwsh 的 STA 問題、Snipaste/Chrome 的 PNG 剪貼簿格式、winget 的 msstore 憑證錯、AutoHotkey v2 語法、可攜路徑。

---

--- PROMPT 開始 ---

你是一台 Windows 機器上的 Claude Code。幫我設定「截圖一鍵貼進 Claude Code」的工具。

【要解決的問題】
Windows 上 Claude Code 無法直接貼剪貼簿的截圖（已知 bug：終端機把 Ctrl+V 當純文字攔走，讀不到二進位圖）。
【原理】寫腳本把剪貼簿的圖存成 png 檔 → 把「檔案路徑(純文字)」放回剪貼簿（Claude Code 讀得到路徑）→ 用 AutoHotkey 綁熱鍵一鍵完成。

請依序執行：

1) 選一個資料夾（例如目前專案根目錄），在裡面建立下面兩個檔。**兩檔必須同一資料夾**（腳本用相對位置互找，路徑可攜）。

2) 建立 `clip2png.ps1`。重點：
   - 不要用 `Get-Clipboard -Format Image`（只在舊 Windows PowerShell 5.1 有；PowerShell 7 沒有）。
   - PowerShell 7 預設 MTA 讀不到剪貼簿圖，必須用 STA 執行緒 runspace。
   - 必須**先抓 PNG 格式**：Snipaste / Chrome 等把圖以 PNG 放剪貼簿，`ContainsImage()` 不認 PNG 會誤判「沒有圖」。下面版本三種格式都處理了。
   內容：

```powershell
# clip2png.ps1 — 把剪貼簿圖片存成 PNG，並把檔案路徑放回剪貼簿
$dir = Join-Path $PSScriptRoot ".clip"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$path = Join-Path $dir ("clip_{0:yyyyMMdd_HHmmss}.png" -f (Get-Date))
$ps = [PowerShell]::Create()
$rs = [RunspaceFactory]::CreateRunspace()
$rs.ApartmentState = 'STA'
$rs.Open()
$ps.Runspace = $rs
[void]$ps.AddScript({
    param($p)
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $cb = [System.Windows.Forms.Clipboard]
    # 1) PNG 格式優先（Snipaste / Chrome / 多數截圖工具）
    if ($cb::ContainsData("PNG")) {
        $stream = $cb::GetData("PNG")
        if ($stream -is [System.IO.Stream]) {
            $img = [System.Drawing.Image]::FromStream($stream)
            $img.Save($p, [System.Drawing.Imaging.ImageFormat]::Png)
            $img.Dispose()
            return $true
        }
    }
    # 2) 一般點陣圖 CF_BITMAP/DIB（Windows 內建 Win+Shift+S）
    if ($cb::ContainsImage()) {
        $img = $cb::GetImage()
        $img.Save($p, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
        return $true
    }
    # 3) 剪貼簿是圖檔的檔案路徑（在檔案總管複製了圖片檔）
    if ($cb::ContainsFileDropList()) {
        foreach ($f in $cb::GetFileDropList()) {
            if ($f -match '\.(png|jpg|jpeg|bmp|gif|webp)$') {
                Copy-Item -LiteralPath $f -Destination $p -Force
                return $true
            }
        }
    }
    return $false
}).AddArgument($path)
$ok = [bool]($ps.Invoke() | Select-Object -Last 1)
$ps.Dispose(); $rs.Close()
if (-not $ok) {
    Write-Host "剪貼簿裡沒有圖片。先用截圖工具截圖，再跑一次。" -ForegroundColor Yellow
    exit 1
}
Set-Clipboard -Value $path
Write-Host "已儲存：$path" -ForegroundColor Green
Write-Host "路徑已複製到剪貼簿 → 到 Claude Code 按 Ctrl+V 貼上即可。" -ForegroundColor Cyan
```

3) 建立 `clip_paste.ahk`（AutoHotkey v2 語法）：

```autohotkey
#Requires AutoHotkey v2.0
; 截圖後按 Ctrl+Alt+V：存檔→把路徑放回剪貼簿→自動貼進當前視窗
^!v:: {
    script := A_ScriptDir "\clip2png.ps1"
    exitCode := RunWait('pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "' script '"', , "Hide")
    if (exitCode = 0) {
        Send("^v")
    } else {
        ToolTip("剪貼簿沒有圖片，先截圖再試。")
        SetTimer(() => ToolTip(), -2500)
    }
}
```

4) 安裝 AutoHotkey v2：
   `winget install --id AutoHotkey.AutoHotkey -e --source winget --accept-source-agreements --accept-package-agreements --scope user`
   （加 `--source winget` 是為了避開 msstore 源在某些網路下的憑證錯誤。）

5) 啟動：`Start-Process "<上面那個資料夾>\clip_paste.ahk"`，確認工作列出現綠色 H 圖示。熱鍵 Ctrl+Alt+V 立即生效，**不需重開機**。

6) （可選，需使用者本人授權執行）開機自動啟動 — 把捷徑放進開機資料夾：
   `$s=(New-Object -ComObject WScript.Shell).CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\clip_paste.lnk"); $s.TargetPath="<資料夾>\clip_paste.ahk"; $s.Save()`

7) 提醒我把 `.clip/` 加進 .gitignore（截圖暫存）。

【測試】用任何截圖工具截圖（內建 Win+Shift+S 或 Snipaste 皆可）→ 點 Claude Code 輸入框 → 按 Ctrl+Alt+V → 應自動出現 `...\.clip\clip_xxxx.png` 路徑 → Enter。看得到圖就成功。

注意：用的是 pwsh（PowerShell 7）。若該機只有 Windows PowerShell 5.1，把 .ahk 裡的 `pwsh.exe` 改成 `powershell.exe`。

--- PROMPT 結束 ---
