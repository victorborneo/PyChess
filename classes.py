import pygame

class Board:
    def __init__(self):
        self.turn = 0
        self.check = 0
        self.last_move = None
        self.promotion = False
        self.black_promotion = pygame.image.load(".\\Pieces\\black_promotion.png")
        self.white_promotion = pygame.image.load(".\\Pieces\\white_promotion.png")
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
                        to_append = [(x, y), Rook(team, f"{color}_rook.png", j % 6)]
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

    def get_all_moves(self, team):
        moves = []

        y = 0
        for line in self.board:

            x = 0
            for _, row in line:
                if row != 0 and row.team == team and type(row).__name__ != "King":
                    for move in row.get_moves(x, y, self.board):
                        moves.append(move)
                x += 1
            y += 1

        return moves

    def reset_en_passant(self):
        for line in self.board:
            for _, row in line:
                if row != 0 and type(row).__name__ == "Pawn":
                    row.en_passant = False

    def check_check(self, all_moves):
        y = 0
        for line in self.board:

            x = 0
            for _, row in line:
                if row != 0 and row.team == self.turn and type(row).__name__ == "King":
                    index_x, index_y = x, y

                x += 1
            y += 1

        for move in all_moves:
            if move == (index_y, index_x):
                self.check += 1

    def get_king_legal_moves(self, x, y, all_moves):
        moves = self.board[y][x][1].get_moves(x, y, self.board, self)

        moves = [x for x in moves if x not in all_moves]

        return moves

    def get_legal_moves(self, x, y, all_moves):
        if self.check > 1:
            return []

        moves = self.board[y][x][1].get_moves(x, y, self.board, self)
        direction = self.get_attack_direction()

        moves = [x for x in moves if x in direction]

        return moves

    def get_attack_direction(self):
        moves = [self.last_move]

        y = 0
        for line in self.board:

            x = 0
            for _, row in line:
                if row != 0 and row.team == self.turn and type(row).__name__ == "King":
                    index_x, index_y = x, y

                x += 1
            y += 1

        horizontal_distance = self.last_move[1] - index_x
        vertical_distance = self.last_move[0] - index_y

        if vertical_distance == 0:
            if horizontal_distance > 0:
                for i in range(1, horizontal_distance):
                    moves.append((index_y, index_x + i))
            else:
                for i in range(1, abs(horizontal_distance)):
                    moves.append((index_y, index_x - i))
        elif horizontal_distance == 0:
            if vertical_distance > 0:
                for i in range(1, vertical_distance):
                    moves.append((index_y + i, index_x))
            else:
                for i in range(1, abs(vertical_distance)):
                    moves.append((index_y - i, index_x))
        else:
            if vertical_distance > 0 and horizontal_distance > 0:
                for i in range(1, vertical_distance):
                    moves.append((index_y + i, index_x + i))
            elif vertical_distance < 0 and horizontal_distance < 0:
                for i in range(1, abs(vertical_distance)):
                    moves.append((index_y - i, index_x - i))
            elif vertical_distance > 0 and horizontal_distance < 0:
                for i in range(1, vertical_distance):
                    moves.append((index_y + i, index_x - i))
            else:
                for i in range(1, horizontal_distance):
                    moves.append((index_y - i, index_x + i))

        return moves

class Piece:
    def __init__(self, value, team, image):
        self.value = value
        self.team = team
        self.image = pygame.image.load(image)

class Pawn(Piece):
    def __init__(self, team, image):
        super().__init__(1, team, image)
        self.en_passant = False

    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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

        if pos_x - 1 >= 0:
            if (board[pos_y + increment][pos_x - 1][1] != 0 and board[pos_y + increment][pos_x - 1][1].team != self.team) or \
                (board[pos_y][pos_x - 1][1] != 0 and board[pos_y][pos_x - 1][1].team != self.team and \
                    type(board[pos_y][pos_x - 1][1]).__name__ == "Pawn" and board[pos_y][pos_x - 1][1].en_passant):
                moves.append((pos_y + increment, pos_x - 1))

        if pos_x + 1 < 8:
            if (board[pos_y + increment][pos_x + 1][1] != 0 and board[pos_y + increment][pos_x + 1][1].team != self.team) or \
                (board[pos_y][pos_x + 1][1] != 0 and board[pos_y][pos_x + 1][1].team != self.team and \
                    type(board[pos_y][pos_x + 1][1]).__name__ == "Pawn" and board[pos_y][pos_x + 1][1].en_passant):
                moves.append((pos_y + increment, pos_x + 1))

        return moves

    def do_en_passant(self, pos_x, pos_y, board):
        if self.team == 0:
            board[pos_y + 1][pos_x][1] = 0
        else:
            board[pos_y - 1][pos_x][1] = 0

class Rook(Piece):
    def __init__(self, team, image, side):
        super().__init__(5, team, image)
        self.side = side

    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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

    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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

    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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

    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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
        self.short_castle = True
        self.long_castle = True
    
    def get_moves(self, pos_x, pos_y, board, board_obj=None):
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

        short_rook_alive = False
        long_rook_alive = False
        for line in board:
            for _, row in line:
                if type(row).__name__ == "Rook" and row.side == 0 and row.team == self.team:
                    long_rook_alive = True
                if type(row).__name__ == "Rook" and row.side == 1 and row.team == self.team:
                    short_rook_alive = True

        if not short_rook_alive:
            self.short_castle = False
        if not long_rook_alive:
            self.long_castle = False

        oponent_moves = board_obj.get_all_moves((self.team + 1) % 2)
        if (pos_y, pos_x) not in oponent_moves:
            if self.short_castle is True and board[pos_y][pos_x + 1][1] == 0 and board[pos_y][pos_x + 2][1] == 0 and not \
                    ((pos_y, pos_x + 2) in oponent_moves or (pos_y, pos_x + 1) in oponent_moves):
                moves.append((pos_y, pos_x + 2))
            if self.long_castle is True and board[pos_y][pos_x - 1][1] == 0 and board[pos_y][pos_x - 2][1] == 0 and \
                    board[pos_y][pos_x - 3][1] == 0 and not ((pos_y, pos_x - 1) in oponent_moves or (pos_y, pos_x - 2) in oponent_moves or \
                        (pos_y, pos_x - 3) in oponent_moves):
                moves.append((pos_y, pos_x - 2))

        return moves

    def castle(self, kind, board):
        y = 0

        for line in board:

            x = 0
            for _, row in line:
                if type(row).__name__ == "Rook" and row.side == kind and row.team == self.team:
                    rook = row
                    index_x, index_y = x, y

                x += 1
            y += 1
                    
        if kind == 0:
            board[index_y][index_x + 3][1] = rook
            board[index_y][index_x][1] = 0
        else:
            board[index_y][index_x - 2][1] = rook
            board[index_y][index_x][1] = 0
