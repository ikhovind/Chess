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
        if(move.upper() == "Z"):
            quit(0)
        if ord(move[0]) in range(ord("A"), ord("H") + 1):
            if int(move[1]) in range(1, 9):
                break
            else:
                print("invalid from row")
        else:
            print("invalid from column")
    return move

while True:
    print(b.__str__())
    print(("White " if(whiteturn) else "Black ") + "to move")
    movefrom = getinputsquare("Enter square to move from")
    moveto = getinputsquare("Enter square to move to")
    if (b.isPieceWhite(movefrom) == whiteturn) or not b.move(movefrom, moveto):
        print("invalid move, try again")
    else:
        if(b.isCheckMate(not whiteturn)):
            print("Checkmate, " + "white won" if (whiteturn) else "black won")
            quit(1)
        whiteturn = not whiteturn