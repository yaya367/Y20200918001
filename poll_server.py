"""
    poll方法IO多路复用并发模型
"""
from socket import *
from select import *

#创建监听套接字，作为初始监听对象
sockfd=socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(5)

#设置非阻塞
sockfd.setblocking(False)

#创建poll对象
p=poll()

#创建查找字典,与关注的IO一致
map={sockfd.fileno():sockfd}

#关注监听套接字
p.register(sockfd,POLLIN)

#循环监控注册的IO
while True:
    events=p.poll()  #[(1,2)]
    #循环遍历就绪的IO,分情况
    for fd,event in events:
        if fd==sockfd.fileno():
            connfd,addr=map[fd].accept()
            #关注连接套接字
            connfd.setblocking(False)
            p.register(connfd,POLLIN)
            #关注IO要与字典一致
            map[connfd.fileno()]=connfd #添加
        elif event==POLLIN:
            #某个客户端发来消息
            data=map[fd].recv(1024)
            #客户端结束
            if not data:
                p.unregister(fd) #取消关注
                map[fd].close()
                del map[fd] #移除 与IO保持一致
                continue #for循环遍历后面的IO
            print(data.decode())
            p.unregister(fd)
            p.register(fd,POLLOUT) #关注写
        elif event==POLLOUT:
            map[fd].send(b'OK')
            p.unregister(fd)
            p.register(fd,POLLIN)




