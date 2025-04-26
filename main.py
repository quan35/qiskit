#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
量子游戏集合 - 应用程序入口
"""

import tkinter as tk
import os
import sys

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from ui.main_window import QuantumGameApp
except ImportError as e:
    print(f"错误: 无法导入 QuantumGameApp - {e}")
    print("请确保项目结构正确，并且 ui/main_window.py 文件存在。")
    sys.exit(1)

def main():
    """主函数，启动图形用户界面"""
    try:
        root = tk.Tk()
        app = QuantumGameApp(root)
        root.mainloop()
    except tk.TclError as e:
        print(f"\n错误: 无法启动图形界面 - {e}")
        print("您的系统可能缺少必要的图形库或 Tkinter 支持未正确安装。")
        print("请检查您的 Python 环境和 Tkinter 安装。")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生意外错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()