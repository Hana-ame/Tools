// 字符串截断函数
export function truncateString(str:string, num:number) {
  if (str.length <= num) {
    return str;
  }
  return str.slice(0, num) + '...';
};