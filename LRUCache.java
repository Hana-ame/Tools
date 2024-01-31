package com.example.tools;

import java.util.LinkedHashMap;
import java.util.Map;

class LRUCache<K, V> extends LinkedHashMap<K, V> {

  private int capacity; // 缓存容量
  // private LinkedHashMap<K, V> cache; // 缓存数据结构

  public LRUCache(int capacity) {
    // 初始化 LinkedHashMap，设置 accessOrder 为 true，表示按照访问顺序排序
    super(capacity, 0.75f, true);
    this.capacity = capacity;
  }
  
  @Override
  protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
    // 当缓存大小超过容量时，移除最老的元素
    return size() > capacity;
  }
}
