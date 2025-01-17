import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Disk and pole setup
NUM_DISKS = 5
disk_colors = [RED, GREEN, BLUE, (255, 165, 0), (128, 0, 128)]

class TowerOfHanoi:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.poles = {"A": [], "B": [], "C": []}

        # Place all disks in ascending order on Pole A
        self.poles["A"] = list(range(1, num_disks + 1))

        self.disk_colors = [RED, GREEN, BLUE, (255, 165, 0), (128, 0, 128)]
        self.pole_positions = {"A": WIDTH // 4, "B": WIDTH // 2, "C": 3 * WIDTH // 4}
        self.disk_height = 20

    def draw(self):
        screen.fill(WHITE)

        # Draw poles
        pole_width = 10
        pole_height = 300
        for pole in self.pole_positions:
            x = self.pole_positions[pole] - pole_width // 2
            y = HEIGHT - pole_height
            pygame.draw.rect(screen, BLACK, (x, y, pole_width, pole_height))

        # Draw disks
        for pole, position in self.pole_positions.items():
            for i, disk in enumerate(self.poles[pole]):
                disk_width = disk * 20
                x = position - disk_width // 2
                y = HEIGHT - (i + 1) * self.disk_height
                color = self.disk_colors[disk - 1]
                pygame.draw.rect(screen, color, (x, y, disk_width, self.disk_height))

        pygame.display.flip()

    def can_move(self, from_pole, to_pole):
        # Check if the from_pole has any disks
        if not self.poles[from_pole]:
            return False
        # Check if the move is valid based on the Tower of Hanoi rules
        if not self.poles[to_pole] or self.poles[from_pole][-1] < self.poles[to_pole][-1]:
            return True
        return False

    def move_disk(self, from_pole, to_pole):
        if self.can_move(from_pole, to_pole):
            disk = self.poles[from_pole].pop()
            self.poles[to_pole].append(disk)
            self.draw()
            time.sleep(0.5)

    def solve_recursive(self, n, source, target, auxiliary):
        if n == 0:
            return

        self.solve_recursive(n - 1, source, auxiliary, target)
        self.move_disk(source, target)
        self.solve_recursive(n - 1, auxiliary, target, source)

    def solve(self):
        self.solve_recursive(self.num_disks, "A", "C", "B")

# Main loop
def main():
    game = TowerOfHanoi(NUM_DISKS)
    running = True
    game.draw()

    # Start solving
    game.solve()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()