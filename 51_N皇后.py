from typing import List




class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:

        ret = []
        # j 列
        col = [False] * n
        """
            [00, 01, 02]
            [10, 11, 12]
            [20, 21, 22]
        """
        # 对角线 一共 2n-1 条
        # 右对角线（左上到右下），规律是每一条线的 idx+j 相等 且 值为从小到大，第x条线等于 第i行j列 idx+j 
        # 左对角线（从右上到左下），规律是每一条线相减的值相等, 第x条线等于 第i行j列  i - j + (n-1) = x
        r_line = [False] * (2*n - 1)
        l_line = [False] * (2*n - 1)

        def gen_ret(n, row):
            ret = []
            for i in range(n):
                tmp_row = ''
                for j in range(n):
                    if (i, j) == row[i]:
                        tmp_row += "Q"
                    else:
                        tmp_row += "."
                ret.append(tmp_row)
            return ret


        def solve(idx, n, row):
            if idx == n:
                ret.append(gen_ret(n, row))
                return

            for j in range(n):
                if not any([col[j], r_line[idx+j], l_line[idx-j+n-1]]):
                    row.append((idx, j))
                    col[j] = r_line[idx + j] = l_line[idx - j + n - 1] = True
                    solve(idx + 1, n, row)
                    row.pop()
                    col[j] = r_line[idx + j] = l_line[idx - j + n - 1] = False

        _row = []
        solve(0, n, _row)
        return ret


s = Solution()
ret = s.solveNQueens(4)
print(ret)
