package com.example.tools;

import javax.swing.text.Segment;

public class SegmentTree {
  private int sum;
  private int lo;
  private int hi;

  private SegmentTree left;
  private SegmentTree right;
  
  private int value;

  public SegmentTree(int n) {

    value = n;

    sum = n;
    lo = n;
    hi = n;
  }

  public SegmentTree(int n, SegmentTree left, SegmentTree right) {
    
    value = n;

    sum = n;
    lo = n;
    hi = n;
    
    if (left != null) {
      lo = left.lo;
      sum += left.sum;
    }
    if (right != null) {
      hi = right.hi;
      sum += right.sum;
    }
  }
  

  public void add(int n) {
    sum += n;
    lo = Math.min(lo, n);
    hi = Math.max(hi, n);
  }
}
