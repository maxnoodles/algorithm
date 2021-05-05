from __future__ import annotations

import operator
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Stream():
    first: Any
    compute_fun: Callable
    empty: bool = False
    ret: Stream = None
    computed: bool = False
    args: list = None
    kwargs: dict = None

    @property
    def next(self) -> Stream:
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



def batch_make_int_stream(start: int=0, step: int=10):
    ret = list(range(start, start + step))
    def compute() -> Stream:
        return batch_make_int_stream(start+step, step)
    return Stream(ret, compute)



# def make_int_stream(start: int=0) -> Stream:
#     batch_stream = batch_make_int_stream(start)
#     def compute() -> Stream:
#         if batch_stream.first:
#             return Stream(batch_stream.first.pop(0), compute)
#         return make_int_stream(start+1)
#     return Stream(batch_stream.first.pop(0), compute)


def make_int_stream(start: int=0) -> Stream:
    batch_stream = batch_make_int_stream(start)
    return make_int_stream_help(batch_stream)


def make_int_stream_help(batch_stream) -> Stream:
    def compute() -> Stream:
        if batch_stream.first:
            return Stream(batch_stream.first.pop(0), compute)
        return make_int_stream_help(batch_stream.next)
    return Stream(batch_stream.first.pop(0), compute)


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
        if low >= high:
            return Stream(low, compute, empty=True)
        else:
            return make_enum_int(low+1, high)
    return Stream(low, compute)


def stream_for_each(stream, proc):
    if stream.empty:
        return
    proc(stream.first)
    return stream_for_each(stream.next, proc)


def stream_map(stream: Stream, proc: Callable) -> Stream:
    if stream.empty:
        return stream
    def compute() -> Stream:
        return stream_map(stream.next, proc)
    return Stream(proc(stream.first), compute)


def stream_filter(stream: Stream, proc: Callable) -> Stream:
    if stream.empty:
        return stream
    def compute() -> Stream:
        return stream_filter(stream.next, proc)
    if proc(stream.first):
        return Stream(stream.first, compute)
    return compute()


def stream_reduce(stream: Stream, proc: Callable) -> Any:
    if stream.empty:
        return stream
    return stream_reduce_help(stream.next, proc, stream.first)


def stream_reduce_help(stream: Stream, proc: Callable, ret: Any) -> Any:
    if stream.empty:
        return ret
    return stream_reduce_help(stream.next, proc, proc(ret, stream.first))


# b = make_enum_int(0, 2)
x = make_int_stream()
print(stream_ref(x, 10))
print(stream_ref(x, 10))
for i in range(10):
    x = x.next
    print(x)

# batch_x = batch_make_int_stream(0, 10)
# print(stream_ref(batch_x, 20))
# print(stream_ref(b, 155))
# y = stream_reduce(b, operator.add)
# print(y)
# stream_for_each(b, print)
# x = stream_filter(b, lambda i: i>50)
# print(x.first)