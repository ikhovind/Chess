class Board:
    board = [
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    def __init__(self):
        return

    def __str__(self) -> str:
        answer = ""
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == "":
                    answer += " "
                else:
                    answer += self.board[i][j]
            if(i < 7):
                answer += "\n"
        return answer
