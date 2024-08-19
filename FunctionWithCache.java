// 240820

package com.example.tools;

import java.util.HashMap;


// not used, please use cache.java.
// T is Functon's return type
// maybe turn to annotation.
public abstract class FunctionWithCache<T>{
  static public HashMap<Function<?>, ?> cache = new HashMap<>();

}
