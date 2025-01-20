import os
import pygame
import sys
from Pause_Menu import PauseMenu
# Add the Pictures folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Pictures'))

os.environ['SDL_VIDEO_CENTERED'] = '1'

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 700  # Window size
        self.BOARD_SIZE = 400  # Smaller game board size
        self.TOP_SPACE = 50  # Space at the top
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font = pygame.font.Font(None, 36)
        self.LINE_WIDTH = 15
        self.BOARD_ROWS, self.BOARD_COLS = 3, 3
        self.SQUARE_SIZE = self.BOARD_SIZE // self.BOARD_COLS
        self.CIRCLE_RADIUS = self.SQUARE_SIZE // 3
        self.CIRCLE_WIDTH = 15
        self.CROSS_WIDTH = 25
        self.SPACE = self.SQUARE_SIZE // 4

        self.BG_COLOR = (34, 139, 34)  # Forest Green background color
        self.LINE_COLOR = (0, 100, 0)  # Dark Green line color
        self.CIRCLE_COLOR = (0, 255, 127)  # Spring Green circle color
        self.CROSS_COLOR = (70, 205, 25)  # Green cross color
        self.BUTTON_COLOR = (60, 179, 113)  # Medium Sea Green button color
        self.TEXT_COLOR = (255, 255, 255)  # White text color
        self.BORDER_COLOR = (0, 100, 0)  # Dark Green border color


        self.board = [[0 for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]
        self.paused = False
        self.show_message = None
        self.player = 1
        self.running = True
        self.winner = None

        # Initialize the PauseMenu
        self.pause_menu = PauseMenu(self.screen, self.font)

        # Load the background image
        self.background_image = pygame.image.load('bg1.png')
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.WIDTH, self.HEIGHT))

    def draw_lines(self):
        for row in range(1, self.BOARD_ROWS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (self.board_x, row * self.SQUARE_SIZE + self.board_y), (self.board_x + self.BOARD_SIZE, row * self.SQUARE_SIZE + self.board_y), self.LINE_WIDTH)
        for col in range(1, self.BOARD_COLS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (col * self.SQUARE_SIZE + self.board_x, self.board_y), (col * self.SQUARE_SIZE + self.board_x, self.board_y + self.BOARD_SIZE), self.LINE_WIDTH)

    def draw_border(self):
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (self.board_x, self.board_y, self.BOARD_SIZE, self.BOARD_SIZE), self.LINE_WIDTH)

    def draw_figures(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.board_x, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.board_y), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                elif self.board[row][col] == 2:
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (col * self.SQUARE_SIZE + self.SPACE + self.board_x, row * self.SQUARE_SIZE + self.SPACE + self.board_y), (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE + self.board_x, row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE + self.board_y), self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (col * self.SQUARE_SIZE + self.SPACE + self.board_x, row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE + self.board_y), (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE + self.board_x, row * self.SQUARE_SIZE + self.SPACE + self.board_y), self.CROSS_WIDTH)

    def draw_button(self):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (10, 10, 50, 50))
        if self.paused:
            pygame.draw.polygon(self.screen, self.TEXT_COLOR, [(20, 20), (20, 50), (50, 35)])  # Play symbol
        else:
            pygame.draw.line(self.screen, self.TEXT_COLOR, (20, 20), (20, 50), 10)  # Pause symbol part 1
            pygame.draw.line(self.screen, self.TEXT_COLOR, (40, 20), (40, 50), 10)  # Pause symbol part 2

    def display_message(self, message):
        message_rect = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 2 - 50, self.WIDTH // 2, 100)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, message_rect)
        pygame.draw.rect(self.screen, self.LINE_COLOR, message_rect, 3)  # Draw border
        text = self.font.render(message, True, self.TEXT_COLOR)
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))

    def mark_square(self, row, col, player):
        self.board[row][col] = player

    def available_square(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def check_win(self, player):
        # Check rows
        for row in range(self.BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player:
                self.draw_horizontal_win_line(row, player)
                return True

        # Check columns
        for col in range(self.BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                self.draw_vertical_win_line(col, player)
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.draw_desc_diagonal(player)
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.draw_asc_diagonal(player)
            return True

        return False

    def draw_horizontal_win_line(self, row, player):
        posY = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.board_y
        color = self.CIRCLE_COLOR if player == 1 else self.CROSS_COLOR
        pygame.draw.line(self.screen, color, (self.board_x, posY), (self.board_x + self.BOARD_SIZE, posY), self.LINE_WIDTH)

    def draw_vertical_win_line(self, col, player):
        posX = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.board_x
        color = self.CIRCLE_COLOR if player == 1 else self.CROSS_COLOR
        pygame.draw.line(self.screen, color, (posX, self.board_y), (posX, self.board_y + self.BOARD_SIZE), self.LINE_WIDTH)

    def draw_asc_diagonal(self, player):
        color = self.CIRCLE_COLOR if player == 1 else self.CROSS_COLOR
        pygame.draw.line(self.screen, color, (self.board_x, self.board_y + self.BOARD_SIZE), (self.board_x + self.BOARD_SIZE, self.board_y), self.LINE_WIDTH)

    def draw_desc_diagonal(self, player):
        color = self.CIRCLE_COLOR if player == 1 else self.CROSS_COLOR
        pygame.draw.line(self.screen, color, (self.board_x, self.board_y), (self.board_x + self.BOARD_SIZE, self.board_y + self.BOARD_SIZE), self.LINE_WIDTH)

    def restart(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_lines()
        self.draw_border()
        self.draw_button()
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                self.board[row][col] = 0
        self.show_message = None
        self.player = 1
        self.winner = None
        self.paused = False

    def draw_play_again_button(self):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (self.WIDTH // 2 - 100, self.HEIGHT - 150, 200, 50))
        text = self.font.render("Play Again", True, self.TEXT_COLOR)
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT - 140))

    def draw_main_menu_button(self):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, (self.WIDTH // 2 - 100, self.HEIGHT - 80, 200, 50))
        text = self.font.render("Main Menu", True, self.TEXT_COLOR)
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT - 70))

    def handle_play_again(self, mouseX, mouseY):
        return self.WIDTH // 2 - 100 <= mouseX <= self.WIDTH // 2 + 100 and self.HEIGHT - 150 <= mouseY <= self.HEIGHT - 100

    def handle_main_menu(self, mouseX, mouseY):
        return self.WIDTH // 2 - 100 <= mouseX <= self.WIDTH // 2 + 100 and self.HEIGHT - 80 <= mouseY <= self.HEIGHT - 30

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_menu.toggle()
        self.show_message = "Game Paused" if self.paused else None

    def run(self):
        self.board_x = (self.WIDTH - self.BOARD_SIZE) // 2
        self.board_y = self.HEIGHT - self.BOARD_SIZE - 50  # Centered at the bottom part

        while self.running:
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos

                    if 10 <= mouseX <= 60 and 10 <= mouseY <= 60:
                        self.toggle_pause()
                        self.draw_button()
                        self.screen.fill(self.BG_COLOR, (0, self.HEIGHT // 2 - 50, self.WIDTH, 100))  # Clear message area
                        self.draw_lines()  # Redraw lines to ensure they are not broken
                        self.draw_border()  # Redraw border to ensure it is not broken
                        self.draw_figures()  # Redraw figures to ensure they are not broken
                        continue  # Skip the rest of the loop to avoid placing X or O

                    if self.paused:
                        self.pause_menu.handle_click((mouseX, mouseY))
                        if self.pause_menu.action == "resume":
                            self.toggle_pause()  # Resume the game
                        elif self.pause_menu.action == "main_menu":
                            return  # Go to main menu
                    else:
                        if self.winner is not None:
                            if self.handle_play_again(mouseX, mouseY):
                                self.restart()
                                continue  # Avoid marking squares immediately after clicking play again
                            elif self.handle_main_menu(mouseX, mouseY):
                                return "main_menu"

                        if not self.winner:
                            clicked_row = (mouseY - self.board_y) // self.SQUARE_SIZE
                            clicked_col = (mouseX - self.board_x) // self.SQUARE_SIZE

                            if 0 <= clicked_row < self.BOARD_ROWS and 0 <= clicked_col < self.BOARD_COLS:
                                if self.available_square(clicked_row, clicked_col):
                                    self.mark_square(clicked_row, clicked_col, self.player)
                                    if self.check_win(self.player):
                                        self.winner = self.player
                                    elif self.is_board_full():
                                        self.winner = 0
                                    self.player = 3 - self.player

                                    self.draw_figures()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()

            self.draw_lines()  # Ensure lines are drawn
            self.draw_border()  # Ensure border is drawn
            self.draw_figures()  # Ensure figures are drawn
            self.draw_button()  # Ensure the pause button is drawn on top

            if self.show_message:
                self.display_message(self.show_message)
            elif self.winner == 1:
                self.display_message("Player O Wins!")
                self.draw_play_again_button()
                self.draw_main_menu_button()
            elif self.winner == 2:
                self.display_message("Player X Wins!")
                self.draw_play_again_button()
                self.draw_main_menu_button()
            elif self.winner == 0:
                self.display_message("It's a Draw!")
                self.draw_play_again_button()
                self.draw_main_menu_button()

            if self.paused:
                self.pause_menu.draw()  # Draw the pause menu on top

            pygame.display.update()

        pygame.quit()
        sys.exit()