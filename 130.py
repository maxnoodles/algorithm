class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        if not board:
            return board

        step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        w, l = len(board), len(board[0])

        def in_area(i, j):
            if 0 <= i < w and 0 <= j < l:
                return True
            return False

        def dfs(i, j):
            if in_area(i, j) and board[i][j] == "O":
                board[i][j] = "A"
                for x, y in step:
                    new_i = i + x
                    new_j = j + y
                    dfs(new_i, new_j)

        for i in range(w):
            dfs(i, 0)
            dfs(i, l - 1)

        for j in range(l):
            dfs(0, j)
            dfs(w - 1, j)

        for i in range(w):
            for j in range(l):
                if board[i][j] == "A":
                    board[i][j] = "O"
                else:
                    board[i][j] = "X"
