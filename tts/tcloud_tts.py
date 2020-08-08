# coding=UTF-8
import requests
import wave
import json
import base64
import time
import collections
import urllib
import base64
import hmac
import hashlib
import uuid
import os


TCLOUD_APP_ID = int(os.environ["TCLOUD_APP_ID"])
TCLOUD_SECRET_ID = os.environ["TCLOUD_SECRET_ID"]
TCLOUD_SECRET_KEY = os.environ["TCLOUD_SECRET_KEY"]
OUTPUT_PATH = "../output/audio"


def generate_sign(request_data):
    url = "tts.cloud.tencent.com/stream"
    sign_str = "POST" + url + "?"
    sort_dict = sorted(request_data.keys())
    for key in sort_dict:
        sign_str = sign_str + key + "=" + urllib.parse.unquote(str(request_data[key])) + '&'
    sign_str = sign_str[:-1]
    sign_bytes = sign_str.encode('utf-8')
    key_bytes = TCLOUD_SECRET_KEY.encode('utf-8')
    authorization = base64.b64encode(hmac.new(key_bytes, sign_bytes, hashlib.sha1).digest())
    return authorization.decode('utf-8')


def text2wav(content):
    request_data = {
        "Action": "TextToStreamAudio",
        "AppId": TCLOUD_APP_ID,

        #返回音频格式：Python SDK只支持pcm格式
        #pcm：返回二进制 pcm 音频，使用简单，但数据量大。
        "Codec": "pcm",
        "Expired": int(time.time()) + 3600,

        #模型类型，1：默认模型
        "ModelType": 1,  

        #主语言类型：
        #1：中文（默认）
        #2：英文
        "PrimaryLanguage": 1,

        #项目 ID，用户自定义，默认为0。
        "ProjectId": 0,

        #音频采样率：
        #16000：16k（默认）
        #8000：8k
        "SampleRate": 16000,
        "SecretId": TCLOUD_SECRET_ID,
        "SessionId": str(uuid.uuid1()),

        #语速，范围：[-2，2]，分别对应不同语速：
        #-2代表0.6倍
        #-1代表0.8倍
        #0代表1.0倍（默认）
        #1代表1.2倍
        #2代表1.5倍
        #输入除以上整数之外的其他参数不生效，按默认值处理。
        "Speed": 0,
        "Text": content,
        "Timestamp": int(time.time()),

        #音色：
        #0：亲和女声（默认）
        #1：亲和男声
        #2：成熟男声
        #3：活力男声
        #4：温暖女声
        #5：情感女声
        #6：情感男声
        "VoiceType": 5,

        #音量大小，范围：[0，10]，分别对应11个等级的音量，默认值为0，代表正常音量。没有静音选项。
        "Volume": 5, 
    }
    signature = generate_sign(request_data)
    # print(f"signature: {signature}")
    header = {
        "Content-Type": "application/json",
        "Authorization": signature
    }
    url = "https://tts.cloud.tencent.com/stream"

    # print(request_data)
    r = requests.post(url, headers=header, data=json.dumps(request_data), stream = True)
    # print(r)
    i = 1
    t = int(time.time() * 1000)
    output_file = os.path.join(OUTPUT_PATH, f"{t}.wav")
    wavfile = wave.open(output_file, 'wb')
    wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
    for chunk in r.iter_content(1000):
        if (i == 1) & (str(chunk).find("Error") != -1) :
            print(chunk)
            return ""
        i = i + 1
        wavfile.writeframes(chunk)
        
    wavfile.close()
    return output_file


if __name__ == "__main__":
    print(text2wav("返回音频格式：Python SDK只支持pcm格式"))

