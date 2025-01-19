import pygame
import sys
from Pause_Menu import PauseMenu

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
            screen.fill(BLACK)
            
            if is_paused:
                # Draw the pause menu when the game is paused
                pause_menu.draw()
            else:
                # Normal game content when not paused
                draw_text("DSA FINAL PROJECT", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
                draw_text("PLAY", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                draw_text("QUIT", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if not is_paused:
                        if SCREEN_WIDTH // 2 - 50 < mouse_x < SCREEN_WIDTH // 2 + 50:
                            if SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2 + 20:
                                PlayMenu().display()
                            elif SCREEN_HEIGHT // 2 + 30 < mouse_y < SCREEN_HEIGHT // 2 + 70:
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
            screen.fill(BLACK)

            draw_text(f"CASE STUDY {self.current_case + 1}", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)
            draw_text(self.case_studies[self.current_case], WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
            draw_text(self.case_details[self.case_studies[self.current_case]], WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, center=True, wrap_width=600)

            draw_text("<", WHITE, 50, SCREEN_HEIGHT // 2)
            draw_text(">", WHITE, SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)
            draw_text("PLAY", GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            draw_text("BACK", RED, 50, 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Previous button
                    if 20 < mouse_x < 80 and SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2 + 20:
                        self.current_case = (self.current_case - 1) % len(self.case_studies)

                    # Next button
                    elif SCREEN_WIDTH - 80 < mouse_x < SCREEN_WIDTH - 20 and SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2 + 20:
                        self.current_case = (self.current_case + 1) % len(self.case_studies)

                    # Play button
                    elif SCREEN_WIDTH // 2 - 50 < mouse_x < SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT - 170 < mouse_y < SCREEN_HEIGHT - 130:
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

                    # Back button
                    elif 20 < mouse_x < 100 and 20 < mouse_y < 80:
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