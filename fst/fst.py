from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    count: int = 0
    value: Any = 0
    children: dict = field(default_factory=dict)
    fina: bool = False
    weight: int = 0
    freeze = 0


class FST:
    def __init__(self):
        self.root = Node()
        self.freeze = list()
        self.unfreeze = dict()
        self.last_key = ''
        self._size = 0
        self.freeze_tag = 0
        self.last_count = 0


    def get_size(self):
        return self._size

    def fz(self, node):
        help_free(node)

    def add(self, world):
        self.freeze_tag = 0
        cur = self.root
        for char in world:
            if not cur.children.get(char):
                if not self.freeze_tag:
                    self.fz(cur)
                self.last_count += 1
                cur.children[char] = Node(count=self.last_count)
            cur = cur.children[char]
        if not cur.fina:
            cur.fina = True
            self._size += 1
        self.last_key = world[0]

    def __str__(self):
        if self.root.children:
            help_str(self.root)
        return ''

def help_str(node, t=0):
    for i, v in node.children.items():
        print(f"{'    '*t}{i}{v.freeze} {v.count} -->", end='\n')
        help_str(v, t+1)


def help_free(node: Node):
    for i, v in node.children.items():
        v.freeze = 1
        help_free(v)



if __name__ == '__main__':
    f = FST()
    s_list = sorted(["abcd", 'bbcd', 'bgcf', 'bfce'])
    for i in s_list:
        f.add(i)
    print(f)


