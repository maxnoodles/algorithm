from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        symbol_map = {
            "+": lambda x, y: x+y,
            "-": lambda x, y: x-y,
            "*": lambda x, y: x*y,
            "/": lambda x, y: int(y/x),
        }
        s = []
        for i in tokens:
            if i not in symbol_map:
                s.append(i)
            else:
                tmp_ret = symbol_map[i](int(s.pop()), int(s.pop()))
                s.append(tmp_ret)
        return s[0]

s = Solution()
ret = s.evalRPN(["10","6","9","3","+","-11","*","/","*","17","+","5","+"])
print(ret)