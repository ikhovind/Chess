class Board:
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    def __init__(self):
        return

    # Assumes that the locations are valid locations on the board
    def isMoveShapeLegal(self, fromLoc: str, toLoc: str) -> bool:
        fromY = int(fromLoc[1]) - 1
        fromX = ord(fromLoc[0]) - 65
        toY = int(toLoc[1]) - 1
        toX = ord(toLoc[0]) - 65
        piece = self.board[int(fromLoc[1]) - 1][ord(fromLoc[0]) - 65]
        upperPiece = piece.upper()
        if upperPiece == "R" or upperPiece == "Q":
            if (fromX == toX and fromY != toY) or (fromY == toY and fromX != toX):
                return True
        if upperPiece == "N":
            if ((fromX == toX - 2) or (fromX == toX + 2)) and ((fromY == toY - 1) or fromY == toY + 1):
                return True
            elif ((fromX == toX - 1) or (fromX == toX + 1)) and ((fromY == toY - 2) or fromY == toY + 2):
                return True
            else:
                return False
        if upperPiece == "B" or upperPiece == "Q":
            if abs(fromX - toX) == abs(fromY - toY) and (fromX - fromY != 0):
                return True
            else:
                return False
        if upperPiece == "K":
            if (abs(fromX - toX) == 1) or (abs(fromY - toY) == 1):
                return True
            else:
                return False
        # if the pawn is white
        if piece == "p":
            if fromY - toY == -1 and fromX == toX:
                return True
            if fromY == 1 and fromY - toY == -2 and fromX == toX:
                return True
        # if the pawn is black
        if piece == "P":
            if fromY - toY == 1 and fromX == toX:
                return True
            if fromY == 7 and fromY - toY == 2 and fromX == toX:
                return True
        return False

    def move(self, fromLoc: str, toLoc: str):
        if self.isMoveShapeLegal(fromLoc, toLoc):
            # 65 is ascii value of A, converts A into 0 to get board index but still use chess notation
            self.board[int(toLoc[1]) - 1][ord(toLoc[0]) - 65] = self.board[int(fromLoc[1]) - 1][ord(fromLoc[0]) - 65]
            self.board[int(fromLoc[1]) - 1][ord(fromLoc[0]) - 65] = ""

    def __str__(self) -> str:
        answer = ""
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == "":
                    answer += " "
                else:
                    answer += self.board[i][j]
            if (i < 7):
                answer += "\n"
        return answer
