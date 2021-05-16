from dataclasses import dataclass, field

hash_pool = dict()


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


@dataclass
class fst:
    root = None

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


@dataclass
class Builder(fst):
    last_val: str = None
    id: int = 1
    root: Node = Node()
    size: int = 0
    next: int = 0

    def __setitem__(self, word, val=0):
        cur = self.root
        last_state = None
        for w in word:
            if w not in cur.child:
                # 在下一次插入前，冻结上一个节点
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



    def mini_list(self):
        mini = []
        count = 0
        queue = [self.root]
        node_set = set()
        node_set.add(self.root.node_hash())
        count += len(self.root.child)
        while queue:
            # print(node_set)
            cur = queue.pop(0)
            node_set.remove(cur.node_hash())
            if cur.child:
                keys = list(cur.child.keys())
                last_edge = 0
                for k, v in cur.child.items():
                    # 相同的边子节点一样
                    if v.node_hash() in node_set:
                        count -= 1
                    else:
                        queue.append(v)
                    if k == keys[-1]:
                        last_edge = 1
                    yield [k, last_edge, cur.edge[k], count if not v.final else 0]
                    node_set.add(v.node_hash())
                    count += 1
                count += len(v.child)
                # 减去每个节点最后一条边
                count -= 1
        return mini

    def to_file(self):
        with open('mini.txt', 'w+', encoding='utf8') as f:
            for i in self.mini_list():
                f.write(str(i) + '\n')


def help_str(node, t=0):
    for i, v in node.child.items():
        print(f"{'    ' * t}{i}{getattr(v, 'id', '')}-{node.edge[i]}-{v.final} -->", end='\n')
        help_str(v, t + 1)


@dataclass
class MiniNode(fst):
    value: int = 0
    final: int = 0
    child: dict = field(default_factory=dict)
    edge: dict = field(default_factory=dict)


class MiniTree:
    root: MiniNode = MiniNode()

    def decode(self, mini_arr):
        return decode_help(self.root, mini_arr, 0, True)

    def __str__(self):
        if self.root.child:
            help_str(self.root)
        return ''


def decode_help(node, mini_arr, mini_index, first):
    if not first and mini_index == 0:
        return
    for mini in mini_arr[mini_index:]:
        key, last_edge, edge_value, next_index = mini
        node.child[key] = MiniNode(final=0 if next_index else 1)
        node.edge[key] = edge_value
        if next_index == 0 and last_edge == 1:
            break
        decode_help(node.child[key], mini_arr, next_index, False)
        if last_edge == 1:
            break


def mini_tree(mini_arr):
    t = MiniTree()
    t.decode(mini_arr)
    print(t)


if __name__ == '__main__':
    f = Builder()
    s_list = sorted(['abcd', 'bbcd', 'bfce', 'bgce', 'bgcf'])
    # s_list = ['bbcd', 'abcd', 'bfce', 'bgce', 'bgcf']
    value = [20, 10, 5, 2, 1]
    for i, v in enumerate(s_list):
        f[v] = value[i]
    print(f)
    print(f['bfce'])
    # print('abc' in f)
    # print('bgcf' in f)
    mini_list = list(f.mini_list())
    for e, i in enumerate(mini_list):
        print(e, i)
    f.to_file()
    m = mini_tree(mini_list)
    print(m)
