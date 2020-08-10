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
    title = lines[0].strip('#').strip()
    result['title'] = title
    content = list(filter(lambda x: x.strip() != '', lines[1:]))
    print(content)
    i = 0
    while i < len(content):
        s = content[i]
        link = s[s.find("(")+1:s.find(")")]
        i += 1
        if link.endswith(".mp4"):
            text = s[s.find("[")+1:s.find("]")]
            result['content'].append({
                'link': link,
                'text': text,
                'type': 'video'
            })
        else:
            text = content[i].strip()
            i += 1
            result['content'].append({
                'link': link,
                'text': text,
                'type': 'image'
            })
    return result


if __name__ == "__main__":
    filname = "data/scripts/test.md"
    res = parse(filname)
    print(res)