// 字符串截断函数
export function truncateString(str: string, num: number) {
  if (str.length <= num) {
    return str;
  }
  return str.slice(0, num) + '...';
};



// 24-11-16：这个函数能够对准endpoint代理一个需要CORS的请求。这里是为了得到bilibili封面用的。
// "X-Content-Type",
// "X-Content-Length",
// "X-Host",
// "X-Origin",
// "X-Referer",
// "X-Cookie",
// 这些会替换那些不让传的，Host是这里设定的
const END_POINT = "https://proxy.moonchan.xyz"
export function fetchWithProxy(
  input: string | URL,
  init?: RequestInit,
): Promise<Response> {
  const url = new URL(input);
  const endpoint = END_POINT + url.pathname + url.search

  if (!init) {
    return fetch(endpoint, {
      headers: {
        "X-Host": url.hostname,
      }
    });
  }

  if (!init.headers) {
    init.headers = {}; // 如果 init.headers 不存在，则初始化为空对象
  }

  // 这段代码不知道怎么debug，简化不了，就留在这里了
    
  // 检查 init.headers 是否是 Headers 对象
  if (init.headers instanceof Headers) {
    init.headers.append("X-Host", url.hostname); // 使用 append 方法添加头
  } else if (Array.isArray(init.headers)) {
    // 如果是一个数组类型，使用 push 添加新的头
    init.headers.push(["X-Host", url.hostname]);
  } else {
    // 将 init.headers 断言为 Record<string, string>
    const headers = init.headers as Record<string, string>;
    headers["X-Host"] = url.hostname; // 添加 X-Host 头
  }

  return fetch(endpoint, init); // 使用更新后的 init 进行 fetch
}