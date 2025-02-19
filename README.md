# build
直接在ps当中`./build.sh`就行（笔记本）

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

如果要改更多的话大概要用react框架比较好了。

```py
def convert(self, source: str) -> str:
    """
    将 Markdown 字符串转换为指定输出格式的字符串。

    参数：
        source: 以 Unicode 或 ASCII 字符串格式的 Markdown 文本。

    返回：
        指定输出格式的字符串。

    Markdown 解析分为五个步骤：

    1. 一些 [`preprocessors`][markdown.preprocessors] 对输入文本进行处理。
    2. 一个 [`BlockParser`][markdown.blockparser.BlockParser] 将预处理文本的高级结构元素解析为一个 [`ElementTree`][xml.etree.ElementTree.ElementTree] 对象。
    3. 一些 [`treeprocessors`][markdown.treeprocessors] 在 [`ElementTree`][xml.etree.ElementTree.ElementTree] 对象上运行。一个这样的 `treeprocessor`（[`markdown.treeprocessors.InlineProcessor`][]）对 [`ElementTree`][xml.etree.ElementTree.ElementTree] 对象运行 [`inlinepatterns`][markdown.inlinepatterns]，解析行内标记。
    4. 一些 [`postprocessors`][markdown.postprocessors] 在 [`ElementTree`][xml.etree.ElementTree.ElementTree] 对象被序列化为文本后运行。
    5. 输出作为字符串返回。

    """

    # 修正源文本
    if not source.strip():
        return ''  # 一个空的 Unicode 字符串

    try:
        source = str(source)
    except UnicodeDecodeError as e:  # pragma: no cover
        # 自定义错误消息，同时保持原始 traceback
        e.reason += '. -- 注意：Markdown 只接受 Unicode 输入！'
        raise

    # 按行分割并运行行预处理器。
    self.lines = source.split("\n")
    for prep in self.preprocessors:
        self.lines = prep.run(self.lines)

    # 解析高级元素。
    root = self.parser.parseDocument(self.lines).getroot()

    # 运行树处理器
    for treeprocessor in self.treeprocessors:
        newRoot = treeprocessor.run(root)
        if newRoot is not None:
            root = newRoot

    # 正确序列化。去掉顶层标签。
    output = self.serializer(root)
    if self.stripTopLevelTags:
        try:
            start = output.index(
                '<%s>' % self.doc_tag) + len(self.doc_tag) + 2
            end = output.rindex('</%s>' % self.doc_tag)
            output = output[start:end].strip()
        except ValueError as e:  # pragma: no cover
            if output.strip().endswith('<%s />' % self.doc_tag):
                # 我们有一个空文档
                output = ''
            else:
                # 我们遇到了严重的问题
                raise ValueError('Markdown 无法去掉顶层 '
                                 '标签。文档=%r' % output.strip()) from e

    # 运行文本后处理器
    for pp in self.postprocessors:
        output = pp.run(output)

    return output.strip()
```

registerExtensions
ext.extendMarkdown(self)

新建一个print看看都有些什么。
