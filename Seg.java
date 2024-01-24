// ongoing 

public class Seg<T> {
  T[] arr;
  Seg(T[] _arr) {
    arr = _arr;
  }

}

class Node<T> {
  int l;
  int r;
  T valueCached;
  boolean modified;
  T[] arr;
  Node<T> ln;
  Node<T> rn;
  Node(int _l, int _r, T[] _arr){
    l = _l;
    r = _r;
    arr = _arr;
    if (l==r) {
      valueCached = arr[l];
      return;
    }
    int m = (l+r)/2;
    ln = new Node<T>(l, m, arr);
    rn = new Node<T>(m+1,r, arr);
    valueCached = ln.valueCached
    

  }
  T elect(T a, T b) {
    return a>b? a:b;
  }
}
