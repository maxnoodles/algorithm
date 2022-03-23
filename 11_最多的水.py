from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:

        def calc(i, j):
            l = height[i]
            r = height[j]
            water = 0
            for x in range(i+1,j+1):
                if height[x] >= l:
                    water += l * (x-i)
                    break
            for y in range(j, i-1, -1):
                if height[y] > r:
                    water += r * (j-y)
                    break
            return water


        n = len(height)
        ret = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                ret[i][j] = calc(i, j)
        print(ret)
        return max([max(i) for i in ret])


s = Solution()
t = [1, 8, 6]
r = s.maxArea(t)
print(r)
