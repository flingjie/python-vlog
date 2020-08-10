# -*- encoding: utf-8 -*-
"""
@File    :   main
@Time    :   2020/8/10 7:36 上午
@Author  :   Fan Lingjie 
@Version :   1.0
@Contact :   fanlingjie@laiye.com
"""
from generator import generate_vlog


if __name__ == "__main__":
    filename = "data/scripts/test.md"
    output_path = "output/test.mp4"
    generate_vlog(filename, output_path)
