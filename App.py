from Board import Board
import argparse

b = Board()
print("Welcome to chess, see-through pieces at the bottom are white and move first\n"
      "Use A-F to denote column and 1-8 to denote row when entering moves\n"
      "Enter Z at any input to quit the game\n")

whiteturn = True


def getinputsquare(prompt: str) -> str:
    while True:
        move = input(prompt + "\n")
        if (move.upper() == "Z"):
            quit(0)
        if ord(move[0]) in range(ord("A"), ord("H") + 1):
            if int(move[1]) in range(1, 9):
                break
            else:
                print("invalid from row")
        else:
            print("invalid from column")
    return move


b.move("E2", "E4")
b.move("E7", "E5")
b.move("F1", "C4")
b.move("D1", "F3")

while True:
    print(b.__str__())
    print(("White " if (whiteturn) else "Black ") + "to move")
    movefrom = getinputsquare("Enter square to move from")
    moveto = getinputsquare("Enter square to move to")
    if (b.isPieceWhite(movefrom) == whiteturn) or not b.move(movefrom, moveto):
        print("invalid move, try again")
    else:
        whiteturn = not whiteturn
        if b.isKingInCheck(whiteturn) and not b.isanymovelegal(whiteturn):
            print("Checkmate, " + "white won" if (not whiteturn) else "black won")
            quit(1)
        if (b.isGameStalemate(whiteturn)):
            print("Stalemate " + ("white" if (whiteturn) else "black") + " has no legal moves")
            quit(2)
        if (b.isLackOfMaterial()):
            print("Game is drawn by lack of material")
            quit(3)
