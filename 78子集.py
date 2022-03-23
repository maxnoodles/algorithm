from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ret = []
        track = []
        n = len(nums)

        def backtrace(start):
            ret.append(track[:])
            for i in range(start, n):
                track.append(nums[i])
                backtrace(i + 1)
                track.pop()

        backtrace(0)
        return ret


word = "ABFC"

s = Solution()
L = [1, 2, 3]
r = s.subsets(L)
print(r)
