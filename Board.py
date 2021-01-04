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

    def translateLocation(self, location: str) -> tuple:
        y = int(location[1]) - 1
        x = ord(location[0]) - 65
        return (y,x)

    def isMoveBlocked(self, fromLoc: tuple, toLoc: tuple) -> bool:
        fromY = fromLoc[0]
        fromX = fromLoc[1]
        toY = toLoc[0]
        toX = toLoc[1]
        piece = self.board[fromY][fromX].upper()

        if piece != "N":
            if toX - fromX == 0:
                for y in range(fromY + (1 if (toY > fromY) else -1), toY, 1 if (toY > fromY) else -1):
                    if self.board[y][fromX] != "":
                        return True
            elif toY - fromY == 0:
                for x in range(fromX + (1 if (toX > fromX) else -1), toX, 1 if (toX > fromX) else -1):
                    if self.board[fromY][x] != "":
                        return True
            else:
                for y in range(fromY + (1 if (toY > fromY) else -1), toY, 1 if (toY > fromY) else -1):
                    x = fromX + (1 if (toX > fromX) else -1)
                    if self.board[y][x] != "":
                        return True
                    x += 1
        return False

    # Assumes that the locations are valid locations on the board
    def isMoveShapeLegal(self, fromTuple: tuple, toTuple: tuple, takes: bool) -> bool:
        fromY = fromTuple[0]
        fromX = fromTuple[1]
        toY = toTuple[0]
        toX = toTuple[1]
        piece = self.board[fromY][fromX]
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
            if (abs(fromX - toX) == 1) :
                # horizontal move or diagonal move
                if((abs(fromY - toY) == 1) or (abs(fromY - toY) == 0)):
                    return True
            if (abs(fromY - toY) == 1):
                # vertical move
                if (abs(fromX - toX) == 0):
                    return True
            else:
                return False
        # if the pawn is white
        if piece == "p":
            if not takes and fromY - toY == -1 and fromX == toX:
                return True
            if not takes and fromY == 1 and fromY - toY == -2 and fromX == toX:
                return True
            if takes and fromY - toY == -1 and abs(fromX - toX) == 1:
                return True
        # if the pawn is black
        if piece == "P":
            if not takes and fromY - toY == 1 and fromX == toX:
                return True
            if not takes and fromY == 6 and fromY - toY == 2 and fromX == toX:
                return True
            if takes and fromY - toY == 1 and abs(fromX - toX) == 1:
                return True
        return False

    #TODO make it possible but not necessary to have kingLoc as a parameter
    def isKingInCheck(self, whiteKing: bool):
        kingLoc = (-1,-1)
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                if piece.upper() == "K" and piece.isupper() != whiteKing:
                    kingLoc = (y,x)
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                # if the piece is upper case then it is black and can check the white king
                # if the piece is lowercase then it is white and can check the black king
                if piece.isupper() == whiteKing and self.isMoveShapeLegal((y,x),kingLoc, True) and not self.isMoveBlocked((y,x), kingLoc):
                    return True
        return False

    def isCheckMate(self, whiteKing: bool) -> bool:
        kingLoc = (-1,-1)
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                if piece.upper() == "K" and piece.isupper() != whiteKing:
                    kingLoc = (y,x)
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                if(piece.isupper() != whiteKing):
                    for yy in range(0,8):
                        for xx in range(0,8):
                            if self.isMoveShapeLegal((y,x),(yy,xx), self.board[yy][xx] != "") and self.isMoveBlocked((y,x),(yy,xx))  and not (self.isCheckAfterMove((y,x),(yy,xx),whiteKing)):
                                return False
        return True

    def isCheckAfterMove(self, fromTuple: tuple, toTuple: tuple, whiteKing: bool):
        value = False
        movedPiece = self.board[fromTuple[0]][fromTuple[1]]
        # 65 is ascii value of A, converts A into 0 to get board index but still use chess notation
        temp = self.board[toTuple[0]][toTuple[1]]
        self.board[toTuple[0]][toTuple[1]] = self.board[fromTuple[0]][fromTuple[1]]
        self.board[fromTuple[0]][fromTuple[1]] = ""
        # if the king is in check after the move then the move is invalid
        value = self.isKingInCheck(whiteKing)
        self.board[fromTuple[0]][fromTuple[1]] = self.board[toTuple[0]][toTuple[1]]
        self.board[toTuple[0]][toTuple[1]] = temp
        return value


    def move(self, fromLoc: str, toLoc: str):
        fromTuple = self.translateLocation(fromLoc)
        toTuple = self.translateLocation(toLoc)

        movedPiece = self.board[fromTuple[0]][fromTuple[1]]
        takenPiece = self.board[toTuple[0]][toTuple[1]]

        # Cannot take a piece of the same color
        if takenPiece != "":
            if movedPiece.isupper() == takenPiece.isupper():
                return

        if self.isMoveShapeLegal(fromTuple, toTuple, takenPiece != "") and not self.isMoveBlocked(fromTuple, toTuple) and not self.isCheckAfterMove(fromTuple, toTuple, not movedPiece.isupper()):
            # 65 is ascii value of A, converts A into 0 to get board index but still use chess notation
            self.board[toTuple[0]][toTuple[1]] = self.board[fromTuple[0]][fromTuple[1]]
            self.board[fromTuple[0]][fromTuple[1]] = ""

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
