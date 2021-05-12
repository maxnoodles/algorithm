from dataclasses import dataclass, field

hash_pool = dict()
# edge_map = dict()


def u(w, id):
    return f'{w}_{id}'


@dataclass
class Node:
    id: int = 0
    char: str = ''
    child: dict = field(default_factory=dict)
    final: int = 0
    encoded: int = 0
    freeze: int = 0
    edge: dict = field(default_factory=dict)

    def node_hash(self):
        h = "1" if self.final else "0"
        h += self.char
        if self.child:
            h += ''.join(sorted(self.child.keys()))
        return h

    def mini_node(self, next, edge):
        return [self.char, self.id,  edge, len(self.child), self.final, next if not self.final else 0]


@dataclass
class Builder:
    last_val: str = None
    id: int = 1
    root: Node = Node(0)
    size: int = 0

    def __setitem__(self, word, val=0):
        cur = self.root
        last_state = None
        for w in word:
            if w not in cur.child:
                if not last_state:
                    last_state = cur
                    self.replace(last_state)
                cur.child[w] = Node(self.id, w)
                cur.edge[w] = val
                val = 0
                self.id += 1
            else:
                node = cur.child[w]
                edge_val = cur.edge[w]
                com = min(edge_val, val)
                if val < edge_val:
                    for k in node.child.keys():
                        node.edge[k] += edge_val - com
                    cur.edge[w] = com
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

    def __contains__(self, item):
        ret, val = self.traverse(item)
        return ret is not None and ret.final

    def __getitem__(self, item):
        ret, val = self.traverse(item)
        return val

    def traverse(self, item):
        cur = self.root
        val = 0
        for i in item:
            if x := cur.child.get(i):
                val += cur.edge[i]
                cur = x
            else:
                return None, None
        return cur, val

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
            count += len(cur.child)

        return mini


def help_str(node, t=0):
    for i, v in node.child.items():
        print(f"{'    ' * t}{i}{v.id}-{node.edge[i]}-{v.final} -->", end='\n')
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
    for i, v in enumerate(s_list):
        f[v] = value[i]
    print(f)
    print(f['bfce'])
    # print('abc' in f)
    # print('bgcf' in f)
    mini_list = f.mini_list()
    for e, i in enumerate(mini_list):
        print(e, i)
    # m = mini_tree(mini_list)
    # print(m)
