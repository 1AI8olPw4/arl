#!/usr/bin/env python3
"""
ARL命令行工具入口文件
"""
import os
import sys

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def print_banner():
    """打印艺术字和版本信息"""
    banner = r"""
    ___    ____  __    ___           _ ______          __    
   /   |  / __ \/ /   /   |  ____  (_)_  __/___  ____/ /____
  / /| | / /_/ / /   / /| | / __ \/ / / / / __ \/ __  / ___/
 / ___ |/ _, _/ /___/ ___ |/ /_/ / / / / / /_/ / /_/ (__  ) 
/_/  |_/_/ |_/_____/_/  |_/ .___/_/ /_/  \____/\__,_/____/  
                         /_/                                  
    """
    version_info = """
    Asset Reconnaissance Light API Tools v1.0.0
    Author: Your Name
    Github: https://github.com/your-repo/arl
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + version_info + Style.RESET_ALL)

from colorama import init, Fore, Style
from cli import main

if __name__ == '__main__':
    init()  # 初始化colorama
    
    # 如果是帮助命令，显示banner
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print_banner()
    
    exit(main()) 