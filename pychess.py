from enum import Enum

class Spot:
	def __init__(self, x, y, piece = None):
		self.piece = piece
		self.x = x
		self.y = y

	def __str__(self):
		if self.piece == None:
			return "."
		return str(self.piece)

class Piece:
	def __init__(self, isWhite):
		self.killed = False
		self.isWhite = isWhite


''' // -------- Pieces -------- // '''
class King(Piece):
	def __init__(self, isWhite):
		super(King, self).__init__(isWhite)
	
	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False
		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		if x + y == 1:
			return True

	def __str__(self):
		return chr(ord('k') - 32 * self.isWhite)

class Knight(Piece):
	def __init__(self, isWhite):
		super(Knight, self).__init__(isWhite)
	
	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False
		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		return x * y == 2

	def __str__(self):
		return chr(ord('n') - 32 * self.isWhite)

class Bishop(Piece):
	def __init__(self, isWhite):
		super(Bishop, self).__init__(isWhite)
	
	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False
		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		return x == y <= 8

	def __str__(self):
		return chr(ord('b') - 32 * self.isWhite)

class Rook(Piece):
	def __init__(self, isWhite):
		super(Rook, self).__init__(isWhite)
	
	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False

		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		if (x == 0 and y != 0 and y <= 8):
			return True
		if (y == 0 and x != 0 and x <= 8):
			return True
		return False

	def __str__(self):
		return chr(ord('r') - 32 * self.isWhite)

class Queen(Piece):
	def __init__(self, isWhite):
		super(Queen, self).__init__(isWhite)
	
	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False

		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		if (x == y or \
			(x == 0 and y != 0 and y <= 8) or \
			(x != 0 and y == 0 and x <= 8)):
			return True
		return False

	def __str__(self):
		return chr(ord('q') - 32 * self.isWhite)

class Pawn(Piece):
	def __init__(self, isWhite):
		super(Pawn, self).__init__(isWhite)
		self.stepped = False

	def canMove(self, board, start, end):
		if (end.piece and end.piece.isWhite == self.isWhite):
			return False

		x = abs(start.x - end.x)
		y = abs(start.y - end.y)
		if (x == 0 and y == 1):
			return True
		if (x == 0 and y == 2 and not self.stepped):
			return True
		return False

	def __str__(self):
		return chr(ord('p') - 32 * int(self.isWhite))

''' // ------------------------ // '''

class Board:
	def __init__(self):
		self.boxes = []
		for y in range(8):
			self.boxes.append([])
			for x in range(8):
				self.boxes[y].append(Spot(x, y))

		self.boxes[0][0].piece = Rook(False)
		self.boxes[0][1].piece = Knight(False)
		self.boxes[0][2].piece = Bishop(False)
		self.boxes[0][3].piece = Queen(False)
		self.boxes[0][4].piece = King(False)
		self.boxes[0][5].piece = Bishop(False)
		self.boxes[0][6].piece = Knight(False)
		self.boxes[0][7].piece = Rook(False)

		self.boxes[7][0].piece = Rook(True)
		self.boxes[7][1].piece = Knight(True)
		self.boxes[7][2].piece = Bishop(True)
		self.boxes[7][3].piece = Queen(True)
		self.boxes[7][4].piece = King(True)
		self.boxes[7][5].piece = Bishop(True)
		self.boxes[7][6].piece = Knight(True)
		self.boxes[7][7].piece = Rook(True)
		
		for row in (1, 6):
			for i in range(8):
				self.boxes[row][i].piece = Pawn(False if row == 1 else True)

	def __str__(self):
		res = "   A B C D E F G H  \n\n"
		for y in range(8):
			res = res + str(y + 1) + "  "
			for x in range(8):
				res = res + str(self.boxes[y][x])
				if x != 7:
					res = res + " "
			res = res + "  " + str(y + 1) + '\n'
		res =  res + "\n   A B C D E F G H  "
		
		return res

class Player:
	def __init__(self, isWhiteSide):
		self.isWhiteSide = isWhiteSide

class GameStatus(Enum):
	ACTIVE = 1
	BLACK_WIN = 2
	WHITE_WIN = 3
	FORFEIT = 4
	STALEMATE = 5
	RESIGNATION = 6

class Move:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.pieceMoved = None
		self.pieceKilled = None
	
	def __str__(self):
		return str(self.pieceMoved) + " " + chr(self.start.x + 65) + str(self.start.y) + " " + chr(self.end.x + 65) + str(self.end.y)

class Game:
	def __init__(self, p1, p2, board):
		self.mover = Moover(board)
		self.parser = CommandParser()
		self.players = [p1, p2]
		self.board = board
		self.status = GameStatus.ACTIVE
		self.turn = p1 if p1.isWhiteSide else p2
		self.moves = []

	def run(self):
		command = ""
		print("Формат ввода:\n	комманда вида '<БУКВА 1><ЧИСЛО 1>;<БУКВА 2><ЧИСЛО 2>',\n	\
где БУКВА находится в интервале от A до H (латиница),\n	\
а ЦИФРА от 1 до 8.\n	\
Для выхода введите 'q'\n")
		while ("q" not in command and self.status == GameStatus.ACTIVE):
			print(("White" if self.turn.isWhiteSide else "Black") + " turn")
			print(self.board)
			command = input()
			if ("q" in command):
				self.exit()
				return
			trajectory = self.parser.parse(command, self.board)
			if not trajectory:
				print("This move is illegal!")
				continue
			move = self.mover.move(trajectory, self.turn)
			if (move):
				self.moves.append(move)
				if (self.turn == self.players[0]):
					self.turn = self.players[1]
				else:
					self.turn = self.players[0]
			else:
				print("This move is illegal!")
	
	def exit(self):
		print("Moves done:", len(self.moves))
		for i, m in enumerate(self.moves):
			print(i, ":", m)


class CommandParser:
	def __init__(self):
		pass

	def parse(self, command, board):
		def mapCoord(char):
			if (48 <= ord(char) <= 56):
				return int(char) - 1
			if (65 <= ord(char) <= 72):
				return ord(char) - 65
			return None

		if (len(command) < 5):
			return False
		sx, sy, ex, ey = mapCoord(command[0]), mapCoord(command[1]), mapCoord(command[3]), mapCoord(command[4])
		if any(_ is None for _ in (sx, sy, ex, ey)):
			print("Wrong command syntax:", sx, sy, ex, ey)
			return False

		start = board.boxes[sy][sx]
		end = board.boxes[ey][ex]

		return { "start": start, "end" : end }

class Moover:
	def __init__(self, board):
		self.board = board

	def move(self, t, turn):
		if (t["start"].piece and \
			t["start"].piece.canMove(self.board, t["start"], t["end"]) and \
			t["start"].piece.isWhite == turn.isWhiteSide):

			res = Move(t["start"], t["end"])
			res.pieceMoved = t["start"].piece
			res.pieceKilled = t["end"] if t["end"] else None

			t["end"].piece = t["start"].piece
			t["start"].piece = None
			
			if t["end"].piece is Pawn:
				t["end"].piece.stepped = True

			return res
		return False