from typing import List


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

class Solution:
    def preorder(self, root: 'Node') -> List[int]:
        if not root:
            return []
        res = [root.val]
        if root.children:
            for i in root.children:
                res += self.preorder(i)
        return res


a = Node(3, [Node(4, [Node(5)])])

s = Solution()
ret = s.preorder(a)
print