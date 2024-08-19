package com.example.tools;

import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class DuplicatableTreeSet<K> {
  
  private transient int size = 0;
  
  TreeMap<K, Integer> m;
  
  public DuplicatableTreeSet() {
    m = new TreeMap<>();
  }

  public boolean add(K e) {
    m.put(e, m.getOrDefault(e, 0)+1);
    size++;
    return true;
  }

  public boolean remove(K key) {
    Integer counts = m.get(key);
    if (counts == null)
      return false;
    if (counts <= 1)
      m.remove(counts);
    else 
      m.put(key, counts-1);
    size--;
    return true;
  }

  public K first() { 
    return m.firstKey();
  }
  public K last() {
    return m.lastKey();
  }
}
