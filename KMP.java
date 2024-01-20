// 滚动比较String，使用KMP算法
// 使用方法：
//   KMP kmp = new KMP(String pattern)
//   bool isEqual = kmp.next(char c)
//     代表加入这个char之后匹配成功
public class KMP {
  String s;
  int len; // s的长度
  int [] m; // 在这个位置匹配失败时，最多能有几个字符前缀相同
  int pe; // 全都正确的时候的下一个指针
  int ps; // 已经有的前缀数量
  
  KMP (String pattern) {
    s = pattern;
    ps = 0;
    len = s.length();
  
    // 在这个位置匹配失败时，最多能有几个字符前缀相同
    m = new int [len]; 
    // 结束标志位
    m[0] = -1;
    // 生成m
    for (int k=0, i=1; i<len; i++) {
      if (s.charAt(i) == s.charAt(k)) {
        m[i] = k;
        k++;        
      } else {
        k = 0;
      }
    }
    for (int i=1; i<len; i++) {
      next(s.charAt(i));
    }
    pe = ps;
    ps = 0;
  }
  
  public boolean next (char c) {
    while (ps >= 0) {
      if (s.charAt(ps) == c) {
        // 匹配成功的情况
        ps++;
        if (ps == len) {
          // 长度已经包括了整个s，即匹配到字符串了
          ps = pe;
          return true;
        }
        return false;
      } else {
        // 不是这个字符啊
  
        // 上一个指针，意义为已经有的前缀数量
        ps = m[ps];
      }
    }
    // 匹配不来
    
    // 清零，免得上面out of field.
    if (ps < 0) ps = 0;
  
    return false;
  }
  
  public static void main (String[] argv) {
    KMP pattern = new KMP("abab");
    System.out.println(pattern)   ;
    String s = "abababababab";
    char [] cs = s.toCharArray();
    for(char c: cs){
      boolean f = pattern.next(c);
      System.out.println(f);
    }
  }
}
