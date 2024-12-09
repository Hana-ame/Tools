// 脑子有问题才自己写algebra, 别用, 估计用不了.

package com.example.tools;

public class Matrix {
    private int dim;
    private int [] axis;
    private int [] data;
    // IntegerMatrix(int [] data, axis ...int) {

    // }

    public static int[] LeftMul(int[][] a, int [] b) {
        int a0 = a.length;
        int a1 = a[0].length;
        int b0 = b.length;
        int [] res = new int[a0];
        for (int i=0; i<a0; i++) {
            for (int x1=0; x1<b0; x1++) {
                res[i]+=a[i][x1]*b[x1];
            }
        }
        return res;
    }
}
