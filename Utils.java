import java.util.List;

class Utils {
    // math
    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a%b);
    }

    // builder
    public static String toRawString(String s) {
        int n = s.length();
        StringBuilder sb = new StringBuilder();
        for (int i=0; i<n; i++) {
            char ch = s.charAt(i);
            if (".$|()[{^?*+\\".indexOf(ch) != -1) {
                sb.append('\\');
            }
            sb.append(ch);
        }
        return sb.toString();
    }
    
    // print
    public static void printList(List<?> a) {
        for (Object o : a) {
            System.out.printf("%s, ", o.toString());            
        }
        System.out.println();
    }

    public static void printArray(Object[] a) {
        for (Object o : a) {
            System.out.printf("%s, ", o.toString());            
        }
        System.out.println();
    }    
    public static void printArray(char[] a) {
        for (char o : a) {
            System.out.printf("%s, ", o);            
        }
        System.out.println();
    }    
    public static void printArray(int[] a) {
        for (int o : a) {
            System.out.printf("%s, ", o);            
        }
        System.out.println();
    }
}
