import pygame
import sys

class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.is_open = False
        self.action = None  # To track the user's selected action

    def draw(self):
        """Draw the pause menu."""
        pygame.draw.rect(self.screen, (50, 50, 50), (self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 100, 300, 200))
        pygame.draw.rect(self.screen, (200, 200, 200), (self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 100, 300, 200), 3)

        resume_text = self.font.render("Resume", True, (255, 255, 255))
        main_menu_text = self.font.render("Main Menu", True, (255, 255, 255))

        self.screen.blit(resume_text, (self.screen.get_width() // 2 - resume_text.get_width() // 2, self.screen.get_height() // 2 - 60))
        self.screen.blit(main_menu_text, (self.screen.get_width() // 2 - main_menu_text.get_width() // 2, self.screen.get_height() // 2 + 20))

    def handle_click(self, pos):
        """Handle mouse clicks on the pause menu options."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Resume button
        if screen_width // 2 - 100 <= pos[0] <= screen_width // 2 + 100 and screen_height // 2 - 70 <= pos[1] <= screen_height // 2 - 30:
            self.action = "resume"  # Signal to resume the game
            self.is_open = False  # Close the pause menu

        # Main Menu button
        elif screen_width // 2 - 100 <= pos[0] <= screen_width // 2 + 100 and screen_height // 2 + 10 <= pos[1] <= screen_height // 2 + 50:
            self.action = "main_menu"  # Signal to go to the main menu
            self.is_open = False  # Close the pause menu
            self.return_to_main_menu()

    def return_to_main_menu(self):
        """Call the Main_Menu to return to the main menu."""
        import Main_Menu  # Lazy import to avoid circular dependency
        # Reinitialize the screen dimensions as defined in Main_Menu.py
        screen = pygame.display.set_mode((Main_Menu.SCREEN_WIDTH, Main_Menu.SCREEN_HEIGHT))
        Main_Menu.MainMenu().display()

    def toggle(self):
        """Toggle the pause menu."""
        self.is_open = not self.is_open