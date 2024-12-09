#!/bin/bash

if [ -z "$PREFIX" ] || [ ! -d "$PREFIX" ]; then
    echo "此脚本仅适用于 Termux 环境。请在 Termux 中运行哦ರ_ರ"
        exit 1
        fi

        echo "请在下面的弹出的窗口点击允许，不给权限报错别找我哦→_→"
        termux-setup-storage
        # 更新 Termux 包管理器
        echo "更新软件包ing<(￣︶￣)>"
        apt update && apt upgrade -y
        #安装openssl(不安装的话总是会出一些奇奇怪怪的bug)
        pkg install openssl -y
        # 安装 Python
        pkg install python -y
        # 安装所需的 Python 库
        echo "正在安装所需的Python库┐(´ー｀)┌"
        pip install requests edge-tts asyncio tqdm

        #下载并解压 FQToolBox 项目
        echo "正在从 GitHub 下载 FQToolBox,快了快了←_←"
        curl -o FQToolBox.zip "https://github.com/jackwd387/FQToolBox/archive/refs/heads/main.zip" || { echo "下载失败(〒﹏〒)"; exit 1; }
            echo "正在解压 FQToolBox..."
                unzip -o -d ~/storage/downloads FQToolBox.zip
                # 进入解压目录并运行 FQToolBox
                cd ~/storage/downloads/FQToolBox-main || { echo "无法进入 FQToolBox 目录"; exit 1; }
                sed -i '$ a\alias fqtoolbox="cd ~/storage/downloads/FQToolBox-main && python ./Menu.py"' ~/.bashrc
                #环境变量
                echo "all done，运行脚本(≧▽≦)"
                python Menu.py
                
