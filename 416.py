from typing import List, Union


class Solution:
    def canPartition(self, nums: List[int]) -> Union[bool, int]:
        """
            状态转移方程
            F(n, C) 考虑将 n 个物品填满容量为 C 的背包
            F(i, C) = F(i-1, C) || F(i-1, C-wi)

        """
        nums_sum = sum(nums)
        if nums_sum % 2 != 0:
            return False
        half_sum = nums_sum // 2
        n = len(nums)

        # -1 未使用过， 1 可以填充  0 不可以填充
        memo = [False] * (half_sum+1)
        for i in range(half_sum):
            memo[i] = (nums[0] == i)

        for i in range(1, n):
            for j in range(half_sum, -1, -1):
                if j >= nums[i]:
                    memo[j] = memo[j] or memo[j-nums[i]]
        return bool(memo[half_sum])



s = Solution()
nn = [1,1,1,1]
r = s.canPartition(nn)
print(r)
