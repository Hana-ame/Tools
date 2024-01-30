import java.util.HashMap;

public class DefaultHashMap<K, V> extends HashMap<K, V> {
  final Function<V> defaultFunction;

  DefaultHashMap(Function<V> function) {
    super();
    defaultFunction = function;
  }

  // @Override
  public V getOrDefault(Object key) {
    V v = null;
    return (v = super.get(key)) == null ? defaultFunction.run() : v ;
  }
  
  public static void main(String[] args) {
    DefaultHashMap<Integer, Integer> m = new DefaultHashMap<>(()->{return 1;}); 
    Integer a = null;
    a = m.getOrDefault(1);
    System.out.println(a);
    m.put(1,2);
    a = m.getOrDefault(1);
    System.out.println(a);
    // 1
    // 2
  }

}
