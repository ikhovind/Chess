from Board import Board

b = Board()

b.move("E2", "E4")
b.move("F1", "C4")
b.move("D1", "F3")
b.move("F3", "F7")
print(b.isCheckMate(False))

print(b.__str__())
