@echo off
setlocal enabledelayedexpansion
echo 正在自动重试推送代码到 GitHub...
echo.

:: 设置重试参数
set max_attempts=10
set delay_seconds=30
set attempt=1

:retry_loop
echo 尝试第 !attempt! 次...
echo 时间: %date% %time%
echo.

git push origin master
if %errorlevel% equ 0 (
    echo.
    echo ✅ 成功！代码已推送到 GitHub！
    goto end
)

echo.
echo 推送失败，等待 %delay_seconds% 秒后重试...
timeout /t %delay_seconds% /nobreak >nul

set /a attempt+=1
if !attempt! leq %max_attempts% (
    goto retry_loop
)

echo.
echo ❌ 已达到最大重试次数（%max_attempts% 次）
echo.
echo 可能的解决方案：
echo 1. 检查网络连接
echo 2. 稍后手动重试：git push origin master
echo 3. 检查防火墙设置
echo 4. 尝试使用 VPN

:end
pause