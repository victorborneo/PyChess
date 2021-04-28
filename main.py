from classes import *

def main():
    pygame.init()

    screen_x, screen_y = 600, 600
    pygame.display.set_caption("Chess")
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                index_x, index_y = (x - 20) // 70, (y - 8) // 70

                if 0 <= index_x < 8 and 0 <= index_y < 8:
                    tile = board.board[index_y][index_x][1]

                    if selected is not None and (index_y, index_x) in moves:
                        board.board[aux_index_y][aux_index_x][1] = 0
                        board.board[index_y][index_x][1] = selected
                        board.turn = (board.turn + 1) % 2
                        moves = []
                        selected = None
                    elif tile != 0 and tile.team == board.turn:
                        selected = board.board[index_y][index_x][1]
                        moves = selected.get_moves(index_x, index_y, board.board)
                        aux_index_x, aux_index_y = index_x, index_y

        redraw()
    pygame.quit()


if __name__ == "__main__":
    main()
