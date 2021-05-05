from dataclasses import dataclass, field
import sys
import cProfile



hash_pool = dict()


@dataclass
class Node:
    value: int
    child: dict = field(default_factory=dict)
    last_child: str = None
    fina: bool = False
    freeze: bool = False
    flag: str = ''

    def node_hash(self):
        h = "1" if self.fina else "0"
        if self.child:
            h += ''.join(sorted(self.child.keys()))
        return h

    def mini_node(self):
        return (self.flag, self.value, self.fina)

@dataclass
class Builder:
    last_val: str = None
    id: int = 0
    root: Node = Node(0)
    size: int = 0

    def add(self, val):
        cur = self.root
        last_state = None
        for v in val:
            if v not in cur.child:
                self.id += 1
                cur.child[v] = Node(value=self.id, flag=v)
                if not last_state:
                    last_state = cur.child[v]
            cur = cur.child[v]
        cur.fina = True
        self.size += 1

        if last_state:
            self.replace(last_state)

    def replace(self, last_state: Node):
        for k, v in last_state.child.items():
            if v.child:
                self.replace(v)
            if (h := v.node_hash()) in hash_pool:
                last_state.child[k] = hash_pool[h]
                self.id -= 1
            else:
                hash_pool[h] = v

    def __str__(self):
        if self.root.child:
            help_str(self.root)
        return ''

    def __contains__(self, val):
        ret = self.traverse(val)
        return ret is not None and ret.fina


    def traverse(self, val):
        cur = self.root
        for i in val:
            if x:= cur.child.get(i):
                cur = x
            else:
                return None
        return cur


    def mini_list(self):
        mini = []
        queue = [self.root]
        while queue:
            cur = queue.pop(0)
            if not cur.freeze:
                mini.append(cur.mini_node())
                cur.freeze = True
            if cur.child:
                for k, v in cur.child.items():
                    queue.append(v)
        return mini





def help_str(node, t=0):
    for i, v in node.child.items():
        print(f"{'    ' * t}{i}{v.value}-{v.fina} -->", end='\n')
        help_str(v, t + 1)



if __name__ == '__main__':
    f = Builder()
    s_list = sorted(["abcd", 'bbcd', 'bgcf', 'bfce'])
    for i in s_list:
        f.add(i)
    print(f)
    print('abc' in f)
    print('bgcf' in f)
    print(f.mini_list())