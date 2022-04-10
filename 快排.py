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
        mid = self.randomized_partition_2(nums, l, r)
        self.randomized_quicksort(nums, l, mid - 1)
        self.randomized_quicksort(nums, mid + 1, r)

    def sortArray(self, nums: List[int]) -> List[int]:
        self.randomized_quicksort(nums, 0, len(nums) - 1)
        return nums


    def randomized_partition_2(self, nums, l, r):
        pos = random.randint(l, r)
        nums[r], nums[pos] = nums[pos], nums[r]
        big = l
        for i in range(l, r):
            if nums[i] < nums[r]:
                nums[i], nums[big] = nums[big], nums[i]
                big += 1
        nums[r], nums[big] = nums[big], nums[r]
        return big




s = Solution()
L = [5,1,1,2,0,0]
r = s.sortArray(L)
print(r)