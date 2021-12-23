# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: ListNode):
        """
        Do not return anything, modify head in-place instead.
        """
        low_p = fast_p = head
        while fast_p.next and fast_p.next.next:
            low_p = low_p.next
            fast_p = fast_p.next.next
        end_head = self.reverse_list(low_p.next)
        low_p.next = None
        cur1, cur2 = head, end_head
        while cur1 and cur2:
            next1 = cur1.next
            next2 = cur2.next
            cur1.next = cur2
            cur2.next = next1
            cur1, cur2 = next1, next2
        return head


    def reverse_list(self, head):
        cur = head
        prv = None
        while cur:
            _next = cur.next
            cur.next = prv
            prv = cur
            cur = _next
        return prv


s = Solution()
n = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))

c = s.reorderList(n)

print(c)