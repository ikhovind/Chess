from Board import Board

b = Board()

b.move("A2", "A4")
b.move("A1", "A3")
#b.move("A3", "D3")
b.move("E7", "E5")
b.move("E8", "E7")
b.move("E7", "D6")
b.move("A3", "D3")
b.move("D6", "C5")

print(b.__str__())
