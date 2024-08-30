package com.example.tools;

import java.util.HashMap;

public class UniqueSet<E> {

  private final HashMap<E, Integer> map;
  private int size = 0;
  
  public UniqueSet() {
    map = new HashMap<>();
  }

  public void add(E e) {
    map.put(e, map.getOrDefault(e, 0) + 1);
    size++;
  }

  public boolean remove(E e) {
    // not removed
    int oldVal = map.getOrDefault(e, 0);
    if (oldVal <= 0) {
      map.remove(e);
      return false;
    }
    
    // removed
    if (oldVal == 1)
      map.remove(e);
    else 
      map.put(e, oldVal - 1);
    size--;      
    return true;
  }

  public int uniqueSize() {
    return map.size();
  }

  public int size() {
    return size;
  }

}