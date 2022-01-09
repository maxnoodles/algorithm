


def LIS(nums):
    """
        状态转移方程
        LIS(i) 表示以第 i 个数结尾的最长上升子序列
        状态转移方程
        LIS(i) = max(1 + LIS(j) if nums[i] > nums[j])  # j < i
    """
    if not nums:
        return 0
    ret = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                ret[i] = max(ret[i], 1 + ret[j])

    return max(ret)


n = [0,1,0,3,2,3]
r = LIS(n)
print(r)
