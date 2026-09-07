@echo off
chcp 65001
echo ======================================
echo      歌单网页服务启动工具（带Serveo穿透）
echo 本地地址：http://127.0.0.1:8000/index.html
echo 等待隧道建立后查看控制台公网链接
echo ======================================
echo 正在启动Web服务...
D:
cd /d D:\1.x\歌单\歌单网页
:: 启动网页服务（新开窗口运行，不阻塞穿透）
start "Web服务" cmd /c "python -m http.server 8000"
:: 打开本地页面
start http://127.0.0.1:8000/index.html
echo 正在建立外网隧道，请等待输出公网地址...
echo.
echo 提示：首次连接输入 yes 确认
ssh -R 80:localhost:8000 serveo.net
echo.
echo 隧道已断开！按任意键退出窗口
pause>nul