# Evan G
# 多线程下载CSV中的youtube播放列表，前提条件通过其他python完成播放列表的CSV导出
# 有字幕，有视频
# 无效验下载完整性，todo

import re
import os
from pytube import YouTube
import time
import multiprocessing
import pandas as pd
import requests

# 定义参数
channel_name = 'wow_english'  # change
start_time = time.time()
source_Path = os.getcwd() + '\\' + '1_source_link'
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

def do_load_media(url, path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            print(content_length)
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)

# 定义下载 功能
def youtube_download_check(a):
    print(a)
    yt = YouTube(a)
    stream = yt.streams.first()
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    file_name = re.sub(rstr, '', yt.title)  # 去掉非法字符
    print(file_name)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(download_path + '\\' + file_name + '.mp4'):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(download_path + '\\' + file_name + '.mp4')
                print(headers['Range'])
            res = stream.filesize
            print(res)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)



# 字幕不存在的处理方式
    if caption is not None:
        caption_text = caption.generate_srt_captions()
        caption_text = unicodetoascii(caption_text)
        if not os.path.exists(download_path + '\\'+file_name + '.srt'):
            f = open(download_path + '\\' + file_name + '.srt', 'wb')
            f.write(caption_text.encode())
            f.close()

# 避免重复下载
    if not os.path.exists(download_path + '\\' + file_name + '.mp4'):
        stream.download(download_path + '\\')



# 定义下载 功能
def youtube_download(a):
    print(a)
    yt = YouTube(a)
    stream = yt.streams.get_by_itag('137')
    caption = yt.captions.get_by_language_code('en')
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    file_name = re.sub(rstr, '', yt.title)  # 去掉非法字符
    print(file_name)

# 字幕不存在的处理方式
    if caption is not None:
        caption_text = caption.generate_srt_captions()
        caption_text = unicodetoascii(caption_text)
        if not os.path.exists(download_path + '\\'+file_name + '.srt'):
            f = open(download_path + '\\' + file_name + '.srt', 'wb')
            f.write(caption_text.encode())
            f.close()

# 避免重复下载
    if not os.path.exists(download_path + '\\' + file_name + '.mp4'):
        stream.download(download_path + '\\')



# 定义下载 功能
def youtube_download_audio(a):
    print(a)
    yt = YouTube(a)
    stream = yt.streams.get_by_itag('140')
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    file_name = re.sub(rstr, '', yt.title)  # 去掉非法字符
    print(file_name)
# 避免重复下载
    if not os.path.exists(download_path + '\\' + file_name + '.mp3'):
        stream.download(download_path + '\\')

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=16)

    df = pd.read_csv(source_Path + '\\' + channel_name + '.csv')
    url_list = df['URL'].values
    rows = len(df['URL'])
    print(rows)

    for x in range(0, 20):  # rows
        url_full = "https://www.youtube.com" + str(url_list[x])
        pool.apply_async(youtube_download_audio, (url_full,))
    pool.close()
    pool.join()
    print('Sub-process done')
    print(time.time() - start_time)
