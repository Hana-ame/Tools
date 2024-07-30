export function getCookiesAsMap(document: Document) {
  const cookieMap = new Map<string, string>();
  
  // 获取所有cookie字符串并分割成单独的cookie
  const cookies = document.cookie.split(';');
  
  for (let cookie of cookies) {
    // 移除每个cookie字符串开头的空格
    cookie = cookie.trim();
    
    // 找到第一个等号的位置
    const separatorIndex = cookie.indexOf('=');
    
    if (separatorIndex > 0) {
      // 提取cookie的名称和值
      const key = cookie.substring(0, separatorIndex);
      const value = cookie.substring(separatorIndex + 1);
      
      // 将cookie添加到Map中，同时进行URL解码
      cookieMap.set(decodeURIComponent(key), decodeURIComponent(value));
    }
  }
  
  return cookieMap;
}