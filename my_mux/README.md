自己Close时没有往对面发送Close

local    remote

request    none

**未能接受到的情况**
data       none
    <-Close
closed     none

**接受到的情况**

data       data

**local关闭的情况**

closed      data
     Close->
closed     closed

**remote关闭的情况**

data        closed
    <-Close
closed     closed



哦，想起来了，Reader和Writer要分开关，你妈。