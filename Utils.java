class Utils {
    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a%b);
    }
    public static void printList(List a) {
        for (Object o : a) {
            System.out.printf("%s, ", o.toString());            
        }
        System.out.println();
    }
}
