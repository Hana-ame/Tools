// ongoing 

import java.util.ArrayList;
import java.util.List;

public class SEG<E> {
  List<E> arr;
  Node root;
  Calculator<E> lifter;

  @FunctionalInterface
  interface Calculator<E> {
    E lift(E a, E b);
  }

  class Node {
    E cached;
    boolean modified;
  
    Node pn;
    int l;
    int r;
    Node ln;
    Node rn;
    Node(Node pn, int l, int r){
      this.pn = pn;
      this.l = l;
      this.r = r;
      if (l == r) {
        cached = arr.get(l);
        return;
      }
      int m = (l+r)/2;
      this.ln = new Node(this, l, m);
      this.rn = new Node(this, m+1, r);
      cached = value();
      return;
    }
    public E value() {
      if ( l == r || ln == null || rn == null) { return arr.get(l); }
      if (!modified) { return cached; }
      cached = lifter.lift(ln.value(), rn.value());
      modified = false;
      return cached;
    }  

    public E set(int index, E element) {      
      E e = null;
      if (l <= index && index <= r) {
        if (l==r) { return arr.set(index, element); }
        modified = true;
        e = ln.set(index, element);
        if (e != null) return e;
        else return rn.set(index, element);
      }
      return e;
    }
  }

  SEG(List<E> arr, Calculator<E> lifter) {
    this.arr = arr;
    this.lifter = lifter;
    this.root = new Node(null, 0, arr.size()-1);
  }

  public E set(int index, E element) {
    return root.set(index, element);
  }

  public Node query(int low, int high) {
    if (l < low) {
      if ((l+r)/2 <low) {
        // todo
      }
    }
  }

  public static void main(String[] args) {
    ArrayList<Integer> arr = new ArrayList<>();
    arr.add(1);
    arr.add(2);
    arr.add(3);
    arr.add(4);
    arr.add(5);
    SEG<Integer> seg = new SEG<>(arr, (a, b)->{return Math.max(a,b);});
  }

}
