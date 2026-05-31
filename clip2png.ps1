# clip2png.ps1 — 把剪貼簿的圖片存成 PNG，並將「檔案路徑」放回剪貼簿
# 用途：Win+Shift+S 截圖後執行本腳本，再到 Claude Code 按 Ctrl+V 貼路徑即可。
# 原理：終端機/Claude Code 在 Windows 讀不到剪貼簿的點陣圖，但讀得到檔案路徑文字。
# 相容 PowerShell 7 與 Windows PowerShell 5.1（剪貼簿存取需 STA 執行緒）。

$dir = Join-Path $PSScriptRoot ".clip"
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$path = Join-Path $dir ("clip_{0:yyyyMMdd_HHmmss}.png" -f (Get-Date))

# 在 STA 執行緒的 runspace 內存取剪貼簿並存檔（pwsh 預設 MTA，無法直接讀剪貼簿圖片）
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

    # 1) PNG 格式優先：Snipaste / Chrome / 多數截圖工具以 PNG 放剪貼簿
    #    （ContainsImage 不認 PNG，會誤判沒有圖，所以要先抓這個；也能保留透明與正確色彩）
    if ($cb::ContainsData("PNG")) {
        $stream = $cb::GetData("PNG")
        if ($stream -is [System.IO.Stream]) {
            $img = [System.Drawing.Image]::FromStream($stream)
            $img.Save($p, [System.Drawing.Imaging.ImageFormat]::Png)
            $img.Dispose()
            return $true
        }
    }

    # 2) 一般點陣圖（CF_BITMAP/DIB）：Windows 內建 Win+Shift+S
    if ($cb::ContainsImage()) {
        $img = $cb::GetImage()
        $img.Save($p, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
        return $true
    }

    # 3) 剪貼簿是「圖檔的檔案路徑」（在檔案總管複製了圖片檔）
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
    Write-Host "剪貼簿裡沒有圖片。先用 Win+Shift+S 截圖，再跑一次。" -ForegroundColor Yellow
    exit 1
}

# 把「路徑」放回剪貼簿 → Ctrl+V 貼進 Claude Code 就是可讀的路徑
Set-Clipboard -Value $path
Write-Host "已儲存：$path" -ForegroundColor Green
Write-Host "路徑已複製到剪貼簿 → 到 Claude Code 按 Ctrl+V 貼上即可。" -ForegroundColor Cyan
