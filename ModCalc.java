package com.example.tools;
// almost unable to use.
public class ModCalc {
  final long MOD;
  ModCalc(long mod){
    MOD = mod;
  } 
  public long ans() {
    return ans;
  }
  public long mod(long n) {
    return ((n % MOD) + MOD) % MOD;
  }
  public long add(long a, long b) {
    return mod(mod(a) + mod(b));
  }
  public long sub(long a, long b) {
    return mod(mod(a) - mod(b));
  }
  public long mul(long a, long b) {
    return mod(mod(a) * mod(b))
  }
  
  // int short cut
  public int add(int a, int b) {
    return (int) add((long)a, (long)b);
  }  
  public int sub(int a, int b) {
    return (int) sub((long)a, (long)b);
  }  
  public int mul(int a, int b) {
    return (int) mul((long)a, (long)b);
  }
}
