# not working.

import os
import pyperclip
from examples.e_dotenv import host,auth,id

print(host, auth, id)

tid = 0
lasts = ""


s = pyperclip.paste()
while True:
    if s.startswith('https://file.moonchan') and lasts != s:
        # url = 'https://pbs.twimg.com/media/FgqE_yaUYAAVXdK?format=jpg&name=large'.replace('&',r'\&')
        url = s.replace('&',r'\&')
        url = url.strip()
        msg = fr'{\{\"m\":\"post\",\"tid\":{tid},\"bid\":35,\"n\":\"\",\"t\":\"\",\"id\":\"{id}\",\"auth\":\"{auth}\",\"txt\":\"post by post tool\",\"p\":\"{url}\",\"page\":0\}}'
        print(f'curl -X POST {host} -d {msg} &')
        os.system(f'curl -X POST {host} -d {msg} &')
        lasts = s
    s = pyperclip.paste()