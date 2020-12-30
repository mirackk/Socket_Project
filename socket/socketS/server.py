# socket传递的都是bytes类型的数据，字符串需要先转换一下，string.encode()即可
# 另一端接收到的bytes数据想转换成字符串，只要bytes.decode()一下就可以
import socket
import os
import shutil
import _thread

ip_port = ('127.0.0.1', 6969)
path = os.getcwd() + "/sdata"


def link_handler(index, sk, conn, addr):
    try:
        print("服务器开始接收来自[%s:%s]的请求...." % (addr[0], addr[1]))
        conn.settimeout(200)
        conn.sendall("success in connection".encode())
        while True:
            client_data = conn.recv(1024).decode()
            if not client_data:  # 客户端已断开
                print("客户端断开连接")
                break

            cmd, filename = client_data.split(" ")
            # 查看信息
            if cmd == "view":
                flag = 0
                files = os.listdir(path)
                for file in files:
                    if file == filename:
                        flag = 1
                        conn.send("yes".encode())
                        f = open(path + '/' + filename + '/' + filename +
                                 '.txt', "rb")  # 我自己整的极为丑陋的东西
                        for line in f:
                            conn.send(line)  # 发送数据
                            print(line)
                        f.close()
                        f = open(
                            path + '/' + filename + '/' + filename + '.jpg',
                            "rb").read()
                        # print("read the jpg")
                        conn.send(f)
                        # print("send the jpg")
                if (flag == 0):
                    print("没有这个学号的学生")
                    conn.send("no".encode())
            # 删除
            if cmd == "delete":
                print("开始删除")
                flag = 0
                files = os.listdir(path)
                for file in files:
                    if file == filename:
                        flag = 1
                        dir = path + '/' + filename
                        shutil.rmtree(dir)
                        conn.send('删除完成'.encode())
                if (flag == 0):
                    print("没有这个学号的学生")
                    conn.send('删除失败，没有这个学号的学生'.encode())
            # 增加
            if cmd == "add":
                flag = 0
                files = os.listdir(path)
                for file in files:  # 查找学生是否存在
                    if file == filename:
                        flag = 1
                        conn.send("no".encode())
                if (flag == 0):  # 不存在学号则可以增加
                    conn.send("yes".encode())
                    name = conn.recv(1024).decode()
                    pic = conn.recv(1024 * 1024)
                    dir = path + '/' + filename
                    if not os.path.exists(dir):
                        os.mkdir(dir)

                    ftxt = open(
                        path + '/' + filename + '/' + filename + '.txt', "w")
                    ftxt.write(filename)
                    ftxt.write('\n' + name)
                    ftxt.close()

                    fjpg = open(
                        path + '/' + filename + '/' + filename + '.jpg', "wb")
                    fjpg.write(pic)
                    fjpg.close()
                    conn.send("success".encode())
    except socket.timeout:
        print('time out')
        conn.send("failed in connect, please try again".encode())

    print("closing connection %d" % index)  # 当一个连接监听循环退出后，连接可以关掉
    conn.close()  # 关闭连接
    _thread.exit()  # 关闭进程


if __name__ == "__main__":
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.bind(ip_port)
    sk.listen(5)

    print('启动socket服务，等待客户端连接...')
    index = 0  # index这里有个小逻辑问题，假如同一个cli连进去又退出，20次就无了
    # 并且我没有设置服务端的关闭程序，就是不能通过cli关闭server，只能server自己关闭
    while True:
        conn, address = sk.accept()
        index += 1
        _thread.start_new_thread(link_handler, (index, sk, conn, address))
        if index > 20:
            break
    print("服务器运行结束")
    sk.close()
