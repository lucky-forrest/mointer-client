@echo off
echo 正在尝试推送代码到 GitHub...
echo.

:: 检查 git 状态
echo 1. 检查 git 状态...
git status
echo.

:: 尝试推送到 GitHub
echo 2. 正在推送代码...
git push origin master

:: 如果失败，显示可能的解决方案
if %errorlevel% neq 0 (
    echo.
    echo 推送失败！可能的解决方案：
    echo.
    echo 1. 检查网络连接：
    echo    ping github.com
    echo.
    echo 2. 如果使用代理，配置代理设置：
    echo    git config --global http.proxy http://proxy-address:port
    echo    git config --global https.proxy https://proxy-address:port
    echo.
    echo 3. 稍后重试：
    echo    git push origin master
    echo.
    echo 4. 检查 GitHub 状态：
    echo    https://www.githubstatus.com/
    echo.
) else (
    echo.
    echo ✅ 代码已成功推送到 GitHub！
)

pause