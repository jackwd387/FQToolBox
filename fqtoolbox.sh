echo "请在下面的弹出的窗口点击允许，完成后输入y并回车"
termux-setup-storage
sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.aliyun.com/termux/termux-packages-24 stable main@' $PREFIX/etc/apt/sources.list
sed -i 's@^\(deb.*games stable\)$@#\1\ndeb https://mirrors.aliyun.com/termux/game-packages-24 games stable@' $PREFIX/etc/apt/sources.list.d/game.list
sed -i 's@^\(deb.*science stable\)$@#\1\ndeb https://mirrors.aliyun.com/termux/science-packages-24 science stable@' $PREFIX/etc/apt/sources.list.d/science.list
pkg update
echo "安装python"
pkg install python -y
echo "python换源"
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
echo "安装依赖"
pip install requests
pip install edge-tts
pip install asyncio
echo "从github获取FQToolBox，此处可能需要科学上网"
curl -o FQToolBox.zip "https://codeload.github.com/jackwd387/FQToolBox/zip/refs/heads/main"
unzip -d ~/storage/downloads FQToolBox.zip
cd ~/storage/downloads/FQToolBox-main
python Menu.py
#c1rcle
#第一次写这种脚本，如有bug请谅解

