TODO 加一个ack，以防丢
配合还要加writebuffer。
```log
2024/09/20 21:32:18 handleServer
2024/09/20 21:32:20 handleClient
2024/09/20 21:32:20 handleClient
2024/09/20 21:32:20 0->5:1,Request,
2024/09/20 21:32:20 5->0:1,Acknowledge,
2024/09/20 21:32:20 handleConn
2024/09/20 21:32:20 0->5:2,Request,
2024/09/20 21:32:20 5->0:1,Data, 来自server 0
2024/09/20 21:32:20 handleConn
2024/09/20 21:32:20 0->5:2,Data, 来自client 0
2024/09/20 21:32:20 5->0:2,Acknowledge,
2024/09/20 21:32:20 0->5:1,Data, 来自client 0
FAIL    github.com/Hana-ame/udptun/Tools/my_mux 19.329s
PS C:\workplace\udptun> ^C
PS C:\workplace\udptun>
PS C:\workplace\udptun> go.exe test -timeout 3000s -run ^TestXxx$ github.com/Hana-ame/udptun/Tools/my_mux -v
=== RUN   TestXxx
2024/09/20 21:32:45 handleServer
2024/09/20 21:32:50 handleClient
2024/09/20 21:32:50 0->5:1,Request, 
2024/09/20 21:32:50 5->0:1,Acknowledge,
2024/09/20 21:32:50 0->5:1,Data, 来自client 0
2024/09/20 21:32:50 5->0:1,Close,
2024/09/20 21:32:50 handleConn
2024/09/20 21:32:50 5->0:1,Data, 来自server 0
2024/09/20 21:32:50 0->5:1,Close,
2024/09/20 21:32:51 5->0:1,Data, 来自server 1
2024/09/20 21:32:51 0->5:1,Close, 
2024/09/20 21:32:51 0->5:1,Data, 来自client 1
2024/09/20 21:32:51 5->0:1,Close,
2024/09/20 21:32:52 5->0:1,Data, 来自server 2
2024/09/20 21:32:52 0->5:1,Data, 来自client 2
2024/09/20 21:32:52 5->0:1,Close,
2024/09/20 21:32:52 0->5:1,Close,
2024/09/20 21:32:53 0->5:1,Data, 来自client 3
2024/09/20 21:32:53 5->0:1,Close, 
2024/09/20 21:32:53 5->0:1,Data, 来自server 3
2024/09/20 21:32:53 0->5:1,Close,
2024/09/20 21:32:54 5->0:1,Data, 来自server 4
2024/09/20 21:32:54 0->5:1,Data, 来自client 4
2024/09/20 21:32:54 5->0:1,Close,
2024/09/20 21:32:54 0->5:1,Close,
```
Request没有被正常响应
Close没有正常被响应

先修Close，不然Request把问题盖住了

```log
2024/09/20 21:46:07 handleServer
2024/09/20 21:46:12 handleClient
2024/09/20 21:46:12 0->5:1,Request, 
2024/09/20 21:46:12 5->0:1,Acknowledge,
2024/09/20 21:46:12 handleConn
2024/09/20 21:46:12 after request
2024/09/20 21:46:12 print mux map 0
[0 0 0 5 1] &{0xc000088750 [0 0 0 5 1] 5 0 1 0 0 0xc000086840 0 1024 32 false}
2024/09/20 21:46:12 0->5:1,Data, 来自client 0
2024/09/20 21:46:12 [0 0 0 5 1] server recv:
2024/09/20 21:46:12 5->0:1,Data, 来自server 0
2024/09/20 21:46:12 0->5:1,Close,
2024/09/20 21:46:12 EOF
FAIL    github.com/Hana-ame/udptun/Tools/my_mux 5.299s
FAIL
```

Tag长度修了
接着还是有Close问题。

修了tag和tag生成，还是不行。

tag解决了，是顺序反了的关系。
话说为什么会反啊。

接下来是发送接收有问题，没data

气笑了，是返回的n没设置

closing会导致锁死。

client的closing不行
去掉了printMap好了

首先是一个local的

Bus提供公用接口

停在Route

非常Raw的也要提供一下
bus_test.go

改一下
现在mux肯定没法用


client的sBus忘记加map里面了。加了就好
喷了，有时候client的newconn没有输出的。

差不多成了的。
client dial的时候可能还是有点问题，但是如果是按顺序的Bus的话应该没问题了。
接下来是Router的问题。
不过话说明明已经按顺序了为什么还是会丢一部分啊。
接下来先更新一下websocket的反向代理得了。
其实还有多路还有缓冲之类的东西。

大体上是

read/write         accpet                                             dial                write/read
conn -- pipe bus -- server -- 转接头 bus -- 真实链接 -- 转接头 bus -- client -- pipe bus -- conn
conn -- pipe bus --                                                        -- pipe bus -- conn
conn -- pipe bus --                                                        -- pipe bus -- conn

还要加 router。
switcher
hub什么的

比如顺序的整理器
队列什么的
果然还是加到Conn里面吧。

## 在wsl里面的指南

似乎还不需要build
`git submodule foreach git pull`

反正在这里pull了test。

整了半天没整出有色debug。。

单次链接，多个链接

带close的情况

- [x] Tag明显又反了，需要接收的时候直接取tag然后相等的
    好像是写错了
没有自增

需要干掉server接受到close之后好像不干活的问题

好像是没处理。

好像收到close不能自动close，什么毛病。

要存远端是不是要closed。好麻烦。  
还要存自己端。  
反正应该嘛，算成了。  
这个问题留到TCPConn的时候解决。  
- 双向的close。
- read、write channel的不好处
- channel 应该如下，写一串东西，然后close。
- 写到close禁止写入
- 读到close禁止读
- 感觉单向conn才是基本元素，草泥马
- 感觉其实可以去掉port直接通的。

其实应该把基础的小结构分的再小一点。应该让writerreader都自治的。
放TCPConn的地方解决

现在就全都放到ws带重传的bus上。


