from typing import List


class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        if k > n or sum(nums) % k != 0:
            return False

        nums.sort(reverse=True)
        bucker = [0] * k
        target = sum(nums) / k
        use = 0
        memo = dict()

        def backtrack(idx, k, bucket, start):
            nonlocal use
            # 结束条件
            if k == 0:
                return True

            if bucker == target:
                res = backtrack(k - 1, 0)
                memo[use] = res
                return res

            if use in memo:
                return memo[use]

            for i in range(start, n):
                if ((use >> i) & 1) == 1:
                    continue
                tmp = bucker + nums[idx]
                if tmp > target:
                    continue
                use |= 1 << i
                bucker = tmp
                if backtrack(k, tmp, i + 1):
                    return True
                bucker -= nums[idx]
                use ^= 1 << i
            return False

        return backtrack(k, 0, 0, 0)


s = Solution()
nums = [2,2,2,2,3,4,5]
k = 4
ret = s.canPartitionKSubsets(nums, k)
print(ret)