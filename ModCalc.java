// 请用ModInteger。这个文件留着展示。

package com.example.tools;
// almost unable to use.
public class ModCalc {
  final long MOD;
  long ans;
  ModCalc(long mod){
    MOD = mod;
  } 
  ModCalc(int mod){
    this((long)mod);
  } 
  ModCalc(ModCalc calc){
    MOD = calc.MOD;
    ans = calc.ans;
  }
  public long ans() {
    return ans;
  }
  public ModCalc set(long n) {
    ans = n % MOD;
    return this;
  }
  public ModCalc set(int n) {
    return set((long)n);
  }
  public ModCalc set(ModCalc calc) {
    ans = calc.ans % MOD;
    return this;
  }
  public ModCalc add(long n) {
    n %= MOD;
    ans += n;
    ans %= MOD;
    return this;
  }
  public ModCalc add(int n) {
    return add((long)n);
  }
  public ModCalc add(ModCalc calc) {
    calc.ans %= MOD;
    ans += calc.ans;
    ans %= MOD;
    return this;
  }
  public ModCalc sub(long n) {
    n %= MOD;
    ans -= n;
    ans += MOD;
    ans %= MOD;
    return this;
  }
  public ModCalc sub(int n) {
    return sub((long)n);
  }
  public ModCalc sub(ModCalc calc) {
    calc.ans %= MOD;
    ans -= calc.ans;
    ans += MOD;
    ans %= MOD;
    return this;
  }
  public ModCalc mul(long n) {
    n %= MOD;
    ans *= n;
    ans %= MOD;
    return this;
  }
  public ModCalc mul(int n) {
    return mul((long)n);
  }
  public ModCalc mul(ModCalc calc) {
    calc.ans %= MOD;
    ans *= calc.ans;
    ans %= MOD;
    return this;
  }
}
