// 240820

package com.example.tools;

public class ModLong {
  public static long C = (int)1e9+7;

  public static void setMOD(long n) {
    C = n;
  }

  public static ModLong sum(ModLong... args) {
    ModLong result = new ModLong(0);
    for(ModLong i : args) {
      result.add(i);
    }
    return result;
  }
  public static ModLong sum(long... args) {
    ModLong result = new ModLong(0);
    for(long i : args) {
      result.add(i);
    }
    return result;
  }
  public static ModLong product(ModLong... args) {
    ModLong result = new ModLong(1);
    for(ModLong i : args) {
      result.multiply(i);
    }
    return result;
  }
  public static ModLong product(long... args) {
    ModLong result = new ModLong(1);
    for(long i : args) {
      result.multiply(i);
    }
    return result;
  }

  
  private long value;
  
  public ModLong(int n) {
    value = n % C;
  }
  
  public long getValue() {
    return value % C;
  }

  public ModLong add(ModLong i) {
    value = (value + i.value) % C;
    value = (value + C) % C;
    return this;
  }
  public ModLong substract(ModLong i) {
    value = (value - i.value) % ModLong.C;
    value = (value + C) % C;
    return this;
  }
  // to long
  public ModLong multiply(ModLong i) {
    value = (int)(((long)value * (long)i.value) % C);
    return this;
  }

  public ModLong add(long i) {
    value = (value + i) % C;
    value = (value + C) % C;
    return this;
  }
  public ModLong substract(long i) {
    value = (value - i) % ModLong.C;
    value = (value + C) % C;
    return this;
  }
  // to long
  public ModLong multiply(long i) {
    value = ((value * i) % C);
    return this;
  }


}
