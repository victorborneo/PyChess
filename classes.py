import pygame

class Board:
    def __init__(self):
        self.turn = 0
        self.image = pygame.image.load(".\\Pieces\\board.png")
        self.board = self.start()

    def start(self):
        board = []

        for i in range(8):
            line = []

            for j in range(8):
                x = 25 + j * 72
                y = 10 + i * 71

                to_append = [(x, y), 0]
                if i == 0 or i == 7:
                    if i == 0:
                        color = ".\\Pieces\\black"
                        team = 1
                    else:
                        color = ".\\Pieces\\white"
                        team = 0

                    if j == 0 or j == 7:
                        to_append = [(x, y), Rook(team, f"{color}_rook.png")]
                    elif j == 1 or j == 6:
                        to_append = [(x, y), Knight(team, f"{color}_knight.png")]
                    elif j == 2 or j == 5:
                        to_append = [(x, y), Bishop(team, f"{color}_bishop.png")]
                    elif j == 3:
                        to_append = [(x, y), Queen(team, f"{color}_queen.png")]
                    else:
                        to_append = [(x, y), King(team, f"{color}_king.png")]

                elif i == 1:
                    to_append = [(x, y), Pawn(1, ".\\Pieces\\black_pawn.png")]

                elif i == 6:
                    to_append = [(x, y), Pawn(0, ".\\Pieces\\white_pawn.png")]

                line.append(to_append)
            board.append(line)

        return board

class Piece:
    def __init__(self, value, team, image):
        self.value = value
        self.team = team
        self.image = pygame.image.load(image)

class Pawn(Piece):
    def __init__(self, team, image):
        super().__init__(1, team, image)

    def get_moves(self, pos_x, pos_y, board):
        moves = []
    
        increment = -1
        if self.team == 1:
            increment = 1

        if board[pos_y + increment][pos_x][1] == 0:
            moves.append((pos_y + increment, pos_x))

            if self.team == 0 and pos_y == 6 and board[pos_y - 2][pos_x][1] == 0:
                moves.append((pos_y - 2, pos_x))

            if self.team == 1 and pos_y == 1 and board[pos_y + 2][pos_x][1] == 0:
                moves.append((pos_y + 2, pos_x))

        if pos_x - 1 >= 0 and board[pos_y + increment][pos_x - 1][1] != 0 and \
                board[pos_y + increment][pos_x - 1][1].team != self.team:
            moves.append((pos_y + increment, pos_x - 1))

        if pos_x + 1 < 8 and board[pos_y + increment][pos_x + 1][1] != 0 and \
                board[pos_y + increment][pos_x + 1][1].team != self.team:
            moves.append((pos_y + increment, pos_x + 1))

        return moves

class Rook(Piece):
    def __init__(self, team, image):
        super().__init__(5, team, image)

    def get_moves(self, pos_x, pos_y, board):
        moves = []

        for i in range(7 - pos_x):
            try:
                if board[pos_y][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y, pos_x + i + 1))

        for i in range(pos_x):
            try:
                if board[pos_y][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y, pos_x - i - 1))

        for i in range(7 - pos_y):
            try:
                if board[pos_y + i + 1][pos_x][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x))

        for i in range(pos_y): 
            try:
                if board[pos_y - i - 1][pos_x][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x))

        return moves

class Knight(Piece):
    def __init__(self, team, image):
        super().__init__(3, team, image)

    def get_moves(self, pos_x, pos_y, board):
        moves = []
        sequences = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))

        for move in sequences:
            try:
                if board[pos_y + move[0]][pos_x + move[1]][1].team != self.team:
                    moves.append((pos_y + move[0], pos_x + move[1]))
            except AttributeError:
                moves.append((pos_y + move[0], pos_x + move[1]))
            except IndexError:
                pass

        return moves

class Bishop(Piece):
    def __init__(self, team, image):
        super().__init__(3, team, image)

    def get_moves(self, pos_x, pos_y, board):
        moves = []

        for i in range(7 - pos_x):
            try:
                if board[pos_y + i + 1][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x + i + 1))
            except IndexError:
                break

        for i in range(pos_x):
            try:
                if board[pos_y - i - 1][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x - i - 1))
            except IndexError:
                break

        for i in range(7 - pos_y):
            try:
                if board[pos_y + i + 1][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x - i - 1))
            except IndexError:
                break

        for i in range(pos_y): 
            try:
                if board[pos_y - i - 1][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x + i + 1))
            except IndexError:
                break

        return moves

class Queen(Piece):
    def __init__(self, team, image):
        super().__init__(9, team, image)

    def get_moves(self, pos_x, pos_y, board):
        moves = []

        for i in range(7 - pos_x):
            try:
                if board[pos_y][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y, pos_x + i + 1))

        for i in range(pos_x):
            try:
                if board[pos_y][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y, pos_x - i - 1))

        for i in range(7 - pos_y):
            try:
                if board[pos_y + i + 1][pos_x][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x))

        for i in range(pos_y): 
            try:
                if board[pos_y - i - 1][pos_x][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x))

        for i in range(7 - pos_x):
            try:
                if board[pos_y + i + 1][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x + i + 1))
            except IndexError:
                break

        for i in range(pos_x):
            try:
                if board[pos_y - i - 1][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x - i - 1))
            except IndexError:
                break

        for i in range(7 - pos_y):
            try:
                if board[pos_y + i + 1][pos_x - i - 1][1].team != self.team:
                    moves.append((pos_y + i + 1, pos_x - i - 1))
                break
            except AttributeError:
                moves.append((pos_y + i + 1, pos_x - i - 1))
            except IndexError:
                break

        for i in range(pos_y): 
            try:
                if board[pos_y - i - 1][pos_x + i + 1][1].team != self.team:
                    moves.append((pos_y - i - 1, pos_x + i + 1))
                break
            except AttributeError:
                moves.append((pos_y - i - 1, pos_x + i + 1))
            except IndexError:
                break

        return moves

class King(Piece):
    def __init__(self, team, image):
        super().__init__(0, team, image)
    
    def get_moves(self, pos_x, pos_y, board):
        moves = []
        sequences = ((1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1))

        for move in sequences:
            try:
                if board[pos_y + move[0]][pos_x + move[1]][1].team != self.team:
                    moves.append((pos_y + move[0], pos_x + move[1]))
            except AttributeError:
                moves.append((pos_y + move[0], pos_x + move[1]))
            except IndexError:
                pass

        return moves
