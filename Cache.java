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