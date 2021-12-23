from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:

        ret = []

        def _comb(idx, tmp):
            if len(tmp) == k:
                ret.append(tmp[:])
                return
            y = n - (k-len(tmp)) + 2
            for i in range(idx, y):
                tmp.append(i)
                _comb(i + 1, tmp)
                tmp.pop()

        _comb(1, [])
        return ret

s = Solution()
s.combine(4, 2)