"""
    select IO多路复用并发模型
    重点代码！！！！

"""
from select import select
from socket import *

#创建监听套接字，作为初始监控IO对象
sockfd=socket()#创建tcp套接字
sockfd.bind(('0.0.0.0',8888)) #绑定地址
sockfd.listen(5) #设置为监听套接字

#设置为非阻塞状态
sockfd.setblocking(False)

#设置关注列表
rlist=[sockfd] #关注监听套接字
wlist=[]
xlist=[]

#循环监控关注IO
while True:
    rs,ws,xs=select(rlist,wlist,xlist)
    #遍历返回值（IO就绪）列表,分情况处理
    for r in rs:
        if r is sockfd:
            connfd, addr = r.accept()
            print("waiting connect",addr)
            #设置为非阻塞
            connfd.setblocking(False)
            #关注客户端连接套接字
            rlist.append(connfd)
        else:
            #某个客户端发来了消息
            data=r.recv(1024)
            #客户端结束
            if not data:
                rlist.remove(r) #取消关注
                r.close()
                continue #for循环遍历后面的IO
            print(data.decode())
            wlist.append(r) #加入写关注列表

    for w in wlist:
        w.send(b"OK")
        wlist.remove(w) #取消关注



