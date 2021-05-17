from pychess import *

board = Board()
p1, p2 = Player(True), Player(False)
game = Game(p1, p2, board)
game.run()

# b = Board()
# f = b.boxes[0][0]
# print(b)
# f.piece = None
# print(b)
