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
        if (data.length == v.data.length) {
            for (int i=0; i<data.length; i++) {
                data[i] += v.data[i];
            }
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

}
