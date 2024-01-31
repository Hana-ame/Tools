package com.example.tools;

import java.util.Comparator;
import java.util.PriorityQueue;

public class PriorityQueueWithMemo<E> extends PriorityQueue<E> {
  public E memo;

  public PriorityQueueWithMemo(Comparator<? super E> comparator, E memo){
    super(comparator);
    this.memo = memo;
  }

  public void setMemo(E e) {
    memo = e;
  }
  public E getMemo() {
    return memo;
  }
}
