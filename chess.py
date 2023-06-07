import pygame
import os

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load images of chess pieces
piece_images = {}
base_dir = "images/pieces"
for file in os.listdir(base_dir):
    if file.endswith(".png"):
        piece_name = file.split(".")[0]
        image = pygame.image.load(os.path.join(base_dir, file))
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        piece_images[piece_name] = image

# Create the chessboard
board = [
    ['B_Rook', 'B_Knight', 'B_Bishop', 'B_Queen', 'B_King', 'B_Bishop', 'B_Knight', 'B_Rook'],
    ['B_Pawn', 'B_Pawn', 'B_Pawn', 'B_Pawn', 'B_Pawn', 'B_Pawn', 'B_Pawn', 'B_Pawn'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['W_Pawn', 'W_Pawn', 'W_Pawn', 'W_Pawn', 'W_Pawn', 'W_Pawn', 'W_Pawn', 'W_Pawn'],
    ['W_Rook', 'W_Knight', 'W_Bishop', 'W_Queen', 'W_King', 'W_Bishop', 'W_Knight', 'W_Rook'],
]

# Get available moves for a given piece
def get_available_moves(row, col):
    piece = board[row][col]
    available_moves = []

    if 'Pawn' in piece:
        direction = 1 if piece.startswith('W') else -1
        # Move forward by one square
        if is_valid_square(row + direction, col) and board[row + direction][col] == ' ':
            available_moves.append((row + direction, col))
            # Move forward by two squares (for the initial double-step)
            if (row == 1 and direction == 1) or (row == 6 and direction == -1):
                if board[row + 2 * direction][col] == ' ':
                    available_moves.append((row + 2 * direction, col))
        # Capture diagonally
        if is_valid_square(row + direction, col - 1) and board[row + direction][col - 1][0] != piece[0]:
            available_moves.append((row + direction, col - 1))
        if is_valid_square(row + direction, col + 1) and board[row + direction][col + 1][0] != piece[0]:
            available_moves.append((row + direction, col + 1))

    elif 'Rook' in piece:
        # Move horizontally
        for c in range(col - 1, -1, -1):
            if board[row][c] == ' ':
                available_moves.append((row, c))
            elif board[row][c][0] != piece[0]:
                available_moves.append((row, c))
                break
            else:
                break

        for c in range(col + 1, COLS):
            if board[row][c] == ' ':
                available_moves.append((row, c))
            elif board[row][c][0] != piece[0]:
                available_moves.append((row, c))
                break
            else:
                break

        # Move vertically
        for r in range(row - 1, -1, -1):
            if board[r][col] == ' ':
                available_moves.append((r, col))
            elif board[r][col][0] != piece[0]:
                available_moves.append((r, col))
                break
            else:
                break

        for r in range(row + 1, ROWS):
            if board[r][col] == ' ':
                available_moves.append((r, col))
            elif board[r][col][0] != piece[0]:
                available_moves.append((r, col))
                break
            else:
                break

    # Add logic for the remaining pieces (Knight, Bishop, Queen, King) here

    return available_moves

# Function to check if a square is within the valid range of the chessboard
def is_valid_square(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# Game loop
running = True
selected_piece = None
valid_moves = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                # Get the row and column of the selected square
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if selected_piece is None:
                    piece = board[row][col]
                    if piece != ' ':
                        selected_piece = (row, col)
                        valid_moves = get_available_moves(row, col)
                else:
                    move = (row, col)
                    if move in valid_moves:
                        # Make the move
                        board[move[0]][move[1]] = board[selected_piece[0]][selected_piece[1]]
                        board[selected_piece[0]][selected_piece[1]] = ' '
                        selected_piece = None
                        valid_moves = []

    # Draw the chessboard
    window.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(window, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[row][col]
            if piece != ' ':
                image = piece_images[piece]
                window.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Highlight the selected piece and valid moves
    if selected_piece is not None:
        pygame.draw.rect(window, (0, 255, 0), (selected_piece[1] * SQUARE_SIZE, selected_piece[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for move in valid_moves:
            pygame.draw.circle(window, (0, 255, 0), (move[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

    pygame.display.update()

pygame.quit()
