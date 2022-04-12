import random
from typing import List


class Solution:
    def randomized_partition(self, nums, l, r):
        pivot = random.randint(l, r)
        nums[pivot], nums[r] = nums[r], nums[pivot]
        i = l
        for j in range(l, r):
            if nums[j] < nums[r]:
                nums[j], nums[i] = nums[i], nums[j]
                i+=1
        nums[i], nums[r] = nums[r], nums[i]
        return i

    def randomized_quicksort(self, nums, l, r):
        if r - l <= 0:
            return
        mid = self.randomized_partition(nums, l, r)
        self.randomized_quicksort(nums, l, mid - 1)
        self.randomized_quicksort(nums, mid + 1, r)

    def sortArray(self, nums: List[int]) -> List[int]:
        self.randomized_quicksort(nums, 0, len(nums) - 1)
        return nums


def quick(_list):

    def _quick(_list, l, r):
        if l >= r:
            return
        pivot = random.randint(l, r)
        _list[pivot], _list[r] = _list[r], _list[pivot]
        big = l
        for i in range(l, r):
            if _list[i] < _list[r]:
                _list[i], _list[big] = _list[big], _list[i]
                big += 1
        _list[r], _list[big] = _list[big], _list[r]

        _quick(_list, l, big-1)
        _quick(_list, big+1, r)

    _quick(_list, 0, len(_list)-1)
    return _list






s = Solution()
L = [5,1,1,2,0,0]
# r = s.sortArray(L)
quick(L)
print(L)

