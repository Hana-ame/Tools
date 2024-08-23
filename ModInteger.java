// 240820

package com.example.tools;

public class ModInteger {
  public static int C = (int)1e9+7;

  public static void setMOD(int n) {
    C = n;
  }

  public static ModInteger sum(ModInteger... args) {
    ModInteger result = new ModInteger(0);
    for(ModInteger i : args) {
      result.add(i);
    }
    return result;
  }
  public static ModInteger product(ModInteger... args) {
    ModInteger result = new ModInteger(1);
    for(ModInteger i : args) {
      result.multiply(i);
    }
    return result;
  }

  
  private int value;
  
  public ModInteger(int n) {
    value = n % C;
  }
  
  public int getValue() {
    return value % C;
  }

  public ModInteger add(ModInteger i) {
    value = (value + i.value) % C;
    value = (value + C) % C;
    return this;
  }
  public ModInteger substract(ModInteger i) {
    value = (value - i.value) % ModInteger.C;
    value = (value + C) % C;
    return this;
  }
  // to long
  public ModInteger multiply(ModInteger i) {
    value = (int)(((long)value * (long)i.value) % C);
    return this;
  }

  public ModInteger add(int i) {
    value = (value + i) % C;
    value = (value + C) % C;
    return this;
  }
  public ModInteger substract(int i) {
    value = (value - i) % ModInteger.C;
    value = (value + C) % C;
    return this;
  }
  // to long
  public ModInteger multiply(int i) {
    value = (int)(((long)value * (long)i) % C);
    return this;
  }
}
