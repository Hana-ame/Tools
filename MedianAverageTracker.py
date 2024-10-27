# 只能接收首字为number的tuple
# 其他用法请继续修改class

from typing import Union
from sortedcontainers import SortedList

Number = Union[int, float]


class TupleTracker(SortedList):
    @staticmethod
    def check_item(item: tuple):
        if not isinstance(item, tuple) or len(item) == 0:
            raise ValueError("添加的元素必须是非空的元组")

        num = item[0]  # 假设元组的第一个元素是数字
        if not isinstance(num, (int, float)):
            raise ValueError("元组的第一个元素必须是数字")

        return num

    def __init__(self, iterable=None, key=None):
        super().__init__(iterable, key)
        # self.sorted_list = SortedList()  # 有序集合
        self.total_sum = 0.0

    def add(self, item: tuple):
        num = TupleTracker.check_item(item)

        super().add(item)  # 添加元组到有序集合
        self.total_sum += num  # 更新总和

    def remove(self, item: tuple):
        num = TupleTracker.check_item(item)

        if item in self:
            super().remove(item)  # 从有序集合中移除元组
            self.total_sum -= num
        else:
            raise ValueError("要删除的元素不在集合中")

    def get_median(self) -> tuple:
        if self.size() == 0:
            raise ValueError("没有元素，无法计算中位数")

        mid_index = self.size() // 2
        return self[mid_index]

    def get_average(self) -> float:
        if self.size() == 0:
            raise ValueError("没有元素，无法计算平均数")

        return self.total_sum / self.size()  # 计算平均数

    def size(self) -> int:
        return len(self)  # 返回当前元素数量
