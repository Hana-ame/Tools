import sys
import os
import re
import random

cookie = 'ipb_member_id=; ipb_pass_hash=; igneous='
iplist = ["178.175.128.252","178.175.132.22","178.175.128.254","178.175.129.254","178.175.132.20"]
paras = ' -H "Host: exhentai.org" -k '

def curl(href:str) -> str:
    global iplist, cookie, paras
    href = href.replace("exhentai.org",random.choice(iplist))
    os.system(f'curl.exe --cookie "{cookie}" {paras} "{href}" -L -O -J')
    print(href.split('/')[-1])
    return href.split('/')[-1]

def download(href:str) -> str:
    fn = href.split('/')[-1]
    print(fn)
    while not os.path.exists(fn):
        fn = curl(href)
    print(fn)
    with open(fn, encoding='utf-8') as f:
        txt = f.read()
        l = re.findall(r'https://exhentai.org/fullimg.php\?gid=[0-9]*&amp;page=[0-9]*&amp;key=\w*',txt)
        if not l:
            l = re.findall(r'<img id="img" src="([^"]+)"',txt)
        print(l)
        # for i in l:
        url = l[-1].replace('&amp;','&') 
        print(url)
        curl(url)
        l = re.findall(r'<a id="next" onclick="[^"]*?" href="([^"]*?)">',txt)
        print(l)
        if l:
            return l[0]
    return ''
        

href = 'https://exhentai.org/s/8a2b3a4139/2168176-1107'
while href != '':
    nexthref = download(href)
    if href == nexthref:
        break
    herf = nexthref
