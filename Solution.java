// import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

class Solution {
  int r;
  public int minimumSeconds(List<Integer> nums) {
    DefaultHashMap<Integer,ArrayList<Integer>> dm = new DefaultHashMap<>(()->{return new ArrayList<Integer>();});
    for (int i=0; i<nums.size(); i++) {
      ArrayList<Integer> arr = dm.get(nums.get(i));
      arr.add(i);
      dm.put(nums.get(i), arr);
    }
    r = Integer.MAX_VALUE;
    dm.forEach((k,v)->{
      int halvinterval = minimumSeconds(v, nums.size());
      // r = Math.min(r, halvinterval);
      setR(halvinterval);
    });
    return r;
  }
  private void setR(int r){
    this.r = r;
  }
  public int minimumSeconds(List<Integer> nums, int length) {
    int interval = nums.get(0)-0+length-1-nums.get(nums.size()-1);
    for (int i=0; i+1<nums.size(); i++) {
      interval = Math.max(interval, nums.get(1+1)- nums.get(i));
    }
    return (interval+1)/2;
  }
}