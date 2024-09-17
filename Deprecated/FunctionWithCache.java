// 240820

package com.example.tools.Deprecated;

import java.util.HashMap;

import com.example.tools.Function;


// not used, please use cache.java.
// T is Functon's return type
// maybe turn to annotation.
@Deprecated
public abstract class FunctionWithCache<T>{
  static public HashMap<Function<?>, ?> cache = new HashMap<>();

}
