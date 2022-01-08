from typing import List


class Solution:

    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board:
            return False
        visited = set()

        # 上 右 下 左
        steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        def in_area(i, j):
            return i >= 0 and i < len(board) and j >= 0 and j < len(board[0])

        def _exist(i, j, idx, board, word):

            if idx == len(word) - 1:
                return board[i][j] == word[idx]

            if board[i][j] != word[idx]:
                return False

            for x, y in steps:
                new_i = i + x
                new_j = j + y
                if in_area(new_i, new_j):
                    return _exist(new_i, new_j, idx + 1, board, word)

        for i in range(len(board)):
            for j in range(len(board[0])):
                if _exist(i, j, 0, board, word):
                    return True

        return False


board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]


word = "ABFC"

s = Solution()
r = s.exist(board, word)
print(r)
