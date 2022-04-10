
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        def __gt__(a, b):
            return a.val > b.val

        ListNode.__gt__ = __gt__


        heap = []
        dummy = ListNode()
        for head in lists:
            if head:
                self.heap_append(heap, head)

        cur = dummy
        while heap:
            node = self.heap_pop(heap)
            cur.next = node
            if node.next:
                self.heap_append(heap, node.next)
            cur = cur.next

        return dummy.next

    def heap_pop(self, arr):
        self.swap(arr, 0, len(arr)-1)
        ret = arr.pop()
        head = 0
        while self.l_child(head) < len(arr):
            l, r = self.l_child(head), self.r_child(head)
            if r < len(arr) and arr[r] < arr[l]:
                l = r
            if arr[l] < arr[head]:
                self.swap(arr, l, head)
                head = l
            else:
                break
        return ret


    def heap_append(self, arr, v: ListNode):
        arr.append(v)
        idx = len(arr) - 1

        while self.parent(idx) >= 0 and arr[idx] < arr[self.parent(idx)]:
            self.swap(arr, idx, self.parent(idx))
            idx = self.parent(idx)

    def parent(self, i):
        return (i-1) // 2

    def l_child(self, i):
        return i * 2 + 1

    def r_child(self, i):
        return i * 2 + 2

    def swap(self, arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]



s = Solution()
# ll = [
#     ListNode(1, ListNode(4, ListNode(5))),
#     ListNode(1, ListNode(3, ListNode(4))),
#     ListNode(2, ListNode(6)),
# ]
ll = [
    ListNode(1),
    ListNode(0),
]
r = s.mergeKLists(ll)
print(r)