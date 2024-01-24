import java.util.HashMap;

class Cache<T> {
  HashMap<Function<T>, T> m;

  Cache() {
    m = new HashMap<>();
  }

  public T run(Function<T> function) {
    return runOrCached(function, function);
  }

  public T runOrCached(Object keyObject, Function<T> function) {
    if (m.containsKey(keyObject)) {
      return m.get(keyObject);
    }
    T result = function.run();
    m.put(function, result);
    return result;
  }

  public void override(Function<T> function, T result) {
    m.put(function, result);
  }

  public T override(Function<T> function) {
    T result = function.run();
    m.put(function, result);
    return result;
  }

  public static void main(String[] args) {
    Cache<String> cache = new Cache<>();
    String r = null;
    r = cache.run(new MyFun(1, 2, 'a', "null"));
    System.out.println(r);
    r = cache.run(new MyFun(1, 2, 'a', "nul2l"));
    System.out.println(r);
    r = cache.run(new MyFun(2, 2, 'a', "nul3l"));
    System.out.println(r);
    r = cache.run(new MyFun(2, 2, 'a', "nul4l"));
    System.out.println(r);
    // null
    // null 
    // nul3l
    // nul3l

    // 不行，可能是因为有hashcode。
    // int a = 1;
    // int b = 2;
    // cache.run(() -> {
    //    " a "
    // });

  }

}

class MyFun implements Function<String> {

  int a;
  int b;
  char c;
  String s;

  MyFun(int a, int b, char c, String s) {
    this.a = a;
    this.b = b;
    this.c = c;
    this.s = s;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + a;
    result = prime * result + b;
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    MyFun other = (MyFun) obj;
    if (a != other.a)
      return false;
    if (b != other.b)
      return false;
    return true;
  }

  @Override
  public String run() {
    return s;
  }
}