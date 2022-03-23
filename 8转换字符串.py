class Solution:
    def myAtoi(self, s: str) -> int:
        MAX = 2 ** 31 - 1
        MIN = -2 ** 31
        new_s = s.lstrip()
        if len(new_s) == 0:
            return 0

        ans, flag = 0, 1
        if s[0] == "+":
            new_s = new_s[1:]
        elif s[0] == "-":
            flag = -1
            new_s = new_s[1:]

        for i in new_s:
            if not i.isdigit():
                break
            else:
                ans = ans * 10 + int(i)
                if ans * flag >= MAX:
                    return MAX
                elif ans * flag <= MIN:
                    return MIN
        return ans * flag



s = Solution()
L = "   -42"
r = s.myAtoi(L)
print(r)