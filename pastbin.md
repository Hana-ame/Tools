code: 
```java
import java.util.HashMap;

class Cache <T> {
  HashMap<String, T> m;
  Cache(){
    m = new HashMap<>();
  }

  public T handle(Function<T> Function){
    if (m.containsKey(Function.hashString())) {
      return m.get(Function.hashString());
    }
    T result = Function.run();
    m.put(Function.hashString(), result);
    return result;
  }

  public void override(Function<T> Function, T result) {
    m.put(Function.hashString(), result);
  }
  public T override(Function<T> Function) {
    T result = Function.run();
    m.put(Function.hashString(), result);
    return result;
  }

}

interface Function<T> {
  public abstract String hashString();
  public abstract T run();  
}
```

usage:
```java
class Class {
    static Cache<Integer> staticCache;

    public static void main(String[] args) {
        staticCache = new Cache<>();
    public static int Functionc(int i) {
        Functionc handler = new Functionc(i);
        return staticCache.handle(handler);
    }

    public void func() {
      
    }
  }
}

// 需要显式
class Functionc implements Function<Integer> {
    Integer i;
    Functionc(int i){
        this.i = i;
    }
    
    @Override
    public String hashString() {
        return String.valueOf(i);
    }

    @Override
    public Integer run() {
        System.out.println("run");
        System.out.println(i);
        return i;
    }
}

```

# defaultmap

```java

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
}

@FunctionalInterface // java 1.8
interface Function<T> {
  // public abstract String hashString();
  public abstract T run();  
}

```