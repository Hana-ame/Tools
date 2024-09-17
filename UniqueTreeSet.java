package com.example.tools;

import java.util.TreeMap;

public class UniqueTreeSet<E> extends TreeMap<E, Integer>{
  
  private transient int size = 0;
  
  public UniqueTreeSet() {
    super();
  }

  public UniqueTreeSet(UniqueTreeSet<E> set) {
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

  // 直接去用TreeMap的东西
  // public E first() { 
  //   return firstKey();
  // }
  // public E last() {
  //   return lastKey();
  // }

}
