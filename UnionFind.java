public class UnionFind {
    private int[] parent;
    private int[] rank;

    // 初始化并查集
    public UnionFind(int size) {
        parent = new int[size];
        rank = new int[size];
        for (int i = 0; i < size; i++) {
            parent[i] = i; // 每个节点的父节点初始化为自己
            rank[i] = 0;   // 初始秩为 0
        }
    }

    // 查找元素的根节点，带路径压缩
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // 路径压缩
        }
        return parent[x];
    }

    // 合并两个集合
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX != rootY) {
            // 按秩合并
            if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
        }
    }

    // 检查两个元素是否在同一集合中
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }

    public static void main(String[] args) {
        UnionFind uf = new UnionFind(10);

        // 合并一些集合
        uf.union(1, 2);
        uf.union(2, 3);
        uf.union(4, 5);

        // 检查连接
        System.out.println(uf.connected(1, 3)); // 输出: true
        System.out.println(uf.connected(1, 4)); // 输出: false
    }
}
