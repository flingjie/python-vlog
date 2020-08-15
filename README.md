### Python for vlog

本项目尝试用Python从一个文本文件中自动生成视频格式的vlog

[思路及实现原理](https://mp.weixin.qq.com/s/3bD_ZgypBVgF4q0F3nj8gw)

### 使用方法

1. 更新.env文件中腾讯tts接口配置,使用source .env加载配置
2. 参照data/exmaple.md文件编写markdown内容
3. 更新main.py文件中的输入文件
4. 运行python main.py命令生成视频,默认在output文件夹下