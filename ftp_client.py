# -*- coding: UTF-8 -*-
'''
PyCharm
@Project ：AID2008第二阶段学习 
@File    ：ftp_client.py
@Author  ：
@Date    ：2020/10/22 上午11:25 
'''
"""
    客户端
"""

from socket import *
import sys, time

#服务器地址
ADDR = ('127.0.0.1', 8888)


# 文件列表
def file_list(socketed, msg):
    socketed.send(msg.encode())
    while True:
        data = socketed.recv(1024)
        print('文件列表：')
        if  data == b'##':
            return
        print(data.decode())


# 下载文件
def down_file(socketed):
    filename = input('要下载的文件名:')
    afreement = 'DOWN %s' % filename

    socketed.send(afreement.encode())
    data = socketed.recv(1024)
    if not data:
        return
    print(data.decode())




# 上传文件
def up_file(socketed):
    fileaddr = input('要上传的文件地址:')
    try:
        file = open(fileaddr, 'rb')

    except FileNotFoundError:
        print('文件不存在')
        return
    afreement = f'UP {fileaddr}'
    socketed.send(afreement.encode())
    data = socketed.recv(1024)

    if data == b"OK":
        while True:
            message = file.read(1024)
            if not message:
                break
            socketed.send(message)
        print('文件上传成功')
        file.close()
        time.sleep(0.1)
        socketed.send(b'##')
    else:
        print(data.decode())


# 退出
def sign_out(socketed, msg):
    socketed.send(msg.encode())
    data = socketed.recv(1024)
    if data.decode() == '拜拜':
        sys.exit('谢谢使用')




def main():
    socketed = socket()
    socketed.connect(ADDR)
    while True:
        print('--------功能选项--------')
        print('LOOK---UP---DOWN---EXIT')

        try:
            msg = input('请输入：')
            if not msg:
                break
        except KeyboardInterrupt:
            socketed.close()
            break

        if msg == 'LOOK':
            file_list(socketed, msg)
        elif msg == 'UP':
            up_file(socketed)
        elif msg == 'DOWN':
            down_file(socketed)
        elif msg == 'EXIT':
            sign_out(socketed, msg)
        else:
            print('请输入有效指令！')



if __name__ == '__main__':
    main()
