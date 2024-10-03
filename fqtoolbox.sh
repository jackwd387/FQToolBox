echo "请在下面的弹出的窗口点击允许"
termux-setup-storage
echo "修改镜像源，并更新软件包"
sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main stable main@' $PREFIX/etc/apt/sources.list
apt update && apt upgrade
echo "安装python"
pkg install python -y
echo "安装依赖"
pip install requests edge-tts asyncio
echo "从github获取FQToolBox，此处可能需要科学上网"
curl -o FQToolBox.zip "https://codeload.github.com/jackwd387/FQToolBox/zip/refs/heads/main"
unzip FQToolBox.zip
cd FQToolBox-main
python Menu.py
#c1rcle
#第一次写这种脚本，如有bug请谅解
