import java.util.Arrays;

public class IntVector {
    private int [] data;

    public IntVector(int initialSize) {
        data = new int[initialSize];
    }
  
    public IntVector(int [] initialData) {
        data = initialData;
    }

    public IntVector add(IntVector v) {
        int minLength = Math.min(data.length, v.data.length);
        for (int i = 0; i < minLength; i++) {
            data[i] += v.data[i];
        }
        return this;
    }

    
    public IntVector minus(IntVector v) {
        int minLength = Math.min(data.length, v.data.length);
        for (int i = 0; i < minLength; i++) {
            data[i] -= v.data[i];
        }
        return this;
    }

    public int size() {
        return data.length;
    }

    public int get(int index) {
        if (index < 0 || index >= data.length) {
            throw new IndexOutOfBoundsException("Index out of bounds");
        }
        return data[index];
    }

    public static IntVector add(IntVector v1, IntVector v2) {
        int maxLength = Math.max(v1.size(), v2.size());
        int[] result = new int[maxLength];

        for (int i = 0; i < maxLength; i++) {
            int val1 = (i < v1.size()) ? v1.get(i) : 0;
            int val2 = (i < v2.size()) ? v2.get(i) : 0;
            result[i] = val1 + val2;
        }
        return new IntVector(result);
    }

    public static IntVector minus(IntVector v1, IntVector v2) {
        int maxLength = Math.max(v1.size(), v2.size());
        int[] result = new int[maxLength];

        for (int i = 0; i < maxLength; i++) {
            int val1 = (i < v1.size()) ? v1.get(i) : 0;
            int val2 = (i < v2.size()) ? v2.get(i) : 0;
            result[i] = val1 - val2;
        }
        return new IntVector(result);
    }

}
