package com.example.tools;

import java.util.HashMap;

public class UniqueSet<E> extends HashMap<E, Integer> {

  private int size = 0;
  
  public UniqueSet() {
    super();
  }

  public UniqueSet(UniqueSet<E> set) {
    super(set);
    size = set.size;
    keySet();
  }

  public void addElement(E e) {
    put(e, getOrDefault(e, 0) + 1);
    size++;
  }

  public boolean removeElement(E e) {
    // not removed
    int oldVal = getOrDefault(e, 0);
    if (oldVal <= 0) {
      remove(e);
      return false;
    }
    
    // removed
    if (oldVal == 1)
      remove(e);
    else 
      put(e, oldVal - 1);
    size--;      
    return true;
  }

  public int uniqueSize() {
    return super.size();
  }

  public int size() {
    return size;
  }

}