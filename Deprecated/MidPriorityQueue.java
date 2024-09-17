package com.example.tools.Deprecated;

import java.util.PriorityQueue;

import com.example.tools.MyUtils;
import com.example.tools.PriorityQueueWithMemo;
import com.example.tools.MyUtils.Arrays;

// 请找时候写一个更通用的数据结构处理器
@Deprecated
public class MidPriorityQueue<E> {

  private final PriorityQueue<E> head;
  private final PriorityQueue<E> tail;

  public MidPriorityQueue(PriorityQueue<E> head, PriorityQueue<E> tail){
    this.head = head;
    this.tail = tail;
  }

  public void add(E e) {
    if (head.size() == tail.size()) {
      head.add(e);
      tail.add(head.poll());
    } else {
      tail.add(e);
      head.add(tail.poll());
    }
  }

  @FunctionalInterface
  interface Calculator<E> {
    E lift(E a, E b);
  }

  public E peek() {
    if (tail.isEmpty()) return null;
    if (head.size() == tail.size()) {
      return head.peek();
    }
    return tail.peek();    
  }
  
  public E poll() {
    if (tail.isEmpty()) return null;
    if (head.size() == tail.size()) {
      return head.poll();
    }
    return tail.poll();
  }

  public static void main(String[] args) {
    // https://leetcode.cn/problems/5TxKeK/?envType=daily-question&envId=2024-02-01
    PriorityQueueWithMemo<Long> head = new PriorityQueueWithMemo<Long>((a,b)->{return Long.compare(b,a);},(long)0){
      @Override
      public Long poll() {
        Long e = super.poll();
        memo -= e;
        return e;
      }
      @Override
      public boolean add(Long e) {
        memo += e;
        return super.add(e);
      }
    };
    PriorityQueueWithMemo<Long> tail = new PriorityQueueWithMemo<Long>((a,b)->{return Long.compare(a,b);},(long)0){
      @Override
      public Long poll() {
        Long e = super.poll();
        memo -= e;
        return e;
      }
      @Override
      public boolean add(Long e) {
        memo += e;
        return super.add(e);
      }
    };
    MidPriorityQueue<Long> mpq = new MidPriorityQueue<>(head, tail);

    // static
    long MOD = (long)1e9+7;
    // ModCalc calc = new ModCalc((long)1e9+7);
    // System.out.println(calc.get());
    // input
    int [] nums = new int[]{};
    // main
    int [] res = new int[nums.length];
    for (int i=0; i<nums.length; i++) {
        mpq.add((long)nums[i]-i);
        // calc
        long mid = mpq.peek() % MOD ;
        long part1 = mid*head.size() % MOD - head.getMemo() % MOD;
        long part2 = tail.getMemo() % MOD - mid*tail.size() % MOD;
        long sum = (part1 + part2) % MOD;
        res[i] = (int)sum;
    }
    // output
    System.out.println(MyUtils.Arrays.asList(res));
  }
}