from dataclasses import dataclass, field

hash_pool = dict()


@dataclass
class Node:
    id: int = 0
    char: str = ''
    value: int = 0
    child: dict = field(default_factory=dict)
    final: int = 0
    encoded: int = 0
    freeze: int = 0

    def node_hash(self):
        h = "1" if self.final else "0"
        h += self.char
        if self.child:
            h += ''.join(sorted(self.child.keys()))
        return h

    def mini_node(self, next, ):
        return [self.char, len(self.child), self.final, next if not self.final else 0, ]


@dataclass
class Builder:
    last_val: str = None
    id: int = 1
    root: Node = Node(0)
    size: int = 0

    def add(self, word, val=0):
        cur = self.root
        last_state = None
        for w in word:
            if w not in cur.child:
                if not last_state:
                    last_state = cur
                    print(last_state)
                    self.replace(last_state)
                cur.child[w] = Node(self.id, w, val)
                val = 0
                self.id += 1
            else:
                com = min(cur.child[w].value, val)
                node = cur.child[w]
                if val < node.value and val:
                    for v in node.child.values():
                        v.value = node.value - com
                    node.value = com
                else:
                    val = val - com
            cur = cur.child[w]
        cur.final = 1
        self.size += 1

    def replace(self, last_state: Node):
        for k, v in last_state.child.items():
            if v.freeze:
                continue
            if v.child:
                self.replace(v)
            if (h := v.node_hash()) in hash_pool:
                last_state.child[k] = hash_pool[h]
                self.id -= 1
            else:
                hash_pool[h] = v
            v.freeze = True

    def __str__(self):
        if self.root.child:
            help_str(self.root)
        return ''

    def __contains__(self, val):
        ret = self.traverse(val)
        return ret is not None and ret.final

    def traverse(self, val):
        cur = self.root
        for i in val:
            if x := cur.child.get(i):
                cur = x
            else:
                return None
        return cur

    def mini_list(self):
        mini = []
        count = 1
        queue = [self.root]
        while queue:
            cur = queue.pop(0)
            if cur.child:
                for k, v in cur.child.items():
                    if not v.encoded:
                        queue.append(v)
                        v.encoded = True
                    else:
                        count -= 1
            mini.append(cur.mini_node(count))
            count += len(cur.child)

        return mini


def help_str(node, t=0):
    for i, v in node.child.items():
        print(f"{'    ' * t}{i}{v.value}-{v.final} -->", end='\n')
        help_str(v, t + 1)



@dataclass
class MiniNode:
    value: int = 0
    final: int = 0
    child: dict = field(default_factory=dict)


class MiniTree:
    root: MiniNode = MiniNode()

    def decode(self, mini_arr):
        return decode_help(self.root, mini_arr, 0)

    def __str__(self):
        if self.root.child:
            help_str(self.root)
        return ''


def decode_help(node, mini_arr, mini_index):
    key, child_num, fina, next_index = mini_arr[mini_index]
    if child_num == 0:
        child_num += 1
    for i in range(0, child_num):
        c_key, _, c_fina, c_next_index = mini_arr[next_index+i]
        node.child[c_key] = MiniNode(final=c_fina)
        if c_fina == 1:
            continue
        decode_help(node.child[c_key], mini_arr, next_index+i)


def mini_tree(mini_arr):
    t = MiniTree()
    t.decode(mini_arr)
    print(t)


if __name__ == '__main__':
    f = Builder()
    s_list = sorted(['abcd', 'bbcd', 'bfce', 'bgce', 'bgcf'])
    value = [20, 10, 5, 2, 1]
    # s_list = sorted(["CGCGAAA", 'CGCGATA', 'CGGAAA', 'CGGATA', 'GGATA', "AATA"])
    for i, v in enumerate(s_list):
        f.add(v, value[i])
    print(f, f.id)
    # print('abc' in f)
    # print('bgcf' in f)
    # mini_list = f.mini_list()
    # for e, i in enumerate(mini_list):
    #     print(e, i)
    # m = mini_tree(mini_list)
    # print(m)