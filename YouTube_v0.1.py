# Evan
# 2018.9.7
# 针对单个youtube包含字幕文件下载
# 增加unicodetoascii函数，去掉异常字符


import requests
import re
from pytube import YouTube
import os


# 定义参数
channel_name = 'sample'  # change
download_path = os.getcwd() + '\\' + '2_download' + '\\' + channel_name

if not os.path.exists(download_path):
    os.mkdir(download_path)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}


def unicodetoascii(text):
    uni2ascii = {
        ord(b'\xe2\x80\x99'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\x9c'.decode('utf-8')): ord('"'),
        ord(b'\xe2\x80\x9d'.decode('utf-8')): ord('"'),
        ord(b'\xe2\x80\x9e'.decode('utf-8')): ord('"'),
        ord(b'\xe2\x80\x9f'.decode('utf-8')): ord('"'),
        ord(b'\xc3\xa9'.decode('utf-8')): ord('e'),
        ord(b'\xe2\x80\x9c'.decode('utf-8')): ord('"'),
        ord(b'\xe2\x80\x93'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\x92'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\x94'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\x94'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\x98'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\x9b'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\x90'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\x91'.decode('utf-8')): ord('-'),
        ord(b'\xe2\x80\xb2'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\xb3'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\xb4'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\xb5'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\xb6'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x80\xb7'.decode('utf-8')): ord("'"),
        ord(b'\xe2\x81\xba'.decode('utf-8')): ord("+"),
        ord(b'\xe2\x81\xbb'.decode('utf-8')): ord("-"),
        ord(b'\xe2\x81\xbc'.decode('utf-8')): ord("="),
        ord(b'\xe2\x81\xbd'.decode('utf-8')): ord("("),
        ord(b'\xe2\x81\xbe'.decode('utf-8')): ord(")"),

    }
    return text.translate(uni2ascii).encode('ascii', 'ignore').decode('utf-8')


yt = YouTube("https://www.youtube.com/watch?v=n1kYu5sW76o")

stream = yt.streams.first()
caption = yt.captions.get_by_language_code('en')
caption_text = caption.generate_srt_captions()
caption_text = unicodetoascii(caption_text)
rstr = r"[\/\\\:\*\?\"\<\>\|]"
file_name = re.sub(rstr, '', yt.title)  # 去掉非法字符
print(file_name)
r = requests.get(yt.thumbnail_url, headers=headers)
f = open(download_path + '\\' + file_name +'.jpg', 'wb')
f.write(r.content)
f.close()

f = open(download_path + '\\' + file_name + '.srt', 'wb')
f.write(caption_text.encode())
f.close()

stream.download(download_path + '\\')
print('finished')
