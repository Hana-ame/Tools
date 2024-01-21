// 先实现双向链表节点类
class DoubleLinkedListNode<K, V> {
  key: K | undefined; // 因为我们需要配合 Map，需多加一条 key 属性
  val: V | undefined;
  next: DoubleLinkedListNode<K, V> | null; // 指向下一个节点
  prev: DoubleLinkedListNode<K, V> | null; // 指向上一个节点
  constructor(key?: K, val?: V) {
    this.key = key;
    this.val = val;
    this.next = null;
    this.prev = null;
  }
}

// 实现双链表类
class DoubleLinkedList<K, V> {
  head: DoubleLinkedListNode<K, V>;
  tail: DoubleLinkedListNode<K, V>;
  capacity: number
  constructor() {
    // 构造一个双向的链表
    this.head = new DoubleLinkedListNode();
    this.tail = new DoubleLinkedListNode();
    this.head.next = this.tail;
    this.head.prev = this.tail;
    this.tail.prev = this.head;
    this.tail.next = this.head;
    this.capacity = 0;
  }
  get size(): number {
    return this.capacity;
  }

  // 将传入的节点变成 head 节点指向的下一个节点
  linkToHead(node: DoubleLinkedListNode<K, V>) {
    if (node == null) {
      return;
    }
    node.next = this.head.next; // 新节点的 next 指针指向现 head 节点的 next 指针指向的节点
    node.prev = this.head; // 新节点的 prev 指针指向 head 节点
    this.head.next!.prev = node;
    this.head.next = node;
    this.capacity++;
  }
  // linkAfter
  // linkBefore

  delete(node: DoubleLinkedListNode<K, V>): DoubleLinkedListNode<K, V> | null {
    if (node == null || node == this.head || node == this.tail) {
      return null;
    }
    node.prev!.next = node.next;
    node.next!.prev = node.prev;
    this.capacity--;
    return node;
  }
  deleteLast(): DoubleLinkedListNode<K, V> | null {
    if (this.head.next === this.tail) {
      return null;
    }
    this.capacity--;
    return this.delete(this.tail.prev!);
  }
}

// 实现 LRU 缓存类
class LRUCache<K, V> {
  private capacity: number;
  private map: Map<K, DoubleLinkedListNode<K, V>>;
  private list: DoubleLinkedList<K, V>;
  constructor(capacity: number) {
    this.capacity = capacity;
    this.map = new Map();
    this.list = new DoubleLinkedList();
  }
  put(key: K, value: V): void {
    if (this.map.has(key)) {
      const node = this.map.get(key)!;
      node.val = value;
      this.list.delete(node); // 链表的 delete 方法只是改变指针方向，并不是个耗费性能的操作
      this.list.linkToHead(node); // 更新双链表头部，保持 most recently used 能快速访问
    } else {
      // 如果 capacity 已经满了，就删除最不常用的节点
      if (this.map.size > this.capacity) {
        const deleteKey = this.list.deleteLast();
        if (deleteKey?.key !== undefined) {
          this.map.delete(deleteKey.key);
        }
      }
      const node = new DoubleLinkedListNode(key, value);
      this.list.linkToHead(node); // 更新链表头部
      this.map.set(key, node); // 更新 Map
    }
  }
  // 访问操作
  get(key: K): V | undefined {
    // 如果有 key 就返回 value，并且更新到双链表的头部
    if (this.map.has(key)) {
      const node = this.map.get(key)!;
      const value = node.val!;
      this.put(key, value);
      return value;
    }
    return;
  }
}
