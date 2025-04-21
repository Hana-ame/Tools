txt = """https://img.toto.im/mw600/d3782fafgy1i0f79snuo0j20wr16jgzm.jpg
https://img.toto.im/mw600/d3782fafgy1i0f79rn70nj20wr0z8h8w.jpg
https://img.toto.im/mw600/66b3de17ly1i0gbr8a86tj20wr1az7mo.jpg
https://img.toto.im/mw600/6dd57921ly1i0fm7yo2caj20m217l7gi.jpg
https://img.toto.im/mw600/66b3de17ly1i0g6hv9vcrj20z015gq7b.jpg
https://img.toto.im/mw600/007DM5Ywly1i0df8b3v6gj30ew0pb434.jpg
https://img.toto.im/mw600/006QKpwKly1i0bhyxggs7j30h70cbq4h.jpg
https://img.toto.im/mw600/66b3de17ly1i0gir7b5bmj20u00jm0ve.jpg
https://img.toto.im/mw600/66b3de17ly1i0g6i03km9j20zt0wt40z.jpg
https://img.toto.im/mw600/66b3de17ly1i0g53k0ahrj20dw0egq3x.jpg
https://img.toto.im/mw600/66b3de17ly1i0gb1vzulkj20nl0zkjtq.jpg
https://img.toto.im/mw600/66b3de17ly1i0g9s2d4u5j20fa0l63zk.jpg
https://img.toto.im/mw600/66b3de17ly1i0ghq34qk2j20jv0o7qfk.jpg
https://img.toto.im/mw600/001K5S1Pgy1i0f81vrimlj60lm0fa0wk02.jpg
https://img.toto.im/mw600/509d369egy1i0gq449hx6j20u0140jzi.jpg
https://img.toto.im/mw600/006QKpwKly1i0dscrzv0kj30n0108gq1.jpg
https://img.toto.im/mw600/66b3de17ly1i0g9ti14y2j212q1c0ag4.jpg
https://img.toto.im/mw600/6dd57921ly1i0c031979ej20o00ndjtc.jpg
https://img.toto.im/mw600/b757552fgy1i0gadnlo7pj20lc0knjyf.jpg
https://img.toto.im/mw600/66b3de17ly1i0gd4t4xccj20mh1dztb8.jpg
https://img.toto.im/mw600/66b3de17ly1i0g4x4dg9qj20j60wj76g.jpg
https://img.toto.im/mw600/66b3de17ly1i0g4wy7vcvj20j60dc41k.jpg
https://img.toto.im/mw600/66b3de17ly1i0g9smgyjij20m80az0t0.jpg
https://img.toto.im/mw600/66b3de17ly1i0gh6b4c08j20ni09cjrq.jpg
https://img.toto.im/mw600/66b3de17ly1i0ggpnrqqlj20j60aa76q.jpg
https://img.toto.im/mw600/66b3de17ly1i0g8dzlkvaj20z013qwiy.jpg
https://img.toto.im/mw600/66b3de17ly1i0gh5m76fsj20nv0s6acs.jpg
https://img.toto.im/mw600/66b3de17ly1i0geq8csk8j20f00hhmyz.jpg
https://img.toto.im/mw600/66b3de17ly1i0gftqyhtrj20ir0zk3zu.jpg
https://img.toto.im/mw600/66b3de17ly1i0gh6hdjn5j20kq0l8td7.jpg
https://img.toto.im/mw600/66b3de17ly1i0gh5fsouxj20kq0iwabh.jpg
https://img.toto.im/mw600/66b3de17ly1i0gg17haaqj20kq0nfdkf.jpg
https://img.toto.im/mw600/66b3de17ly1i0gg1dnypkj20uy0g0myf.jpg
https://img.toto.im/mw600/66b3de17ly1i0gjvfu643j20u013daee.jpg
https://img.toto.im/mw600/66b3de17ly1i0gcrb1e42j215o1jke81.jpg
https://img.toto.im/mw600/66b3de17ly1i0gh6tus6cj20j40u043q.jpg
https://img.toto.im/mw600/66b3de17ly1i0gijwsfz0j20zi152n1h.jpg
https://img.toto.im/mw600/66b3de17ly1i0gb1jg86oj20fy078glx.jpg
https://img.toto.im/mw600/66b3de17ly1i0gbiqw5yej20km0fg42a.jpg
https://img.toto.im/mw600/66b3de17ly1i0g724fx6vj20u00u0wkz.jpg
https://img.toto.im/mw600/007QvzfIgy1i0abs5y0zyj30sg0s5ac6.jpg
https://img.toto.im/mw600/66b3de17ly1i0goi9i7k8j20v714d42w.jpg
https://img.toto.im/mw600/007Go198gy1i0g6i5n1b9j30wi0hognc.jpg
https://img.toto.im/mw600/66b3de17ly1i0gg0ooz8cj20ed0hsdhc.jpg
https://img.toto.im/mw600/b757552fgy1i0gadon9n9j20k00jjtgp.jpg"""

import json

result = []
arr = txt.split("\n")
for id, item in enumerate(arr):
    result.append({
        "id": str(id),
        "url": item,
        "title": "titile",
        "description": f"{id} + | +{item}",  
    })
    
with open("result.json", "w") as f:
    json.dump(result, f, indent=2)