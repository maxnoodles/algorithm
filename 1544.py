class Solution:
    def makeGood(self, s: str) -> str:
        ret = []
        for i in s:
            if ret:
                if i == i.lower():
                    if i.upper() == ret[-1]:
                        ret.pop()
                elif i == i.upper():
                    if i.lower() == ret[-1]:
                        ret.pop()
                else:
                    ret.append(i)
            else:
                ret.append(i)
        return ''.join(ret)


a = Solution()

ret = a.makeGood("leEeetcode")
print(ret)