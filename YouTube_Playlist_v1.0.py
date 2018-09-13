# 无需提前创建播放列表，直接下载youtube 播放列表（<100）


import requests
import re
from pytube import YouTube
import os
from pytube import Playlist
import time
import multiprocessing

# 定义参数
channel_name = '乒乓生活'  # change
pl = Playlist("https://www.youtube.com/watch?v=aeGBRfJG7Vs&list=PLnEUh5aDDkHAqYwZeS_Tk-11sV_e-FseO") # change
rows = len(pl.parse_links())

start_time = time.time()
download_path = os.getcwd() + '\\' + '2_download' + '\\' + channel_name


if not os.path.exists(download_path):
    os.mkdir(download_path)

# 增加unicodetoascii函数，去掉异常字符
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


# 定义youtube 函数
def youtube_download(a):
    yt = YouTube(a)
    stream = yt.streams.first()
    caption = yt.captions.get_by_language_code('en')
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    file_name = re.sub(rstr, '', yt.title)  # 去掉非法字符
    print(file_name)

    # 字幕不存在的处理方式
    if caption is not None:
        caption_text = caption.generate_srt_captions()
        caption_text = unicodetoascii(caption_text)
        if not os.path.exists(download_path + '\\' + file_name + '.srt'):
            f = open(download_path + '\\' + file_name + '.srt', 'wb')
            f.write(caption_text.encode())
            f.close()

    # 避免重复下载
    if not os.path.exists(download_path + '\\' + file_name + '.mp4'):
        stream.download(download_path + '\\')
        stream.on_complete()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=16)
    for x in range(0, rows):  # rows
        url_list = "https://www.youtube.com" + str(pl.parse_links()[x])
        pool.apply_async(youtube_download, (url_list,))
    pool.close()
    pool.join()
    print('Sub-process done')
    print(time.time() - start_time)
