# -*- encoding: utf-8 -*-
"""
@File    :   md2dict
@Time    :   2020/8/9 4:38 下午
@Author  :   Fan Lingjie 
@Version :   1.0
@Contact :   fanlingjie@laiye.com
"""


def parse(filename):
    result = {
        "title": "",
        "content": []
    }
    with open(filename) as f:
        lines = f.readlines()
    s = lines[0]
    link = s[s.find("(") + 1:s.find(")")]
    text = s[s.find("[") + 1:s.find("]")]
    result['title'] = {
        "text": text,
        "link": link
    }

    # 开始解析内容部分
    content = list(filter(lambda x: x.strip() != '', lines[1:]))
    print(content)
    i = 0
    link = ""
    text = ""
    while i < len(content):
        s = content[i]
        print(f"content: {s}")
        if s.find("(") > 0:
            print(f"find link!")
            link = s[s.find("(") + 1:s.find(")")]
            text = s[s.find("[") + 1:s.find("]")]
            i += 1
            if link.endswith(".mp4") or link.endswith(".gif"):
                result['content'].append({
                    'link': link,
                    'text': text,
                    'type': 'video'
                })
        else:
            print("handle nonlink")
            subtitle = content[i].strip()
            i += 1
            result['content'].append({
                'link': link,
                'text': text,
                'subtitle': subtitle,
                'type': 'image'
            })
    return result


if __name__ == "__main__":
    filname = "data/scripts/test.md"
    res = parse(filname)
    print(res)
