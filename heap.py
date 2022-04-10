

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


class MaxHeap():

    def __init__(self, arr=None):
        if arr:
            self._data = arr
            for i in range(self._parent(self.size-1), -1, -1):
                self.sift_down(i)
        else:
            self._data = []

    @property
    def size(self):
        return len(self._data)

    def is_empty(self):
        return not self._data

    # 返回完全二叉数的数组表示中，一个索引所表示的元素的左孩子节点的索引
    def _parent(self, index):
        if index == 0:
            raise ValueError("index 0 doesn't have parent")
        return (index - 1) // 2

    # 返回完全二叉树的数组表示中，一个索引所表示的元素的左孩子节点的索引
    def left_child(self, index):
        return index * 2 + 1

    # 返回完全二叉树的数组表示中，一个索引所表示的元素的左孩子节点的索引
    def right_child(self, index):
        return index * 2 + 2

    # 向堆添加元素
    def add(self, v):
        self._data.append(v)
        self.sift_up(self.size - 1)

    def sift_up(self, i):
        while i > 0 and self._data[i] > self._data[self._parent(i)]:
            swap(self._data, i, self._parent(i))
            i = self._parent(i)

    def find_max(self):
        if self.is_empty():
            raise ValueError('Head is empty')
        return self._data[0]

    def extract_max(self):
        ret = self.find_max()
        swap(self._data, 0, self.size-1)
        self._data.pop()
        self.sift_down(0)
        return ret

    def sift_down(self, i):
        while self.left_child(i) < self.size:
            j = self.left_child(i)
            if j + 1 < self.size and self._data[j+1] > self._data[j]:
                j = self.right_child(i)
            if self._data[j] > self._data[i]:
                swap(self._data, j, i-1)
            i = j


if __name__ == "__main__":
    n = 10000
    from time import time

    start_time1 = time()
    max_heap = MaxHeap()
    from random import randint

    for i in range(n):
        max_heap.add(randint(0, n))
    print('heap add: ', time() - start_time1)  # head add:  5.748132228851318
    print(max_heap._data)

    extract_time = time()
    max_heap.extract_max()
    print(max_heap._data)
    print('heap extract max: ', time() - extract_time)  # head add:  5.748132228851318


    start_time2 = time()
    arr = []
    from random import randint

    for i in range(n):
        arr.append(randint(0, n))
    max_heap = MaxHeap(arr)
    print('\nheapify: ', time() - start_time2)  # heapify:  4.680660963058472
    print(max_heap._data)