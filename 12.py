from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ret, track = [], []

        def backtrack(start):
            ret.append(track[:])
            for i in range(start, n):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                track.append(nums[i])
                backtrack(i + 1)
                track.pop()

        backtrack(0)
        return ret


s = Solution()
L = [1, 2, 2]
r = s.subsetsWithDup(L)
print(r)
