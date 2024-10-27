import sys
from PIL import Image

# fn = "2023年7月N2真题_page-0001.jpg"

def convertToMono(fn):
  image = Image.open(fn)  # 替换"your_image.jpg"为你要打开的图片文件名
  _,g,_ = image.split()
  g.save(fn.replace('.jpg', '.2.jpg'))

for fn in sys.argv:
  if fn.endswith('.jpg'):
    print(fn)
    convertToMono(fn)
