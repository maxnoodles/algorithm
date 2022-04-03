from typing import List


class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        n = len(matrix)

        for row in range(1, n):
            for col in range(n):
                matrix[row][col] = matrix[row][col] + min(matrix[row-1][max(col - 1, 0): min(col + 2, n)])

        return min(matrix[-1])


s = Solution()
nums = [[-19,57],[-40,-5]]
ret = s.minFallingPathSum(nums)
print(ret)
