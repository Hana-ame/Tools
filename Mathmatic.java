// 240820

package com.example.tools;

public class Mathmatic {
  // 240820
  // author: llama-3.1-70b
  public static long combination(int n, int k) {
    long result = 1;
    for (int i = 1; i <= k; i++) {
      result = result * (n - i + 1) / i;
    }
    return result;
  }
  
  // math
  public static int gcd(int a, int b) {
    if (b == 0)
      return a;
    return gcd(b, a % b);
  }


  public static void main(String[] args) {
    long r = combination(100, 10);
    System.out.println(r);
  }
}
