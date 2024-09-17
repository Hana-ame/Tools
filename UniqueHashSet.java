package com.example.tools;

import java.util.HashMap;

public class UniqueHashSet<E> extends HashMap<E, Integer> {

  private transient int size = 0;
  
  public UniqueHashSet() {
    super();
  }

  public UniqueHashSet(UniqueHashSet<E> set) {
    super(set);
    size = set.size;
    // keySet();
  }

  public int addElement(E e) {
    int count = put(e, getOrDefault(e, 0) + 1);
    size++;
    return count;
  }

  public boolean removeElement(E e) {
    // not removed
    int count = getOrDefault(e, 0);
    if (count <= 0) {
      remove(e);
      return false;
    }
    
    // removed
    if (count == 1)
      remove(e);
    else 
      put(e, count - 1);
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