package com.example.tools;

import java.util.ArrayList;
import java.util.LinkedList;
// import java.util.Arrays;
import java.util.List;

public class MyUtils {
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

    public static class Arrays {
        // Arrays.asList can only deal with T[], where T is Object.

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
            List<T> list = java.util.Arrays.asList(arr);
            return (ArrayList<T>) list;
        }
        public static <T> LinkedList<T> asLinkedList(T[] arr) {
            LinkedList<T> list = new LinkedList<>();
            for (T e : arr) {
                list.add(e);
            }
            return (LinkedList<T>) list;
        }

    }

    // print
    public static void printList(List<?> a) {
        String firstClassName = "?";
        if (!a.isEmpty()) {
            firstClassName = a.get(0).getClass().getName();
        }
        System.out.printf("List<%s>[ ", firstClassName);
        for (Object o : a) {
            String currentClassName = o.getClass().getName();
            System.out.printf(o.toString());
            if (!currentClassName.equals(firstClassName))
                System.out.printf("<%s>, ", currentClassName);
            else
                System.out.printf(", ");
        }
        System.out.printf("]");
        System.out.println();
    }
    
    public static <T> void printArray(T[] a) {        
        String firstClassName = "Object";
        if (a.length > 0) {
            firstClassName = a[0].getClass().getName();
        }
        System.out.printf("%s[ ", firstClassName);
        for (T o : a) {
            String currentClassName = o.getClass().getName();
            System.out.printf(o.toString());
            if (!currentClassName.equals(firstClassName))
                System.out.printf("<%s>, ", currentClassName);
            else
                System.out.printf(", ");
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(char[] a) {
        System.out.printf("char[ ");
        for (char o : a) {
            System.out.printf("%s, ", o);
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(int[] a) {
        System.out.printf("int[ ");
        for (int o : a) {
            System.out.printf("%s, ", o);
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void printArray(long[] a) {
        System.out.printf("long[ ");
        for (long o : a) {
            System.out.printf("%s, ", o);
        }
        System.out.printf("]");
        System.out.println();
    }

    public static void main(String[] args) {
        List<Integer> a = new ArrayList<>();
        printList(a);
        a.add(1);
        printList(a);
    }
}
