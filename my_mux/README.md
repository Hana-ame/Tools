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
FAIL    github.com/hana-ame/udptun/Tools/my_mux 19.329s
PS C:\workplace\udptun> ^C
PS C:\workplace\udptun>
PS C:\workplace\udptun> go.exe test -timeout 3000s -run ^TestXxx$ github.com/hana-ame/udptun/Tools/my_mux -v
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
FAIL    github.com/hana-ame/udptun/Tools/my_mux 5.299s
FAIL
```

Tag长度修了
接着还是有Close问题。

修了tag和tag生成，还是不行。

tag解决了，是顺序反了的关系。
话说为什么会反啊。

接下来是发送接收有问题，没data