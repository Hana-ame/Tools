import unittest
from MedianAverageTracker import TupleTracker

class TestTupleTracker(unittest.TestCase):
    def setUp(self):
        """在每个测试之前初始化一个 TupleTracker 实例"""
        self.tracker = TupleTracker()

    def test_add_item(self):
        """测试添加元组"""
        self.tracker.add((5, 'apple'))
        self.tracker.add((3, 'banana'))
        self.tracker.add((8, 'cherry'))
        self.assertEqual(self.tracker.size(), 3)
        self.assertEqual(self.tracker.total_sum, 16.0)  # 5 + 3 + 8

    def test_remove_item(self):
        """测试删除元组"""
        self.tracker.add((5, 'apple'))
        self.tracker.add((3, 'banana'))
        self.tracker.remove((3, 'banana'))
        self.assertEqual(self.tracker.size(), 1)
        self.assertEqual(self.tracker.total_sum, 5.0)  # 只有 5

    def test_get_median(self):
        """测试获取中位数"""
        self.tracker.add((5, 'apple'))
        self.tracker.add((3, 'banana'))
        self.tracker.add((8, 'cherry'))
        self.tracker.add((1, 'date'))
        self.assertEqual(self.tracker.get_median(), (5, 'apple'))  # 中位数是 5

    def test_get_average(self):
        """测试获取平均数"""
        self.tracker.add((5, 'apple'))
        self.tracker.add((3, 'banana'))
        self.tracker.add((8, 'cherry'))
        self.assertEqual(self.tracker.get_average(), 5.333333333333333)  # (5 + 3 + 8) / 3

    def test_remove_nonexistent_item(self):
        """测试删除不存在的元组"""
        self.tracker.add((5, 'apple'))
        with self.assertRaises(ValueError):
            self.tracker.remove((3, 'banana'))

    def test_check_item_invalid(self):
        """测试检查无效元组"""
        with self.assertRaises(ValueError):
            self.tracker.add((None, 'apple'))  # 第一个元素不是数字
        with self.assertRaises(ValueError):
            self.tracker.add([])  # 不是元组
        with self.assertRaises(ValueError):
            self.tracker.add(5)  # 不是元组

if __name__ == '__main__':
    unittest.main()