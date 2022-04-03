from typing import List


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def heapsort(arr):
            n = len(arr)
            # heapify 从最后一个非叶子几点开始堆化
            for i in range(n//2-1, -1, -1):
                shift_down(arr, n, i)

            for i in range(n-1, 0, -1):
                arr[0], arr[i] = arr[i], arr[0]
                # 每次交互完 n 会减 1，也就是等于 i
                shift_down(arr, i, 0)

        def shift_down(arr, n, i):
            # 对长度为 n 的 arr 中第 i 个元素堆化
            while (i * 2 + 1 < n):
                l = i * 2 + 1
                r = l + 1
                if r < n and arr[r] > arr[l]:
                    l = r
                if arr[i] >= arr[l]:
                    return
                arr[i], arr[l] = arr[l], arr[i]
                i = l

        heapsort(nums)
        return nums


s = Solution()
L = [3,2,1,5,6,4, 7]
r = s.sortArray(L)
print(r)
