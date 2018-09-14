from bypy import ByPy
import os
import time

channel_name = 'PHP Tutorials'  # change wow_english Business English Pod
start_time = time.time()
download_path = os.getcwd() + '\\' + '2_download' + '\\' + channel_name
print(download_path)
bp = ByPy()
bp.mkdir(remotepath='youtube')  #在网盘中新建目录
bp.syncup(download_path,'youtube') #将本地文件上传到百度云盘中
print('上传完毕！')
print((time.time() - start_time) / 60)