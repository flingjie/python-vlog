# -*- encoding: utf-8 -*-
"""
@File    :   main
@Time    :   2020/8/10 7:36 上午
@Author  :   Fan Lingjie 
@Version :   1.0
"""
from generator import generate_vlog


if __name__ == "__main__":
    # filename = "/Users/walker/Movies/视频号/常用帮助函数.md"
    filename = "data/example.md"
    output_path = "output"
    generate_vlog(filename, output_path)
