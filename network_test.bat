@echo off
echo 网络连接诊断工具
echo ==================
echo.

echo 1. 测试基本网络连接：
ping github.com -n 4
echo.

echo 2. 测试 HTTPS 连接：
curl -I --connect-timeout 10 https://github.com
echo.

echo 3. 测试 DNS 解析：
nslookup github.com
echo.

echo 4. 检查网络端口：
netstat -an | findstr ":443"
echo.

echo 5. 检查代理设置：
echo HTTP Proxy: %HTTP_PROXY%
echo HTTPS Proxy: %HTTPS_PROXY%
echo.

echo 6. Git 配置：
git config --global --get url."https://github.com/".insteadOf
git config --global --get http.proxy
git config --global --get https.proxy
echo.

pause