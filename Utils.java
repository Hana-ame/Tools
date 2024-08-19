import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

class Utils {
    // math
    public static int gcd(int a, int b) {
        if (b == 0)
            return a;
        return gcd(b, a % b);
    }

    // builder
    public static String toRawString(String s) {
        int n = s.length();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (".$|()[]{}^?*+\\".indexOf(ch) != -1) {
                sb.append('\\');
            }
            sb.append(ch);
        }
        return sb.toString();
    }

    // Arrays.asList
    public static ArrayList<Long> asList(long[] arr) {
        ArrayList<Long> list = new ArrayList<>(arr.length);
        for (long i : arr)
            list.add(i);
        return list;
    }    
    
    public static ArrayList<Integer> asList(int[] arr) {
        ArrayList<Integer> list = new ArrayList<>(arr.length);
        for (int i : arr)
            list.add(i);
        return list;
    }   

    public static ArrayList<Short> asList(short[] arr) {
        ArrayList<Short> list = new ArrayList<>(arr.length);
        for (short i : arr)
            list.add(i);
        return list;
    }    

    public static ArrayList<Byte> asList(byte[] arr) {
        ArrayList<Byte> list = new ArrayList<>(arr.length);
        for (byte i : arr)
            list.add(i);
        return list;
    }

    public static ArrayList<Character> asList(char[] arr) {
        ArrayList<Character> list = new ArrayList<>(arr.length);
        for (char i : arr)
            list.add(i);
        return list;
    }

    public static ArrayList<Double> asList(double[] arr) {
        ArrayList<Double> list = new ArrayList<>(arr.length);
        for (double i : arr)
            list.add(i);
        return list;
    }

    public static ArrayList<Float> asList(float[] arr) {
        ArrayList<Float> list = new ArrayList<>(arr.length);
        for (float i : arr)
            list.add(i);
        return list;
    }

    public static ArrayList<Boolean> asList(boolean[] arr) {
        ArrayList<Boolean> list = new ArrayList<>(arr.length);
        for (boolean i : arr)
            list.add(i);
        return list;
    }

    public static <T> ArrayList<T> asList(T[] arr) {
        ArrayList<T> list = (ArrayList<T>) Arrays.asList(arr);
        return list;
    }

    // print
    public static void printList(List<?> a) {
        System.out.printf("List<?>[");
        for (Object o : a) {
            System.out.printf("%s, ", o.toString());
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(Object[] a) {
        System.out.printf("Object[");
        for (Object o : a) {
            System.out.printf("%s, ", o.toString());
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(char[] a) {
        System.out.printf("char[");
        for (char o : a) {
            System.out.printf("%s, ", o);
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(int[] a) {
        System.out.printf("int[");
        for (int o : a) {
            System.out.printf("%s, ", o);
        }
        System.out.printf("]");
        System.out.println();
    }
}