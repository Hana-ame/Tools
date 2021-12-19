# 使用方法
# 在命令行中输入
# py .\excurl.py 原图  https://exhentai.org/g/2082242/b0e*7fb9b6/ （开头的py可能是python或python3）
# 原图为爬原图的选项，没有这两个字就是爬缩略图
# 运行完毕会将图片移入以标题为名的文件夹，不过还请在空的文件夹下面运行避免事故
# 使用请填入自己的cookie
# 如有必要请修改代理地址

import sys
import os
import re
import random

# 请填入自己的cookie
cookie = 'ipb_member_id=; ipb_pass_hash=; igneous='

override = True
iplist = ["178.175.128.252","178.175.132.22","178.175.128.254","178.175.129.254","178.175.132.20"]
defaultmode = 'default'
flag缩图 = False

def 链接方式(mode=defaultmode):    
    global override
    if mode == 'proxy':
        return " -x http://localhost:10809 -k"
    elif mode == 'direct':
        return ' '
    elif mode != 'default':
        return mode
    if override:
        return ' -H "Host: exhentai.org" -k '
    else:
        return " -x http://localhost:10809 "
    

def 链接override(链接):
    global override, iplist
    if override:
        return 链接.replace("exhentai.org",random.choice(iplist)) # todo
    else:
        return 链接 

def 下载page(链接, last, first=0): # 第一页为0，最后一页为显示出的最后一页
    page列表 = []
    for i in range(first,last):
        文件名 = '{画廊id}.p{页码}.html'.format(画廊id=链接.split('/')[-3], 页码=i)
        if not os.path.exists(文件名):
            os.system('curl.exe --cookie "{cookie}" {链接方式} "{链接}?p={页码}" > {文件名}'.format(cookie=cookie,链接=链接override(链接), 页码=i, 文件名=文件名, 链接方式=链接方式()))
        page列表.append(文件名)
    return page列表

def 读取pic列表(文件列表):
    pic列表 = []
    for filename in 文件列表:
        with open(filename, encoding='utf-8') as f:
            txt = f.read()
            l = re.findall(r'https://exhentai.org/s/[0-9a-f]{10}/[0-9]*-[0-9]*',txt)
            for i in l:
                pic列表.append(i)
    return pic列表

def 下载pic(链接列表):
    for 链接 in 链接列表:
        文件名 = 链接.split('/')[-1]
        if not os.path.exists(文件名):
            os.system('curl.exe --cookie "{cookie}" {链接方式} "{链接}" -O -J'.format(cookie=cookie, 链接=链接override(链接), 链接方式=链接方式()))
        with open(文件名, encoding='utf-8') as f:
            txt = f.read()
            l = re.findall(r'https://exhentai.org/fullimg.php\?gid=[0-9]*&amp;page=[0-9]*&amp;key=\w*',txt)
            print(l)
            if flag缩图:
                l = []
            for i in l:
                原图链接 = i.replace('&amp;','&') 
                print(原图链接)
                os.system('curl.exe --cookie "{cookie}" {链接方式} "{链接}" -L -O -J'.format(cookie=cookie, 链接=链接override(原图链接), 链接方式=链接方式()))
            if l == []:
                lnext = re.findall(r'https://\w+(?:\.\w+)*\.hath.network(?:\:[0-9]+)?/[.\w;=/-]*',txt)
                print(lnext)
                for i in lnext:
                    os.system('curl.exe --cookie "{cookie}" {链接方式} "{链接}" -L -O -J'.format(cookie=cookie, 链接=链接override(i), 链接方式=链接方式()))



链接 = "https://exhentai.org/g/2088459/db744f165f/"
页码 = 0

# TODO flag传参模式
def 是数字(s):
    l = re.findall(r'^[0-9]+$',s)
    return l != []

flag缩图 = True
override = False
for arg in sys.argv:
    if arg == '原图':
        flag缩图 = False
    if arg.startswith('https://exhentai.org') or arg.startswith('https://e-hentai.org'):
        链接 = arg
    if 是数字(arg):
        页码 = int(arg)

print(flag缩图)
print(链接)
# print(页码)
# exit(0)

if 页码 == 0:
    文件名 = '{画廊id}.p{页码}.html'.format(画廊id=链接.split('/')[-3], 页码=0)
    if not os.path.exists(文件名):
        os.system('curl.exe --cookie "{cookie}" {链接方式} "{链接}?p={页码}" > {文件名}'.format(cookie=cookie,链接=链接override(链接), 页码=0, 文件名=文件名, 链接方式=链接方式()))
    
    with open(文件名, encoding='utf8') as f:
        txt = f.read()
        # print(txt)
        l = re.findall(r'p=([0-9]+)', txt)
        # print(l)
        for i in l:
            i = (int(i))
            if 页码<i: 页码 = i
    页码 += 1
# exit(0)
print(页码)
# exit(0)
filelist = 下载page(链接,页码)
print(filelist)
picslist = 读取pic列表(filelist)
print(picslist)
下载pic(picslist)

txt = ""
with open(filelist[0], encoding='utf-8') as f:
    txt = f.read()

l = re.findall(r'<h1 id="gj">(.+?)</h1>', txt)
print(l)
if l == []:
    l = re.findall(r'<h1 id="gn">(.+?)</h1>', txt)
    print(l)
title = l[0]
os.system('mkdir "'+title+'"')
os.system('move *.jpg "'+title+'"')
os.system('move *.jpeg "'+title+'"')
os.system('move *.png "'+title+'"')
os.system('move *.gif "'+title+'"')
for fn in filelist:
    os.system('del "'+fn+'"')
for fn  in picslist:
    文件名 = fn.split('/')[-1]
    os.system('del "'+文件名+'"')
