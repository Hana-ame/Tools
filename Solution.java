// import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class Solution {
  public int[] distinctDifferenceArray(int[] nums) {
      DefaultHashMap<Integer, Integer> dm = new DefaultHashMap<>(()->{return Integer.valueOf(0);}) {
          @Override
          protected boolean removeValue(Integer v) {
              return v == 0;
          }
      };
      Set<Integer> m = new HashSet<>();
      for (int n : nums) {
        dm.put(n, dm.get(n)+1);
      }
      int [] res = new int [nums.length];
      for (int i=0; i<nums.length; i++) {
        m.add(i);
        dm.put(nums[i],dm.get(nums[i])-1);
        System.out.println(dm);
        System.out.println(m);
        res[i] = dm.size() - m.size();
      }
      return res;
  }
  public static void main(String[] args) {
    Solution s = new Solution();
    s.distinctDifferenceArray(new int[]{1,2,3,4,5,6});
    ArrayList<Integer> arr = new ArrayList<>();
    arr.add(1);
    arr.add(1);
    arr.add(1);
    arr.add(1);
    System.out.println(arr);
    int [] a = new int[]{1,2,3,4,5,6};
    System.out.println(a);
    System.out.println(Utils.asList(a));  
    System.out.println(Utils.asList(a));  
    Arrays.asList(a);
    
    
  }
}