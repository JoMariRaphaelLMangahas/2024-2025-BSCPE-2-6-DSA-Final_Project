import pygame
import sys
import random
from Pause_Menu import PauseMenu  # Import PauseMenu
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POLE_COLOR = (100, 100, 100)
BG_COLOR = (255, 255, 255)
POLE_POSITIONS = [200, 400, 600]
BASE_Y = 500
POLE_HEIGHT = 300
DISK_HEIGHT = 25
MIN_DISK_WIDTH = 60
MAX_DISK_WIDTH = 180
NUM_DISKS = 5  # Changed to 5

class Disk:
    def __init__(self, width, color):
        self.width = width
        self.color = color
        self.x = POLE_POSITIONS[0]
        self.y = 0
        self.current_pole = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.width//2, self.y, self.width, DISK_HEIGHT))

class Pole:
    def __init__(self, x_pos):
        self.x = x_pos
        self.disks = []

    def top_position(self):
        return BASE_Y - len(self.disks) * (DISK_HEIGHT + 3)

    def add_disk(self, disk):
        disk.current_pole = self
        self.disks.append(disk)
        disk.y = self.top_position()

    def remove_disk(self):
        if self.disks:
            disk = self.disks.pop()
            disk.current_pole = None
            return disk
        return None

    def get_top_disk(self):
        return self.disks[-1] if self.disks else None

class HanoiGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.poles = [Pole(pos) for pos in POLE_POSITIONS]
        self.disks = []
        self.moves = []
        self.current_move = None
        self.animation_speed = 15  # Increased animation speed
        self.show_text = True
        self.text_counter = 0
        self.solving = False
        self.game_over = False
        self.pause_menu = PauseMenu(self.screen, pygame.font.SysFont(None, 48))  # Initialize PauseMenu
        self.is_paused = False  # Pause state
        self.pause_button = pygame.Rect(10, 10, 40, 40)  # Pause button
        
        self.create_disks()
        self.reset_positions()

    def create_disks(self):
        # Generate widths in descending order
        step = (MAX_DISK_WIDTH - MIN_DISK_WIDTH) // (NUM_DISKS - 1)
        widths = [MIN_DISK_WIDTH + i * step for i in range(NUM_DISKS)]
        widths.sort(reverse=True)  # Sort in descending order
        
        colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                 for _ in range(NUM_DISKS)]
        
        self.disks = [Disk(width, color) for width, color in zip(widths, colors)]

    def reset_positions(self):
        for pole in self.poles:
            pole.disks.clear()
        for disk in self.disks:
            self.poles[0].add_disk(disk)

    def draw_poles(self):
        for pole in self.poles:
            pygame.draw.rect(self.screen, POLE_COLOR,
                            (pole.x - 10, BASE_Y - POLE_HEIGHT, 20, POLE_HEIGHT))

    def draw_text(self):
        if not self.solving and not self.game_over:
            if self.text_counter // 30 % 2 == 0:
                text = self.font.render("Press SPACE to start", True, (0, 0, 0))
                self.screen.blit(text, (300, 100))
        elif self.game_over:
            if self.text_counter // 30 % 2 == 0:
                text = self.font.render("Complete! Press R to reset", True, (0, 0, 0))
                self.screen.blit(text, (250, 100))

    def generate_moves(self, n, source, target, auxiliary):
        if n == 1:
            self.moves.append((source, target))
            return
        self.generate_moves(n-1, source, auxiliary, target)
        self.moves.append((source, target))
        self.generate_moves(n-1, auxiliary, target, source)

    def start_solve(self):
        if not self.solving:
            self.moves = []
            self.generate_moves(NUM_DISKS, 0, 2, 1)
            self.solving = True

    def animate_move(self):
        if self.current_move is None and self.moves:
            self.current_move = self.moves.pop(0)
            source, target = self.current_move
            self.moving_disk = self.poles[source].remove_disk()
            self.animation_phase = 0
            self.animation_progress = 0

        if self.moving_disk:
            source, target = self.current_move
            target_pole = self.poles[target]
            
            if self.animation_phase == 0:  # Lift
                target_y = BASE_Y - POLE_HEIGHT - 50
                self.moving_disk.y = max(self.moving_disk.y - self.animation_speed, target_y)
                if self.moving_disk.y <= target_y:
                    self.animation_phase = 1

            elif self.animation_phase == 1:  # Move horizontally
                target_x = self.poles[target].x
                direction = 1 if target_x > self.moving_disk.x else -1
                self.moving_disk.x += direction * self.animation_speed
                if abs(self.moving_disk.x - target_x) < self.animation_speed:
                    self.moving_disk.x = target_x
                    self.animation_phase = 2

            elif self.animation_phase == 2:  # Lower
                target_y = target_pole.top_position()
                self.moving_disk.y = min(self.moving_disk.y + self.animation_speed, target_y)
                if self.moving_disk.y >= target_y:
                    target_pole.add_disk(self.moving_disk)
                    self.current_move = None
                    self.moving_disk = None
                    if not self.moves:
                        self.solving = False
                        self.game_over = True

    def draw_pause_play_button(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_button)
        if self.is_paused:
            play_button_points = [
                (self.pause_button.x + 10, self.pause_button.y + 5),
                (self.pause_button.x + 10, self.pause_button.y + 35),
                (self.pause_button.x + 30, self.pause_button.y + 20)
            ]
            pygame.draw.polygon(self.screen, (0, 0, 0), play_button_points)
        else:
            bold_font = pygame.font.SysFont(None, 48, bold=True)  # Define bold font
            pause_text = bold_font.render("||", True, (0, 0, 0), (255, 255, 255))  # Bold text with background color
            self.screen.blit(pause_text, (self.pause_button.x + 10, self.pause_button.y + 5))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.solving and not self.game_over:
                    self.start_solve()
                if event.key == pygame.K_r and self.game_over:
                    self.create_disks()
                    self.reset_positions()
                    self.game_over = False
                if event.key == pygame.K_p:  # Toggle pause menu with 'P' key
                    self.is_paused = not self.is_paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_paused:
                    self.pause_menu.handle_click(event.pos)
                elif self.pause_button.collidepoint(event.pos):
                    self.is_paused = not self.is_paused

    def run(self):
        while True:
            self.screen.fill(BG_COLOR)
            self.handle_events()
            self.text_counter += 1

            if self.is_paused:
                self.pause_menu.draw()
                if self.pause_menu.action == "resume":
                    self.is_paused = False
                    self.pause_menu.action = None  # Reset the action
                elif self.pause_menu.action == "main_menu":
                    # Handle returning to the main menu
                    self.pause_menu.action = None  # Reset the action
                    # Implement main menu logic here if needed
                self.draw_pause_play_button()
            else:
                if self.solving:
                    self.animate_move()

                self.draw_poles()
                for disk in self.disks:
                    disk.draw(self.screen)
                self.draw_text()
                self.draw_pause_play_button()

            pygame.display.flip()
            self.clock.tick(30)