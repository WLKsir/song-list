@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"

set "PATH=D:\AI\Tools\nodejs;%PATH%"
set "STAGE=D:\AI\Temp\songlist-deploy"
set "WRANGLER_HOME=D:\AI\Temp\wrangler"
set "HOME=D:\AI\Temp\wrhome"
set "npm_config_cache=D:\AI\Tools\npm-cache"

echo.
echo [1/3] 暂存网页文件（不含 android 工程）...
if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%"
for %%F in (index.html wheel.html xlsx.full.min.js bg.jpg) do (
    if exist "%%F" copy /y "%%F" "%STAGE%\" >nul
)
copy /y "最新歌单.xlsx" "%STAGE%\" >nul

echo.
echo [2/3] 上传到 Cloudflare Pages ...
call npx -y wrangler@latest pages deploy "%STAGE%" --project-name=mml-songlist --branch=main
if errorlevel 1 (
    echo.
    echo [失败] 部署失败。若提示未登录，见部署说明 4.2 节。
    pause
    exit /b 1
)

echo.
echo [3/3] 完成，约 1 分钟后线上生效：https://mml-songlist.pages.dev/
pause
