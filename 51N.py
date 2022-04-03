from typing import List
from copy import deepcopy


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        ret = []
        track = [["."] * n for _ in range(n)]

        def is_valid(row, col, track):
            # 检查列冲突
            for i in range(n):
                if track[i][col] == 'Q':
                    return False

            # 右边上叫冲突
            i, j = row - 1, col + 1
            while i >= 0 and j < n:
                if track[i][j] == 'Q':
                    return False
                i -= 1
                j += 1

            # 检查左上角
            x, y = row - 1, col - 1
            while x >= 0 and y >= 0:
                if track[x][y] == 'Q':
                    return False
                x -= 1
                y -= 1
            return True

        def backtrack(row):
            # 结束条件
            if row == n:
                ret.append(deepcopy(track))
                return

            for col in range(n):
                if not is_valid(row, col, track):
                    continue

                track[row][col] = 'Q'
                backtrack(row + 1)
                track[row][col] = '.'

        backtrack(0)
        return ret


s = Solution()
ret = s.solveNQueens(4)
print(ret)
