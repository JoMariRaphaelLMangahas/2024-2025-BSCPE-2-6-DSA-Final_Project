import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ROD_COLOR = (200, 150, 100)
DISK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
BUTTON_GREEN = (0, 255, 0)
BUTTON_RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class TowerOfHanoi:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.rod_width = 10
        self.disk_height = 20
        self.rod_x = [200, 400, 600]
        self.rod_y = 400
        shuffled_disks = list(range(1, num_disks + 1))
        random.shuffle(shuffled_disks)
        self.towers = [shuffled_disks, [], []]
        self.selected_disk = None
        self.selected_rod = None
        self.move_count = 0
        self.paused = False
        self.show_guideline = False
        self.show_quit_popup = False
        self.show_restart_popup = False
        self.show_new_game_popup = False
        self.saved_shuffled_disks = shuffled_disks.copy()

    def is_game_completed(self):
        return (
            len(self.towers[2]) == self.num_disks
            and sorted(self.towers[2], reverse=True) == [i for i in range(self.num_disks, 0, -1)]
        )

    def draw_game(self):
        screen.fill(WHITE)

        if self.show_guideline:
            self.draw_guideline()
        elif self.paused:
            self.draw_menu()
        elif self.show_quit_popup:
            self.draw_quit_popup()
        elif self.show_restart_popup:
            self.draw_restart_popup()
        elif self.show_new_game_popup:
            self.draw_new_game_popup()
        else:
            self.draw_towers()

        pygame.display.flip()

    def draw_towers(self):
        if self.is_game_completed():
            self.draw_congratulations()

        for x in self.rod_x:
            pygame.draw.rect(screen, ROD_COLOR, (x - self.rod_width // 2, self.rod_y - 200, self.rod_width, 200))

        for i, tower in enumerate(self.towers):
            for j, disk in enumerate(tower):
                if i == self.selected_rod and disk == self.selected_disk:
                    continue
                disk_width = 30 + disk * 20
                x = self.rod_x[i]
                y = self.rod_y - (j + 1) * self.disk_height
                self.draw_rounded_disk(x, y, disk_width, self.disk_height, DISK_COLORS[disk - 1], str(disk))

        if self.selected_disk is not None:
            disk_width = 30 + self.selected_disk * 20
            x = self.rod_x[self.selected_rod]
            y = self.rod_y - 250
            self.draw_rounded_disk(x, y, disk_width, self.disk_height, DISK_COLORS[self.selected_disk - 1], str(self.selected_disk))

        moves_text = font.render(f"Moves: {self.move_count}", True, BLACK)
        screen.blit(moves_text, (WIDTH // 2 - 50, HEIGHT - 50))

        self.draw_icons()

    def draw_congratulations(self):
        congrats_text = font.render("Congratulations! You've completed the game!", True, BLACK)
        text_rect = congrats_text.get_rect(center=(WIDTH // 2, 50))
        pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 20))
        screen.blit(congrats_text, text_rect)

    def draw_icons(self):
        menu_rect = pygame.Rect(10, 10, 40, 30)
        pygame.draw.rect(screen, WHITE, menu_rect, border_radius=5)
        menu_text = font.render("lll", True, BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        screen.blit(menu_text, menu_text_rect)

        # Question mark icon
        question_rect = pygame.Rect(WIDTH - 50, 10, 40, 30)
        if self.show_guideline:
            pygame.draw.rect(screen, WHITE, question_rect, border_radius=5)
            question_mark = font.render("?", True, BLACK)
        else:
            pygame.draw.rect(screen, WHITE, question_rect, border_radius=5)
            question_mark = font.render("?", True, BLACK)
        question_text_rect = question_mark.get_rect(center=question_rect.center)
        screen.blit(question_mark, question_text_rect)

    def draw_menu(self):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 340))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 140, HEIGHT // 2 - 140, 280, 60))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 140, HEIGHT // 2 - 60, 280, 60))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 140, HEIGHT // 2 + 20, 280, 60))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 140, HEIGHT // 2 + 100, 280, 60))

        resume_text = font.render("RESUME", True, BLACK)
        restart_text = font.render("RESTART", True, BLACK)
        new_game_text = font.render("NEW GAME", True, BLACK)
        quit_text = font.render("QUIT", True, BLACK)

        screen.blit(resume_text, (WIDTH // 2 - 50, HEIGHT // 2 - 120))
        screen.blit(restart_text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))
        screen.blit(new_game_text, (WIDTH // 2 - 65, HEIGHT // 2 + 40))
        screen.blit(quit_text, (WIDTH // 2 - 35, HEIGHT // 2 + 120))

    def draw_guideline(self):
        pygame.draw.rect(screen, GRAY, (50, 50, WIDTH - 100, HEIGHT - 100))
        guideline_text = font.render("Guidelines:", True, BLACK)
        rules = [
            "1. Only one disk can be moved at a time.",
            "2. A larger disk cannot be placed on a smaller disk.",
            "3. All disks start on the leftmost rod.",
            "4. Goal: Move all disks to the rightmost rod."
        ]
        screen.blit(guideline_text, (70, 70))

        for i, rule in enumerate(rules):
            rule_text = font.render(rule, True, BLACK)
            screen.blit(rule_text, (70, 110 + i * 40))

    def draw_restart_popup(self):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200))
        question_text = font.render("You will lose progress. Restart?", True, BLACK)
        screen.blit(question_text, (WIDTH // 2 - 130, HEIGHT // 2 - 70))

        yes_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 10, 130, 50)
        no_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 10, 130, 50)

        pygame.draw.rect(screen, BUTTON_GREEN, yes_rect)
        pygame.draw.rect(screen, BUTTON_RED, no_rect)

        yes_text = font.render("YES", True, WHITE)
        no_text = font.render("NO", True, WHITE)

        screen.blit(yes_text, yes_rect.move(45, 10))
        screen.blit(no_text, no_rect.move(50, 10))

    def draw_new_game_popup(self):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200))
        question_text = font.render("Start a new game?", True, BLACK)
        screen.blit(question_text, (WIDTH // 2 - 130, HEIGHT // 2 - 70))

        yes_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 10, 130, 50)
        no_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 10, 130, 50)

        pygame.draw.rect(screen, BUTTON_GREEN, yes_rect)
        pygame.draw.rect(screen, BUTTON_RED, no_rect)

        yes_text = font.render("Yes", True, WHITE)
        no_text = font.render("No", True, WHITE)

        screen.blit(yes_text, yes_rect.move(45, 10))
        screen.blit(no_text, no_rect.move(50, 10))
    
    def draw_quit_popup(self):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200))
        question_text = font.render("Want to quit the game?", True, BLACK)
        screen.blit(question_text, (WIDTH // 2 - 130, HEIGHT // 2 - 70))

        yes_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 + 10, 130, 50)
        no_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 10, 130, 50)

        pygame.draw.rect(screen, BUTTON_GREEN, yes_rect)
        pygame.draw.rect(screen, BUTTON_RED, no_rect)

        yes_text = font.render("Yes", True, WHITE)
        no_text = font.render("No", True, WHITE)

        screen.blit(yes_text, yes_rect.move(45, 10))
        screen.blit(no_text, no_rect.move(50, 10))

    def draw_rounded_disk(self, x, y, width, height, color, text, inverted=False):
        pygame.draw.rect(screen, color, (x - width // 2, y, width, height), border_radius=10)
        text_color = BLACK if not inverted else WHITE
        disk_text = small_font.render(text, True, text_color)
        text_rect = disk_text.get_rect(center=(x, y + height // 2))
        screen.blit(disk_text, text_rect)

    def handle_click(self, x, y):
        for i, rod_x in enumerate(self.rod_x):
            if rod_x - 50 < x < rod_x + 50:
                if self.selected_disk is None:
                    if self.towers[i]:
                        self.selected_disk = self.towers[i].pop()
                        self.selected_rod = i
                else:
                    if i == self.selected_rod:
                        self.towers[self.selected_rod].append(self.selected_disk)
                    else:
                        if not self.towers[i] or self.selected_disk < self.towers[i][-1]:
                            self.towers[i].append(self.selected_disk)
                            self.move_count += 1
                        else:
                            self.towers[self.selected_rod].append(self.selected_disk)
                    self.selected_disk = None
                    self.selected_rod = None
                return
            
        if self.paused:
            if WIDTH // 2 - 140 < x < WIDTH // 2 + 140:
                if HEIGHT // 2 - 140 < y < HEIGHT // 2 - 80:
                    self.paused = False
                elif HEIGHT // 2 - 60 < y < HEIGHT // 2:
                    self.show_restart_popup = True
                    self.paused = False
                elif HEIGHT // 2 + 20 < y < HEIGHT // 2 + 80:
                    self.show_new_game_popup = True
                    self.paused = False
                elif HEIGHT // 2 + 100 < y < HEIGHT // 2 + 160:
                    self.show_quit_popup = True
                    self.paused = False
            return

        if self.show_restart_popup:
            if WIDTH // 2 - 140 < x < WIDTH // 2 - 10 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                self.reset_game(self.saved_shuffled_disks)
                self.show_restart_popup = False
            elif WIDTH // 2 + 10 < x < WIDTH // 2 + 140 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                self.show_restart_popup = False
            return

        if self.show_new_game_popup:
            if WIDTH // 2 - 140 < x < WIDTH // 2 - 10 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                self.reset_game()
                self.show_new_game_popup = False
            elif WIDTH // 2 + 10 < x < WIDTH // 2 + 140 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                self.show_new_game_popup = False
            return
        
        if self.show_quit_popup:
            if WIDTH // 2 - 140 < x < WIDTH // 2 - 10 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                pygame.quit()
                sys.exit()
            elif WIDTH // 2 + 10 < x < WIDTH // 2 + 140 and HEIGHT // 2 + 10 < y < HEIGHT // 2 + 60:
                self.show_quit_popup = False
            return

    def handle_menu_click(self, x, y):
        if 10 < x < 50 and 10 < y < 40:
            self.paused = not self.paused

        if WIDTH - 50 < x < WIDTH - 10 and 10 < y < 40:
            self.show_guideline = not self.show_guideline

    def reset_game(self, shuffled_disks=None):
        if shuffled_disks is None:
            shuffled_disks = list(range(1, self.num_disks + 1))
            random.shuffle(shuffled_disks)
        self.towers = [shuffled_disks, [], []]
        self.selected_disk = None
        self.selected_rod = None
        self.move_count = 0
        self.saved_shuffled_disks = shuffled_disks.copy()


def main():
    game = TowerOfHanoi(num_disks=5)
    running = True

    while running:
        game.draw_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game.paused or game.show_quit_popup or game.show_restart_popup or game.show_new_game_popup:
                    game.handle_click(x, y)
                else:
                    game.handle_menu_click(x, y)
                    game.handle_click(x, y)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()