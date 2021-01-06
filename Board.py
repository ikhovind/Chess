import re
import Pieces

class Board:
    # uppercase are black and lowercase are white
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
    # Translates from chess notation (A-H and 1-8) to array index (0-7)
    def translateLocation(self, location: str) -> tuple:
        y = int(location[1]) - 1
        # 65 is ascii value of A, converts A into 0 to get board index but still use chess notation
        x = ord(location[0]) - 65
        return (y,x)

    def isMoveBlocked(self, fromLoc: tuple, toLoc: tuple) -> bool:
        fromY = fromLoc[0]
        fromX = fromLoc[1]
        toY = toLoc[0]
        toX = toLoc[1]
        piece = self.board[fromY][fromX].upper()

        movedPiece = self.board[fromLoc[0]][fromLoc[1]]
        takenPiece = self.board[toLoc[0]][toLoc[1]]

        # Cannot take a piece of the same color
        if takenPiece != "":
            if movedPiece.isupper() == takenPiece.isupper():
                return True


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
                x = fromX + (1 if (toX > fromX) else -1)
                for y in range(fromY + (1 if (toY > fromY) else -1), toY, 1 if (toY > fromY) else -1):
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

    def isKingInCheck(self, whiteKing: bool):
        kingLoc = (-1,-1)
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                # if it is the king and has the same colour as parameter
                if piece.upper() == "K" and piece.isupper() != whiteKing:
                    kingLoc = (y,x)
        for a in range(0,8):
            for b in range(0,8):
                piece = self.board[a][b]
                # if the piece is upper case then it is black and can check the white king
                # if the piece is lowercase then it is white and can check the black king
                if piece.isupper() == whiteKing and self.isMoveShapeLegal((a,b),kingLoc, True) and not self.isMoveBlocked((a,b), kingLoc):
                    return True
        return False

    # checks all possible moves to see if there is some way to get the king out of check
    def isanymovelegal(self, whiteKing: bool) -> bool:
        for y in range(0,8):
            for x in range(0,8):
                piece = self.board[y][x]
                # if it is upper then it is black, not upper then it is white
                if piece.isupper() != whiteKing:
                    for yy in range(0,8):
                        for xx in range(0,8):
                            # if the move is legal and not blocked and the king is not in check after the move then it is not checkmate
                            if self.isMoveShapeLegal((y, x),(yy, xx), self.board[yy][xx] != "") \
                                    and not self.isMoveBlocked((y, x),(yy, xx))  \
                                    and not self.isCheckAfterMove((y, x), (yy, xx), whiteKing):
                                return True
        return False

    # checks if the given king is in check after a hypothetical check
    def isCheckAfterMove(self, fromTuple: tuple, toTuple: tuple, whiteKing: bool) -> bool:
        temp = self.board[toTuple[0]][toTuple[1]]
        self.board[toTuple[0]][toTuple[1]] = self.board[fromTuple[0]][fromTuple[1]]
        self.board[fromTuple[0]][fromTuple[1]] = ""

        value = self.isKingInCheck(whiteKing)
        # the pieces are moved back to where they were before, but we know know if this move will put the given king in check
        self.board[fromTuple[0]][fromTuple[1]] = self.board[toTuple[0]][toTuple[1]]
        self.board[toTuple[0]][toTuple[1]] = temp
        return value

    def move(self, fromLoc: str, toLoc: str):
        fromTuple = self.translateLocation(fromLoc)
        toTuple = self.translateLocation(toLoc)

        movedPiece = self.board[fromTuple[0]][fromTuple[1]]
        takenPiece = self.board[toTuple[0]][toTuple[1]]

        # if shape is legal, if the move is not blocked and if your king is not in check after the move then the move is made
        if self.isMoveShapeLegal(fromTuple, toTuple, takenPiece != "") and not self.isMoveBlocked(fromTuple, toTuple) \
                and not self.isCheckAfterMove(fromTuple, toTuple, not movedPiece.isupper()):
            self.board[toTuple[0]][toTuple[1]] = self.board[fromTuple[0]][fromTuple[1]]
            self.board[fromTuple[0]][fromTuple[1]] = ""
            # if a pawn has reached other side of board
            if (movedPiece == "p" and toTuple[0] == 7) or (movedPiece == "P" and toTuple[0] == 0):
                # runs until a valid piece is selected
                while True:
                    upgrade = input("Enter N, B, Q or R")
                    if len(upgrade) == 1:
                        if re.search("[N,B,Q,R]", upgrade):
                            self.board[toTuple[0]][toTuple[1]] = upgrade.upper() if (movedPiece.isupper()) else upgrade.lower()
                            break
            return True
        return False

    def isPieceWhite(self, fromLoc:str) -> bool:
        fromTuple = self.translateLocation(fromLoc)
        char = self.board[fromTuple[0]][fromTuple[1]]
        return char.isupper()

    def isGameStalemate(self, white: bool):
        return not self.isanymovelegal(white) and not self.isKingInCheck(white)

    def isLackOfMaterial(self):
        #checkmate cannot be achieved by only knight or bishop alone, but all other pieces are sufficient
        checkmatedict =  {
            "N" : 1,
            "K" : 0,
            "B" : 1,
            "R" : 2,
            "P" : 2,
            "Q" : 2
        }
        whitePieces = 0
        blackPieces = 0
        for y in range(0, 8):
            for x in range(0, 8):
                piece = self.board[y][x]
                if (piece.isupper()):
                    blackPieces += checkmatedict.get(piece.upper())
                else:
                    whitePieces += checkmatedict.get(piece.upper())
                if blackPieces > 1 or whitePieces > 1:
                    return False
        return True
    def __str__(self) -> str:
        answer = ""
        for i in range(7, -1, -1):
            for j in range(0, 8):
                if self.board[i][j] == "":
                    answer += "        "
                else:
                    answer += Pieces.PT[self.board[i][j]].value + "      "
            answer += "\n"
        return answer

