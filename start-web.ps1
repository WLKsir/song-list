$port = 8088
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://127.0.0.1:$port/")
$listener.Start()
Write-Host "✅ 网页服务启动：http://127.0.0.1:$port"
Write-Host "网页目录：$(Get-Location)"
Write-Host "按 Ctrl+C 关闭服务"

while ($listener.IsListening) {
    try{
        $ctx = $listener.GetContext()
        $req = $ctx.Request
        $res = $ctx.Response
        $filePath = Join-Path (Get-Location) $req.Url.LocalPath.TrimStart('/')
        if (Test-Path $filePath -PathType Container){
            $filePath = Join-Path $filePath "index.html"
        }
        if (Test-Path $filePath){
            $data = [System.IO.File]::ReadAllBytes($filePath)
            $res.ContentLength64 = $data.Length
            $res.OutputStream.Write($data,0,$data.Length)
        }else{
            $res.StatusCode = 404
            $msg = [Text.Encoding]::UTF8.GetBytes("404 Not Found")
            $res.OutputStream.Write($msg,0,$msg.Length)
        }
        $res.Close()
    }catch{}
}