package tools

import "sync"

// ConcurrentHashMap 是一个线程安全的映射，支持泛型类型
type ConcurrentHashMap[K comparable, V any] struct {
	m map[K]V
	sync.RWMutex
}

// NewConcurrentHashMap 创建一个新的 LockedMap 实例
func NewConcurrentHashMap[K comparable, V any]() *ConcurrentHashMap[K, V] {
	return &ConcurrentHashMap[K, V]{
		m:       make(map[K]V),
		RWMutex: sync.RWMutex{},
	}
}

func (m *ConcurrentHashMap[K, V]) Contains(key K) bool {
	m.RLock()
	defer m.RUnlock()
	_, ok := m.m[key]
	return ok
}

// Get 根据键获取值
func (m *ConcurrentHashMap[K, V]) Get(key K) (V, bool) {
	m.RLock()
	defer m.RUnlock()
	v, ok := m.m[key]
	return v, ok
}

// Put 插入键值对
func (m *ConcurrentHashMap[K, V]) Put(key K, value V) {
	m.Lock()
	defer m.Unlock()
	m.m[key] = value
}

// PutIfAbsent 如果键不存在，则插入键值对
func (m *ConcurrentHashMap[K, V]) PutIfAbsent(key K, value V) bool {
	m.Lock()
	defer m.Unlock()

	// 检查键是否存在
	if _, exists := m.m[key]; exists {
		return false // 键已存在，返回 false
	}

	// 键不存在，插入键值对
	m.m[key] = value
	return true // 返回 true 表示插入成功
}

// Remove 根据键删除元素
func (m *ConcurrentHashMap[K, V]) Remove(key K) {
	m.Lock()
	defer m.Unlock()
	delete(m.m, key)
}

// ForEach 遍历映射并对每个键值对调用处理函数
// handler 是一个函数，接收键和值并执行操作。
func (m *ConcurrentHashMap[K, V]) ForEach(handler func(key K, value V)) {
	if handler == nil {
		return // 如果处理函数为 nil，直接返回
	}

	m.RLock()         // 获取读取锁，确保安全访问
	defer m.RUnlock() // 确保在函数结束时释放锁

	// 遍历映射中的每个键值对并调用处理函数
	for key, value := range m.m {
		handler(key, value)
	}
}

// Size 返回映射的大小
func (m *ConcurrentHashMap[K, V]) Size() int {
	m.RLock()
	defer m.RUnlock()
	return len(m.m)
}
