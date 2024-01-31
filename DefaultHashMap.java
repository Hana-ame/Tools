import java.util.HashMap;

class DefaultHashMap<K, V> extends HashMap<K, V> {
  final Function<V> defaultFunction;

  DefaultHashMap(Function<V> function) {
    super();
    defaultFunction = function;
  }

  @Override
  public V get(Object key) {
    V v = null;
    return (v = super.get(key)) == null ? defaultFunction.run() : v ;
  }
  
  @Override
  public V put(K key, V value) {
    if (removeValue(value)) {
      return remove(key);
    }    
    return super.put(key, value);
  }

  protected boolean removeValue(V value) {
    return false;
  }

  public static void main(String[] args) {
    DefaultHashMap<Integer, Integer> m = new DefaultHashMap<>(()->{return 1;}); 
    Integer a = null;
    a = m.get(1);
    System.out.println(a);
    m.put(1,2);
    a = m.get(1);
    System.out.println(a);
    // 1
    // 2
  }

}
