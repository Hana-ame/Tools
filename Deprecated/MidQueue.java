package com.example.tools.Deprecated;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.PriorityQueue;
import com.example.Utils;

// 请找时候写一个更通用的数据结构处理器
@Deprecated
public class MidQueue<E extends Comparable<E>>  {
  
  private final PriorityQueue<E> lo;
  private final PriorityQueue<E> hi;
  private final Comparator<? super E> comparator;

  public MidQueue(Comparator<? super E> comparator){
    this.comparator = comparator;
    this.lo = new PriorityQueue<>((b,a) -> {return comparator.compare(a,b);}); // reversed.
    this.hi = new PriorityQueue<>((a,b) -> {return comparator.compare(a,b);});
  }
  // no, the two pq is different.
  // public MidQueue() {
  //   this(new PriorityQueue<E>(), new PriorityQueue<E>());
  // }

  public void add(E e) {
    lo.add(e);
    if (lo.size() -1 > hi.size()) {
      hi.add(lo.poll());
    }
    if (!hi.isEmpty() && comparator.compare(lo.peek(),(hi.peek())) > 0) {
      hi.add(lo.poll());
      lo.add(hi.poll());
    }    
  }

  public E peek() {
    if (lo.isEmpty()) return null;
    return lo.peek();
  }
  
  public E poll() {
    if (lo.isEmpty()) return null;
    return lo.poll();
  }


  public static void main(String[] args) {
    // https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/?envType=daily-question&envId=2024-08-27
    // input 
    ArrayList<Double> arr = Utils.getDataFromJsonFile("testcases/3134.json");
    int [] nums = new int[arr.size()];
    for (int i=0; i<nums.length; i++) {
      double d = arr.get(i);
      nums[i] = (int) Math.round(d);
    }
    // main
    MidQueue<Integer> q = new MidQueue<>(
      (a,b) -> {return a-b;}
    );
    ArrayList<HashSet<Integer>> maps = new ArrayList<HashSet<Integer>>(nums.length);
    for (int i=0; i<nums.length; i++) {
      maps.add( new HashSet<Integer>() );
      for (int j=0; j<=i; j++) {
        maps.get(j).add(nums[i]);
        q.add(maps.get(j).size());
      }
    }
    int r = q.peek();

    System.out.println(r);
  }
}
