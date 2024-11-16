# 基于python的markdown静态blog部署

## 寻思

不成啊这个google抓不到我data，做的太动态的话。  
本来应该在github.io上面做的，但是那边被react的blog半成品占着。  
所以一下午寻思寻思写个python的静态部署好了，虽然肯定没有自定义模版或者别的啥了。  
但好歹这是静态的不是，总归容易索引了。

大部分是通过GPT写出来的。  

- [utils.py](https://pastebin.com/35Xc6ssa)
- [page.py](https://pastebin.com/0YqZbW1V)
- [blog.py](https://pastebin.com/eShDApj5)

配置文件是这样的，固定文件名为同文件夹下的blog.yaml  
```yaml
directories:
  - dir: "." # 文件夹，不包含子文件夹的
    tags: ["main"] # 这个文件夹分类的tag

index: "main" # 主页用的tag，主要是/tag/[tag]-0.html的copy
tags:
  - "main" # 显示在头部的tag

dist: "./bulletin" # 编译到这个目录
```

## TODO

- [ ] tag should be done.  
- [ ] more further css.  