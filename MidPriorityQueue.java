import java.util.Comparator;
import java.util.PriorityQueue;

public class MidPriorityQueue<E> {
  @SuppressWarnings("serial") // Conditionally serializable
  private final Comparator<? super E> comparator;
  private final Calculator<E> calc;

  PriorityQueue<E> head;
  PriorityQueue<E> tail;

  MidPriorityQueue(Comparator<? super E> comparator, Calculator<E> calc){
    this.comparator = comparator;
    this.calc = calc;
    head = new PriorityQueue<>(comparator.reversed());
    tail = new PriorityQueue<>(comparator);
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
      return calc.lift(head.peek(), tail.peek());
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
    Integer.compare(0, 0);
    MidPriorityQueue<Integer> mpq = new MidPriorityQueue<>(
      (a,b)->{return Integer.compare(a,b);}, 
      (a,b)->{return (a+b)/2;}
    );
  }
}
