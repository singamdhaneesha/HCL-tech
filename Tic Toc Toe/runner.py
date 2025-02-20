import pygame
import sys
import time
import random

# Initialize game constants
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    return O if count_x > count_o else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i, row in enumerate(board) 
                   for j, val in enumerate(row) if val == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    
    next_board = [row[:] for row in board]
    next_board[i][j] = player(board)
    return next_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] and all(cell == row[0] for cell in row):
            return row[0]
    
    # Check columns
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        if column[0] and all(cell == column[0] for cell in column):
            return column[0]
    
    # Check diagonals
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]
    
    if diag1[0] and all(cell == diag1[0] for cell in diag1):
        return diag1[0]
    if diag2[0] and all(cell == diag2[0] for cell in diag2):
        return diag2[0]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell != EMPTY for cell in row) for row in board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # 50% chance of making a random move
    if random.random() < 0.5:
        possible_moves = list(actions(board))
        if possible_moves:
            return random.choice(possible_moves)
    
    current_player = player(board)
    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)
    
    return move

def max_value(board, alpha=float('-inf'), beta=float('inf')):
    if terminal(board):
        return utility(board), None
    
    v = float('-inf')
    best_move = None
    
    possible_actions = list(actions(board))
    random.shuffle(possible_actions)
    
    for action in possible_actions:
        min_val, _ = min_value(result(board, action), alpha, beta)
        
        # 30% chance of misvaluation
        if random.random() < 0.3:
            min_val *= random.uniform(0.5, 1.5)
        
        if min_val > v:
            v = min_val
            best_move = action
        
        alpha = max(alpha, v)
        if beta <= alpha and random.random() > 0.3:
            break
    
    return v, best_move

def min_value(board, alpha=float('-inf'), beta=float('inf')):
    if terminal(board):
        return utility(board), None
    
    v = float('inf')
    best_move = None
    
    possible_actions = list(actions(board))
    random.shuffle(possible_actions)
    
    for action in possible_actions:
        max_val, _ = max_value(result(board, action), alpha, beta)
        
        # 30% chance of misvaluation
        if random.random() < 0.3:
            max_val *= random.uniform(0.5, 1.5)
        
        if max_val < v:
            v = max_val
            best_move = action
        
        beta = min(beta, v)
        if beta <= alpha and random.random() > 0.3:
            break
    
    return v, best_move

def run_game():
    pygame.init()
    size = width, height = 600, 400

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tic-Tac-Toe: Balanced Edition")

    try:
        mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
        largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
        moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
    except:
        mediumFont = pygame.font.SysFont(None, 28)
        largeFont = pygame.font.SysFont(None, 40)
        moveFont = pygame.font.SysFont(None, 60)

    user = None
    board = initial_state()
    ai_turn = False

    # Game statistics
    stats = {
        'player_wins': 0,
        'ai_wins': 0,
        'ties': 0
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        if user is None:
            # Draw title
            title = largeFont.render("Balanced Tic-Tac-Toe", True, white)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 50)
            screen.blit(title, titleRect)

            # Draw buttons
            playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
            playX = mediumFont.render("Play as X", True, black)
            playXRect = playX.get_rect()
            playXRect.center = playXButton.center
            pygame.draw.rect(screen, white, playXButton)
            screen.blit(playX, playXRect)

            playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
            playO = mediumFont.render("Play as O", True, black)
            playORect = playO.get_rect()
            playORect.center = playOButton.center
            pygame.draw.rect(screen, white, playOButton)
            screen.blit(playO, playORect)

            # Display stats
            statsText = mediumFont.render(
                f"Wins: {stats['player_wins']} Ties: {stats['ties']} Losses: {stats['ai_wins']}", 
                True, white
            )
            statsRect = statsText.get_rect()
            statsRect.center = (width / 2, height - 50)
            screen.blit(statsText, statsRect)

            # Check if button is clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if playXButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = X
                elif playOButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = O

        else:
            # Draw game board
            tile_size = 80
            tile_origin = (width / 2 - (1.5 * tile_size),
                           height / 2 - (1.5 * tile_size))
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, white, rect, 3)

                    if board[i][j] != EMPTY:
                        move = moveFont.render(board[i][j], True, white)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        screen.blit(move, moveRect)
                    row.append(rect)
                tiles.append(row)

            game_over = terminal(board)
            current_player = player(board)

            if game_over:
                game_winner = winner(board)
                if game_winner is None:
                    title = f"Game Over: Tie"
                    stats['ties'] += 1
                else:
                    if game_winner == user:
                        stats['player_wins'] += 1
                        title = "You Win!"
                    else:
                        stats['ai_wins'] += 1
                        title = "AI Wins!"
            elif user == current_player:
                title = f"Your Turn ({user})"
            else:
                title = f"AI Thinking..."

            title = largeFont.render(title, True, white)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 30)
            screen.blit(title, titleRect)

            # Check for AI move
            if user != current_player and not game_over:
                if ai_turn:
                    time.sleep(0.5)
                    move = minimax(board)
                    board = result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            # Check for a user move
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1 and user == current_player and not game_over:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if (board[i][j] == EMPTY and tiles[i][j].collidepoint(mouse)):
                            board = result(board, (i, j))

            # Play Again button
            if game_over:
                againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                again = mediumFont.render("Play Again", True, black)
                againRect = again.get_rect()
                againRect.center = againButton.center
                pygame.draw.rect(screen, white, againButton)
                screen.blit(again, againRect)
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1:
                    mouse = pygame.mouse.get_pos()
                    if againButton.collidepoint(mouse):
                        time.sleep(0.2)
                        user = None
                        board = initial_state()
                        ai_turn = False

        pygame.display.flip()

if __name__ == '__main__':
    run_game()