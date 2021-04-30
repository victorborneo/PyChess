from classes import *

def main():
    pygame.init()
    pygame.font.init()

    screen_x, screen_y = 600, 600
    pygame.display.set_caption("Chess")
    font = pygame.font.SysFont('Arial', 30)
    pygame.display.set_icon(pygame.image.load('.\\Pieces\\icon.png'))

    check_message = font.render("Check!!", True, (255, 0, 0))
    checkmate_message = font.render("Checkmate!!", True, (255, 0, 0))
    stalemate_message = font.render("Stalemate!!", True, (255, 0, 0))
    draw_message = font.render("Draw!!", True, (255, 0, 0))

    window = pygame.display.set_mode((screen_x, screen_y))

    def redraw():
        window.blit(board.image, (0, 0))

        y = 0
        for line in board.board:

            x = 0
            for pos, row in line:
                if row != 0:
                    window.blit(row.image, pos)

                if (y, x) in moves:
                    pygame.draw.circle(window, (255, 0, 0), (pos[0] + 30, pos[1] + 35), 5)
                x += 1
            y += 1

        if board.promotion:
            if board.turn != 0:
                window.blit(board.white_promotion, (20, 20))
            else:
                window.blit(board.black_promotion, (20, 20))

        if board.checkmate:
            window.blit(checkmate_message, (0, 0))
        elif board.stalemate:
            window.blit(stalemate_message, (0, 0))
        elif board.draw:
            window.blit(draw_message, (0, 0))
        elif board.check > 0:
            window.blit(check_message, (0, 0))

        pygame.display.update()

    run = True
    selected = None
    moves = []
    board = Board()
    while run:
        pygame.time.Clock().tick(30)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if board.promotion:
                    board.promotion = False

                    if board.turn != 0:
                        color = ".\\Pieces\\white"
                        team = 0
                    else:
                        color = ".\\Pieces\\black"
                        team = 1

                    if event.key == pygame.K_1:
                        board.board[index_y][index_x][1] = Queen(team, f"{color}_queen.png")
                    elif event.key == pygame.K_2:
                        board.board[index_y][index_x][1] = Rook(team, f"{color}_rook.png", -1)
                    elif event.key == pygame.K_3:
                        board.board[index_y][index_x][1] = Bishop(team, f"{color}_bishop.png")
                    elif event.key == pygame.K_4:
                        board.board[index_y][index_x][1] = Knight(team, f"{color}_knight.png")
                    else:
                        board.promotion = True

                    all_moves = board.get_all_moves(board.turn)
                    board.check_check(all_moves)
                    board.check_checkmate_or_stalemate()
                    board.check_draw()

                if board.checkmate or board.stalemate or board.draw:
                    if event.key == pygame.K_RETURN:
                        board = Board()

            elif event.type == pygame.MOUSEBUTTONDOWN and not (board.promotion or board.checkmate or board.stalemate or board.draw):
                x, y = pygame.mouse.get_pos()
                index_x, index_y = (x - 20) // 70, (y - 8) // 70

                if 0 <= index_x < 8 and 0 <= index_y < 8:
                    tile = board.board[index_y][index_x][1]

                    if selected is not None and (index_y, index_x) in moves:
                        board.last_move = (index_y, index_x)
                        board.reset_en_passant()
                        board.check = 0

                        if type(selected).__name__ == "King":
                            if index_x - aux_index_x == 2:
                                selected.castle(1, board.board)
                            if index_x - aux_index_x == -2:
                                selected.castle(0, board.board)

                            selected.short_castle = False
                            selected.long_castle = False
                        elif type(selected).__name__ == "Rook":
                            for line in board.board:
                                for _, row in line:
                                    if type(row).__name__ == "King" and row.team == selected.team:
                                        king = row

                            if selected.side == 0:
                                king.long_castle = False
                            elif selected.side == 1:
                                king.short_castle = False
                        elif type(selected).__name__ == "Pawn":
                            if abs(index_y - aux_index_y) == 2:
                                selected.en_passant = True
                            if board.board[index_y][index_x][1] == 0 and aux_index_x != index_x:
                                selected.do_en_passant(index_x, index_y, board.board)
                            if (selected.team == 0 and index_y == 0) or (selected.team == 1 and index_y == 7):
                                board.promotion = True

                        board.board[aux_index_y][aux_index_x][1] = 0
                        board.board[index_y][index_x][1] = selected
                        all_moves = board.get_all_moves(board.turn)

                        board.turn = (board.turn + 1) % 2
                        board.check_check(all_moves)
                        board.check_checkmate_or_stalemate()
                        board.check_draw()

                        moves = []
                        selected = None
                    elif tile != 0 and tile.team == board.turn:
                        moves = []
                        selected = board.board[index_y][index_x][1]

                        if type(selected).__name__ == "King":
                            aux_moves = board.get_king_legal_moves(index_x, index_y)
                        else:
                            aux_moves = board.get_legal_moves(index_x, index_y, selected)

                        for move in aux_moves:
                            try:
                                if board.board[move[0]][move[1]][1].team != board.turn:
                                    moves.append(move)
                            except AttributeError:
                                moves.append(move)

                        aux_index_x, aux_index_y = index_x, index_y

        redraw()
    pygame.quit()


if __name__ == "__main__":
    main()
