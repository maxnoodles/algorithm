from typing import List
import random


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:

        def _quick(l, r, nums):
            pivot = random.randint(l, r)
            nums[l], nums[pivot] = nums[pivot], nums[l]
            base = nums[l]
            while l < r:
                while l < r and nums[r] <= base:
                    r -= 1
                nums[r], nums[l] = nums[l], nums[r]
                while l < r and nums[l] >= base:
                    l += 1
                nums[l], nums[r] = nums[r], nums[l]
            return l

        def random_quick(l, r, nums):
            mid = _quick(l, r, nums)
            if mid == k-1:
                return nums[mid]
            elif mid > k-1:
                return random_quick(l, mid - 1, nums)
            else:
                return random_quick(mid + 1, r, nums)

        return random_quick(0, len(nums) - 1, nums)


s = Solution()
L = [3,2,1,5,6,4]
r = s.findKthLargest(L, 2)
print(r)