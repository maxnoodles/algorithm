from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Stream():
    first: Any
    compute_fun: Callable
    empty: bool = False
    ret: Any = None
    computed: bool = False

    @property
    def next(self) -> Any:
        assert not self.empty
        if not self.computed:
            self.ret = self.compute_fun()
            self.computed = True
            print(f"!!!no use cache: {self.ret}")
        return self.ret

    def __repr__(self):
        if self.empty:
            return '<empty stream>'
        return f'Stream({self.first}, <compute_rest>)'


def is_add(num: int) -> bool:
    return num / 2 != 0


def stream_ref(stream: Stream, n: int) -> Any:
    if stream.empty:
        return stream
    if n == 0:
        return stream.first
    return stream_ref(stream.next, n - 1)



def make_int_stream(start: int=0) -> Stream:
    def compute() -> Stream:
        return make_int_stream(start+1)
    return Stream(start, compute)


# def st(func):
#     def wrapper(*args, **kwargs):
#         def real_func():
#             return func(*args, **kwargs)
#         return real_func
#     return wrapper
#
# @st
# def _make_int_stream(start: int=0):
#     return Stream(start, _make_int_stream(start+1))
# a = _make_int_stream(0)


def make_enum_int(low: int, high: int) -> Stream:
    def compute() -> Stream:
        if low > high:
            return Stream(low, compute, empty=True)
        else:
            return make_enum_int(low+1, high)
    return Stream(low, compute)



def stream_map(stream: Stream, proc: Callable) -> Stream:
    if stream.empty:
        return stream
    def compute():
        return stream_map(stream.next, proc)
    return Stream(proc(stream.first), compute)


def stream_filter(stream: Stream, proc: Callable):
    if stream.empty:
        return stream
    def compute():
        return stream_filter(stream.next, proc)
    if proc(stream.first):
        return Stream(stream.first, compute)
    return compute()


b = make_enum_int(10, 100)
# print(stream_ref(a(), 5))
# x = make_int_stream()
# print(stream_ref(x, 5))
# print(stream_ref(b, 155))
# print(stream_ref(b, 155))

x = stream_filter(b, lambda i: i>50)
print(x.first)