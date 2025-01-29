import pygame
import sys
from Pause_Menu import PauseMenu
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'Pictures'))

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DSA Final Project")

# Fonts
font = pygame.font.Font(None, 36)

# Pause Menu Instance
pause_menu = None  # Will be initialized later

# Load the high-definition background image
background_image = pygame.image.load('Pictures/Main Menu/bgm_m.png')
background_image = pygame.transform.smoothscale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load button background images
play_button_image = pygame.image.load('Pictures/Main Menu/play.png')
play_button_image = pygame.transform.smoothscale(play_button_image, (200, 75))  # Increased size

quit_button_image = pygame.image.load('Pictures/Main Menu/exit.png')
quit_button_image = pygame.transform.smoothscale(quit_button_image, (200, 75))  # Increased size

# Load case study background images
case_study_backgrounds = {
    "TIC-TAC-TOE": pygame.image.load('Pictures/Main Menu/TICTACTOE.png'),
    "STACKS APPLICATION": pygame.image.load('Pictures/Main Menu/Stacks.png'),
    "QUEUE APPLICATION": pygame.image.load('Pictures/Main Menu/QUEUE.png'),
    "BINARY TREE TRAVERSAL": pygame.image.load('Pictures/Main Menu/BTT.png'),
    "BINARY SEARCH TREE": pygame.image.load('Pictures/Main Menu/BST.png'),
    "TOWERS OF HANOI USING RECURSION": pygame.image.load('Pictures/Main Menu/towerofhanoi.png'),
    "SORTING": pygame.image.load('Pictures/Main Menu/SORTING.png')
}

# Scale case study background images
for key in case_study_backgrounds:
    case_study_backgrounds[key] = pygame.transform.smoothscale(case_study_backgrounds[key], (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load arrow and play button images for case studies
left_arrow_image = pygame.image.load('Pictures/Main Menu/leftarrow.png')
left_arrow_image = pygame.transform.smoothscale(left_arrow_image, (50, 50))

right_arrow_image = pygame.image.load('Pictures/Main Menu/rightarrow.png')
right_arrow_image = pygame.transform.smoothscale(right_arrow_image, (50, 50))

play_case_button_image = pygame.image.load('Pictures/Main Menu/play.png')
play_case_button_image = pygame.transform.smoothscale(play_case_button_image, (200, 100))  # Increased size

back_case_button_image = pygame.image.load('Pictures/Main Menu/exit.png')
back_case_button_image = pygame.transform.smoothscale(back_case_button_image, (100, 50))

def draw_text(text, color, x, y, center=True, wrap_width=None):
    if wrap_width:
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            if font.size(current_line + word)[0] <= wrap_width:
                current_line += word + ' '
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)

        for i, line in enumerate(lines):
            text_surface = font.render(line.strip(), True, color)
            text_rect = text_surface.get_rect()
            if center:
                text_rect.center = (x, y + i * 30)
            else:
                text_rect.topleft = (x, y + i * 30)
            screen.blit(text_surface, text_rect)
    else:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

class MainMenu:
    def display(self):
        global pause_menu  # Reference to the pause menu
        
        # Initialize the PauseMenu object here
        pause_menu = PauseMenu(screen, font)

        is_paused = False  # Flag to track if the game is paused

        while True:
            screen.blit(background_image, (0, 0))  # Draw the background image
            
            if is_paused:
                # Draw the pause menu when the game is paused
                pause_menu.draw()
            else:
                # Draw button backgrounds
                play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 37.5, 200, 75)
                quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 37.5, 200, 75)
                
                screen.blit(play_button_image, play_button_rect.topleft)
                screen.blit(quit_button_image, quit_button_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if not is_paused:
                        if play_button_rect.collidepoint(mouse_x, mouse_y):
                            PlayMenu().display()
                        elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                            ConfirmQuit().display()
                    else:
                        # Handle pause menu button clicks
                        pause_menu.handle_click((mouse_x, mouse_y))
                        if pause_menu.action == "resume":
                            is_paused = False  # Resume the game
                        elif pause_menu.action == "main_menu":
                            return  # Go to main menu

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        is_paused = not is_paused  # Toggle the pause state

class PlayMenu:
    def __init__(self):
        self.case_studies = [
            "TIC-TAC-TOE",
            "STACKS APPLICATION",
            "QUEUE APPLICATION",
            "BINARY TREE TRAVERSAL",
            "BINARY SEARCH TREE",
            "TOWERS OF HANOI USING RECURSION",
            "SORTING"
        ]

        self.case_details = {
            "TIC-TAC-TOE": "Tic-tac-toe is a classic game played on a 3x3 grid. Players take turns marking the spaces with X or O. The first to align three wins.",
            "STACKS APPLICATION": "Simulate a parking garage using a stack (LIFO). Supports car arrival and departure based on plate numbers.",
            "QUEUE APPLICATION": "Simulate a parking garage using a queue (FIFO). Supports car arrival and departure based on plate numbers.",
            "BINARY TREE TRAVERSAL": "Create a binary tree up to 5 levels and display traversals (LRT, TLR, LTR).",
            "BINARY SEARCH TREE": "Insert up to 30 integers in a BST and display traversals (LRT, TLR, LTR).",
            "TOWERS OF HANOI USING RECURSION": "Solve the Towers of Hanoi problem with 5 disks and display each step.",
            "SORTING": "Accept 30 integers and display sorting using bubble, insertion, selection, and other algorithms."
        }

        self.current_case = 0

    def display(self):
        global screen, font
        while True:
            screen.blit(case_study_backgrounds[self.case_studies[self.current_case]], (0, 0))  # Draw the case study background

            # Draw navigation and play buttons
            left_arrow_rect = pygame.Rect(20, SCREEN_HEIGHT // 2 - 25, 50, 50)
            right_arrow_rect = pygame.Rect(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2 - 25, 50, 50)
            play_case_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)  # Centered play button
            back_button_rect = pygame.Rect(20, 20, 100, 50)

            screen.blit(left_arrow_image, left_arrow_rect.topleft)
            screen.blit(right_arrow_image, right_arrow_rect.topleft)
            screen.blit(play_case_button_image, play_case_button_rect.topleft)
            screen.blit(back_case_button_image, back_button_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Previous button
                    if left_arrow_rect.collidepoint(mouse_x, mouse_y):
                        self.current_case = (self.current_case - 1) % len(self.case_studies)

                    # Next button
                    elif right_arrow_rect.collidepoint(mouse_x, mouse_y):
                        self.current_case = (self.current_case + 1) % len(self.case_studies)

                    # Play button
                    if play_case_button_rect.collidepoint(mouse_x, mouse_y):
                        selected_case = self.case_studies[self.current_case]
                        print(f"You selected to play CASE STUDY {self.current_case + 1}: {self.case_studies[self.current_case]}")

                        if selected_case == "TIC-TAC-TOE":
                            from Tic_Tac_Toe import TicTacToe
                            app = TicTacToe()
                            result = app.run()
                            if result == "main_menu":
                                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                                pygame.display.set_caption("DSA Final Project")
                                return

                        elif selected_case == "STACKS APPLICATION":
                            from Stack_Application import ParkingLot
                            app = ParkingLot()
                            app.run()

                        elif selected_case == "BINARY TREE TRAVERSAL":
                            from Binary_Tree_Traversal import Application
                            app = Application()
                            app.run()
                        
                        elif selected_case == "BINARY SEARCH TREE":
                            from Binary_Search_Tree import BinarySearchTreeApp
                            app = BinarySearchTreeApp()
                            app.run()
                        
                        elif selected_case == "TOWERS OF HANOI USING RECURSION":
                            from Tower_of_Hanoi import HanoiGame
                            app = HanoiGame()
                            app.run()

                    # Back button
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        return

class ConfirmQuit:
    def display(self):
        while True:
            screen.fill(BLACK)
            draw_text("ARE YOU SURE TO QUIT THE GAME?", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
            draw_text("YES", GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text("NO", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if SCREEN_WIDTH // 2 - 50 < mouse_x < SCREEN_WIDTH // 2 + 50:
                        if SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2 + 20:
                            pygame.quit()
                            sys.exit()
                        elif SCREEN_HEIGHT // 2 + 30 < mouse_y < SCREEN_HEIGHT // 2 + 70:
                            return

if __name__ == "__main__":
    MainMenu().display()