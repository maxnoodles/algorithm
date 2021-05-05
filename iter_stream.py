from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass
class Stream():
    first: Any
    compute_fun: Callable
    empty: bool = False
    ret: Stream = None
    computed: bool = False
    args: Iterable = None

    @property
    def next(self) -> Stream:
        assert not self.empty
        if not self.computed:
            n, self.args = self.compute_fun(*self.args)
            self.ret = Stream(n, self.compute_fun, args=self.args)
            self.computed = True
            print(f"!!!no use cache: {self.ret}")
        return self.ret

    def __repr__(self):
        if self.empty:
            return '<empty stream>'
        return f'Stream({self.first}, <compute_rest>)'



def make_int_stream_2(start: int=0) -> Stream:
    return Stream(start, compute, args=(start,))


def compute(start):
    return start + 1, (start + 1, )


def stream_ref(stream: Stream, n: int) -> Any:
    while True:
        if stream.empty:
            return stream
        if n == 0:
            return stream.first
        stream = stream.next
        n = n-1


a = make_int_stream_2(0)


# b = a.next
# for i in range(1000000):
#     b = b.next
#     print(b)

x = stream_ref(a, 2000)
print(x)


