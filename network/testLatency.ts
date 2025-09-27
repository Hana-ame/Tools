/**
 * 带超时功能的fetch封装
 * @param {string} url 请求的URL
 * @param {Options} options 请求选项，同fetch API。可在此对象中设置timeout属性。
 * @returns {Promise<[number, boolean]>} 返回fetch的Promise，超时或失败时会reject
 */

interface Options extends RequestInit {
    timeout?: number;
}

// 由于 cors 的限制，只能通过是否超时来查看
// elapsedTime, isFailed
export function testLatency(url: string, options: Options = {}): Promise<[number, boolean]> {
  const { timeout = 3000, ...fetchOptions } = options;
  
  return new Promise((resolve) => {
    const startTime = performance.now(); // 记录开始时间
    const controller = new AbortController();
    
    const timeoutId = setTimeout(() => {
      const endTime = performance.now();
      const elapsedTime = endTime - startTime;
      controller.abort();
      resolve([elapsedTime, true]); // 超时返回 [消费时间, true]
    }, timeout);

    fetch(url, {
      ...fetchOptions,
      signal: controller.signal
    })
      .then((response) => {
        const endTime = performance.now();
        const elapsedTime = endTime - startTime;
        clearTimeout(timeoutId);
        resolve([elapsedTime, false]); // 成功返回 [消费时间, false]
      })
      .catch((error) => {
        const endTime = performance.now();
        const elapsedTime = endTime - startTime;
        clearTimeout(timeoutId);
        
        // 如果是超时导致的错误，已经在上面的setTimeout中处理
        if (error.name === 'AbortError') {
          // 这里不需要额外处理，超时情况已经处理
        } else {
          // 其他网络错误返回 [消费时间, false]
          resolve([elapsedTime, false]);
        }
      });
  });
}