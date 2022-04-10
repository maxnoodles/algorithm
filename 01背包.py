cnt = 0


def cnt_time():
    global cnt
    cnt += 1


def knapsack_01(w, v, c):
    """
        状态转移方程
        F(i, c) = F(i-1, c)
                = vi + F(i-1, c-wi)

        F(i, c) = max(F(i-1, c), vi + F(i-1, c-wi))

    """
    memo = [[-1] * (c + 1) for _ in range(len(w))]

    def _knapsack(w: list, v: list, idx: int, c: int):
        if idx < 0 or c <= 0:
            return 0

        if memo[idx][c] != -1:
            return memo[idx][c]
        cnt_time()

        # F(i-1, c)
        res = _knapsack(w, v, idx - 1, c)
        if c >= w[idx]:
            # vi + F(i-1, c-wi)
            res = max(res, v[idx] + _knapsack(w, v, idx - 1, c - w[idx]))
        memo[idx][c] = res
        return res

    return _knapsack(w, v, len(w) - 1, c)


def get_row(i):
    return i % 2


def dp_knapsack_01(w, v, c):
    """
        状态转移方程
        F(i, c) = F(i-1, c)
                = vi + F(i-1, c-wi)

        F(i, c) = max(F(i-1, c), vi + F(i-1, c-wi))

    """
    assert (len(w) == len(v))
    n = len(w)
    if n == 0:
        return 0
    # memo = [[-1]*(c+1) for _ in range(2)]
    #
    # # 先填写第一列
    # for i in range(c+1):
    #     if w[0] <= i:
    #         memo[0][i] = v[0]
    #
    # for i in range(1, n):
    #     row = get_row(i)
    #     for j in range(c+1):
    #         memo[row][j] = memo[1-row][j]
    #         if j >= w[i]:
    #             memo[row][j] = max+1) for _ in range(2)]
    #

    memo = [-1] * (c + 1)
    for i in range(c + 1):
        if w[0] <= i:
            memo[i] = v[0]

    for i in range(1, n):
        for j in range(c, -1, -1):
            if j >= w[i]:
                memo[j] = max(memo[j], v[i] + memo[j-w[i]])
    return memo[-1]


def dp_knapsack_02(ws, v, c):
    n = len(ws)
    dp = [[-1] * (c+1) for _ in range(n)]

    # 初始化第一行
    for w in range(c+1):
        if w >= ws[0]:
            dp[0][w] = v[0]


    for i in range(1, n):
        for j in range(c+1):
            if j >= ws[i]:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j - ws[i]] + v[i])
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n-1][c]




ww = [2, 2, 6, 5, 4]
vv = [6, 3, 5, 4, 6]
cc = 10
r = knapsack_01(ww, vv, cc)
r2 = dp_knapsack_02(ww, vv, cc)
r3 = dp_knapsack_01(ww, vv, cc)
print(r, r2, r3)
