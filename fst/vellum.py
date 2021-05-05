from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class defaultBuilderOpts:
    Encoder: int = 1
    RegistryTableSize: int = 10000
    RegistryMRUSize: int = 2


@dataclass
class transition:
    out: int = 0
    addr: int = 0
    _in: int = 0


@dataclass
class builderNode:
    final_out_put: int = 0
    trans: list = field(default_factory=list)
    final: bool = False
    next: Optional["builderNode"] = None

    def reset(self):
        self.final = False
        self.final_out_put = 0
        for i in range(0, len(self.trans)):
            self.trans[i] = transition()
        self.trans = self.trans[:0]
        self.next = None

@dataclass
class builderNodeUnfinished:
    node: builderNode
    listOut: int
    lastIn: bytes
    has_last_t: bool

@dataclass
class builderNodePool:
    head = builderNode()

    def get(self):
        if not self.head:
            return builderNode()
        head = self.head
        self.head = self.head.next
        return head

    def put(self, node):
        if node:
            node.reset()
            node.next = self.head
            self.head = node

@dataclass
class unfinishedNodes:
    builderNodePool: builderNodePool
    stack: List[builderNodeUnfinished] = field(default_factory=list)
    cache: List[builderNodeUnfinished] = field(default_factory=list)

    def push_empty(self, final):
        next = self.get()
        next.node = self.builder_node_pool.get()
        next.node.final = final

    def get(self):
        if len(self.stack) < len(self.cache):
            return self.cache[len(self.stack)]
        return builderNodeUnfinished()


@dataclass
class registry:
    builderNodePool: builderNodePool
    tablseSize: int
    mrusize: int
    table: list = field(default_factory=list)


@dataclass
class registryCell:
    addr: int
    node: builderNode


def newRegistry(p, tableSize, mruSize):
    nsize = tableSize * mruSize
    return registry(p, tableSize, mruSize, [])



def newUnfinishedNodes(pool):
    rv = unfinishedNodes(
        builderNodePool=pool,
        stack=list(),
        cache=list(),
    )
    rv.push_empty(False)
    return rv

@dataclass
class Builder:
    unfinished: newUnfinishedNodes
    registry: registry
    pool: builderNodePool
    # encoder: encoder
    opts: defaultBuilderOpts
    last: list = field(default_factory=list)
    len: int = 0
    last_addr: int = 0


def newBuilder(w):
    opt = defaultBuilderOpts()
    pool = builderNodePool()
    return Builder(
        unfinished=newUnfinishedNodes(pool),
        registry=newRegistry(pool, opt.RegistryTableSize, opt.RegistryMRUSize),
        pool=pool,
        opts=opt,
        last_addr=0
    )
