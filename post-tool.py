import os
import pyperclip



tid = 101487
lasts = ""

s = pyperclip.paste()
while True:
    if s.startswith('https://pbs.twimg') and lasts != s:
        # url = 'https://pbs.twimg.com/media/FgqE_yaUYAAVXdK?format=jpg&name=large'.replace('&',r'\&')
        url = s.replace('&',r'\&')
        msg = fr'{{\"m\":\"post\",\"tid\":{tid},\"bid\":35,\"n\":\"\",\"t\":\"\",\"id\":\"Nanaka\",\"auth\":\"{auth}\",\"txt\":\"\",\"p\":\"{url}\",\"page\":0}}'
        os.system(f'curl -X POST {path} -d {msg} &')
        lasts = s
    s = pyperclip.paste()