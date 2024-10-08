#!/bin/bash

if [ -z "$PREFIX" ] || [ ! -d "$PREFIX" ]; then
    echo "此脚本仅适用于 Termux 环境。请在 Termux 中运行哦ರ_ರ"
        exit 1
        fi

        echo "请在下面的弹出的窗口点击允许，不给权限报错别找我哦→_→"
        termux-setup-storage

        # 修改 Termux 软件源为清大镜像
        echo "更换 Termux 软件源为清大镜像♪～(´ε｀ )"
        sed -i 's@^\(deb.*stable main\)$@#\1\ndeb https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main stable main@' $PREFIX/etc/apt/sources.list
        # 更新 Termux 包管理器
        echo "更新软件包ing<(￣︶￣)>"
        pkg update -y

        # 安装 Python
        pkg install python -y
        # 配置 Python 的 pip 源
        echo "正在配置 Python 的 pip 源为清华大学镜像(・o・)"
        pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/

        # 安装所需的 Python 库
        echo "正在安装所需的Python库┐(´ー｀)┌"
        pip install requests edge-tts asyncio

        #下载并解压 FQToolBox 项目
        echo "正在从 GitHub 下载 FQToolBox，此处可能需要科学上网，快了快了←_←"
        curl -o FQToolBox.zip "https://codeload.github.com/jackwd387/FQToolBox/zip/refs/heads/main" || { echo "下载失败，请尝试使用科学上网(〒﹏〒)"; exit 1; }
            echo "正在解压 FQToolBox..."
                unzip -o -d ~/storage/downloads FQToolBox.zip
                # 进入解压目录并运行 FQToolBox
                cd ~/storage/downloads/FQToolBox-main || { echo "无法进入 FQToolBox 目录"; exit 1; }
                echo "all done，运行脚本(≧▽≦)"
                python Menu.py
                
