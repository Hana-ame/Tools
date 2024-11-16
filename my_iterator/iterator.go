// 写这个干嘛，没事做。
// 为啥不和js一样用，又为啥要和js一样用。

package myiterator

type SliceIterator[KT any, VT any] []KT

func (s SliceIterator[KT, VT]) Map(f func(i int, v KT) VT) []VT {
	r := make([]VT, len(s))
	for i, k := range s {
		r[i] = f(i, k)
	}
	return r
}
