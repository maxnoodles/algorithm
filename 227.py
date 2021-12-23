class Solution:
    def calculate(self, s: str) -> int:
        low_map = {
            "+": lambda x: x,
            "-": lambda x: -x,
        }
        height_map = {
            "*": lambda x, y: x*y,
            "/": lambda x, y: int(x/y),
        }
        stack = [int(s[0])]
        tmp_symbol = '+'
        prv_s = ''
        for i in s:
            if i == ' ':
                continue
            elif i in '+-*/':
                tmp_symbol = i
            else:
                i = int(i)
                if tmp_symbol in low_map:
                    val = low_map[tmp_symbol](i)
                    if prv_s not in '+-*/':
                        val += stack.pop()*10
                    stack.append(val)
                else:
                    stack.append(height_map[tmp_symbol](stack.pop(), i))
            prv_s = str(i)
        return sum(stack)

class Solution2:
    def calculate(self, s: str) -> int:
        n = len(s)
        stack = []
        preSign = '+'
        num = 0
        for i in range(n):
            if s[i] != ' ' and s[i].isdigit():
                num = num * 10 + ord(s[i]) - ord('0')
            if i == n - 1 or s[i] in '+-*/':
                if preSign == '+':
                    stack.append(num)
                elif preSign == '-':
                    stack.append(-num)
                elif preSign == '*':
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))
                preSign = s[i]
                num = 0
        return sum(stack)


s = Solution2()
r = s.calculate("9/10")
print(r)
