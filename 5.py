class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
        d = [[False] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = True

        max_len = 1
        begin = 0
        # l 个长度是否是回文
        for l in range(2, n + 1):
            print(l, n)
            for i in range(n):
                # 计算j
                j = l + i - 1
                if j >= n:
                    break

                if s[i] != s[j]:
                    d[i][j] = False
                else:
                    if j - i < 3:
                        # 回文的定义 长度小于3且2个数相等
                        d[i][j] = True
                    else:
                        d[i][j] = d[i + 1][j - 1]

                if d[i][j] and j - i + 1 > max_len:
                    max_len = j - i + 1
                    begin = i
        return s[begin: begin + max_len]


a = Solution()
a.longestPalindrome("babad")