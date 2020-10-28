# -*- coding: UTF-8 -*-
'''
PyCharm
@Project ：AID2008第二阶段学习 
@File    ：ftp_server.py
@Author  ：
@Date    ：2020/10/22 上午11:24 
'''
"""
    服务端
"""
from socket import *
from multiprocessing import Process
from signal import *
import os, time

# 文件库位置
ilbrary = '/home/tarena/AID2008第二阶段学习/day10/'

# 下载位置
local_ilbrary = '/home/tarena/下载１/'

file = os.listdir(ilbrary)
# print(files)

POST = '0.0.0.0'
PORT = 8888
ADDR = (POST, PORT)


# 处理查看文件列表
def files(connfd):
    str_file = ''
    if file == []:
        connfd.send('无文件'.encode())
    for filename in file:

        str_file += filename + '\n'
    connfd.send(str_file.encode())
    time.sleep(0.1)
    connfd.send(b'##')


# 处理上传
def upload_file(connfd, fileaddr):
    filename = fileaddr.split('/')[-1]
    if os.path.exists(ilbrary + filename):
        connfd.send('上传文件已存在'.encode())
        return
    connfd.send('OK'.encode())
    up_file = open(ilbrary + filename, 'wb')
    while True:
        data = connfd.recv(1024)
        if data == b'##':
            break
        up_file.write(data)
    up_file.close()


# 处理下载
def download_file(connfd, filename):
    if os.path.exists(ilbrary + filename):
        file = open(ilbrary + filename, 'rb')
        if os.path.exists(local_ilbrary + filename):
            connfd.send('下载的文件重复'.encode())
            return
        else:
            down_file = open(local_ilbrary + filename, 'wb')
            while True:
                data = file.read(1024)
                down_file.write(data)
                if not data:
                    break
        connfd.send('下载成功'.encode())

        file.close()
        down_file.close()

    else:
        connfd.send('文件不存在'.encode())
        return


# 处理退出
def exits(connfd):
    connfd.send('拜拜'.encode())


# 处理请求
def request(connfd):
    while True:
        try:
            data = connfd.recv(1024)
            tmp = data.decode().split(' ', 1)
            print(tmp)
        except KeyboardInterrupt:
            return

        if not data:
            break
        if tmp[0] == 'LOOK':
            files(connfd)
        elif tmp[0] == 'UP':
            upload_file(connfd, tmp[1])
        elif tmp[0] == 'DOWN':

            download_file(connfd, tmp[1])

        elif tmp[0] == 'EXIT':
            exits(connfd)
    connfd.close()


# 启动函数
def main():
    socketed = socket()
    socketed.bind(ADDR)
    socketed.listen(5)
    signal(SIGCHLD,SIG_IGN)
    while True:
        try:
            connfd, addr = socketed.accept()
        except KeyboardInterrupt:
            socketed.close()
            return

        process = Process(target=request, args=(connfd,))
        Process.daemon=True
        process.start()


if __name__ == '__main__':
    main()
