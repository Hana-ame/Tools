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
    init.headers = {
      "X-Host": url.hostname,
    };
    return fetch(endpoint, init);
  }

  // 如果 init 和 init.headers 存在，将 X-Host 加入到现有的 headers 中
  if (init.headers instanceof Headers) {
    init.headers.set("X-Host", url.hostname);
  } 

  return fetch(endpoint, init); // 使用更新后的 init 进行 fetch
}