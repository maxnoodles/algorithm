class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        odd = set()
        length = len(s)
        rp, max_len = 0, 0
        for i in range(length):
            if i != 0:
                odd.remove(s[i-1])
            while rp < length and s[rp] not in odd:
                odd.add(s[rp])
                rp += 1
            print(odd)
            print(rp, i)
            max_len = max(max_len, rp - i)
        return max_len

a = Solution()
ret = a.lengthOfLongestSubstring('abcb')
print(ret)