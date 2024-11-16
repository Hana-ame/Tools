// azure@24-11-13

package tools

import (
	"container/list"
)

type LRUCache[K comparable, V any] struct {
	capacity int
	cache    map[K]*list.Element
	order    *list.List
}

// CacheItem 代表缓存中的每一项
type CacheItem[K any, V any] struct {
	key   K
	value V
}

// NewLRUCache 创建一个新的 LRU 缓存
func NewLRUCache[K comparable, V any](capacity int) *LRUCache[K, V] {
	return &LRUCache[K, V]{
		capacity: capacity,
		cache:    make(map[K]*list.Element),
		order:    list.New(),
	}
}

// Get 从缓存中获取值
func (c *LRUCache[K, V]) Get(key K) (V, bool) {
	if element, found := c.cache[key]; found {
		// 移动到列表的前面，表示最近使用过
		c.order.MoveToFront(element)
		return element.Value.(CacheItem[K, V]).value, true
	}
	var zeroValue V
	return zeroValue, false
}

// Put 将值放入缓存中
func (c *LRUCache[K, V]) Put(key K, value V) {
	if element, found := c.cache[key]; found {
		// 更新值并移动到前面
		c.order.MoveToFront(element)
		element.Value = CacheItem[K, V]{key: key, value: value}
	} else {
		// 如果缓存已满，移除最少使用的元素
		if c.order.Len() >= c.capacity {
			back := c.order.Back()
			if back != nil {
				c.order.Remove(back)
				delete(c.cache, back.Value.(CacheItem[K, V]).key)
			}
		}
		// 添加新的元素
		newItem := CacheItem[K, V]{key: key, value: value}
		element := c.order.PushFront(newItem)
		c.cache[key] = element
	}
}
