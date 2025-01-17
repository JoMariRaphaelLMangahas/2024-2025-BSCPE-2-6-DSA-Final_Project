import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Disk class
class Disk:
    def __init__(self, radius):
        self.radius = radius
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def draw(self, x, y):
        pygame.draw.rect(screen, self.color, pygame.Rect(x - self.radius, y, self.radius * 2, 20))


# Pole class
class Pole:
    def __init__(self, x):
        self.x = x
        self.disks = []

    def draw(self):
        pygame.draw.line(screen, BLACK, (self.x, 100), (self.x, 300), 5)
        for i, disk in enumerate(self.disks):
            disk.draw(self.x, 300 - 30 * (i + 1))

    def push(self, disk):
        if len(self.disks) == 0 or self.disks[-1].radius > disk.radius:
            self.disks.append(disk)
            return True
        return False

    def pop(self):
        if self.disks:
            return self.disks.pop()
        return None


# Game class
class TowerOfHanoi:
    def __init__(self):
        self.poles = [Pole(150), Pole(300), Pole(450)]  # Three poles at different x positions
        self.moves = []  # Store the sequence of moves
        self.generate_disks()  # Create and shuffle disks

    def generate_disks(self):
        # Create 5 disks and shuffle them
        self.disks = [Disk(radius) for radius in range(1, 6)]
        random.shuffle(self.disks)

        # Push all disks to pole A
        for disk in self.disks:
            self.poles[0].push(disk)

    def move_disk(self, from_pole, to_pole):
        disk = from_pole.pop()
        if disk:
            if to_pole.push(disk):
                self.moves.append((from_pole, to_pole))
                return True
        return False

    def draw(self):
        screen.fill(WHITE)
        for pole in self.poles:
            pole.draw()

    def solve(self, n, from_pole, to_pole, aux_pole):
        if n == 0:
            return
        # Move n-1 disks to auxiliary pole
        self.solve(n - 1, from_pole, aux_pole, to_pole)
        # Move the nth disk to destination pole
        self.move_disk(from_pole, to_pole)
        # Move n-1 disks from auxiliary pole to destination pole
        self.solve(n - 1, aux_pole, to_pole, from_pole)

    def is_solved(self):
        # Check if all disks are in pole C
        return len(self.poles[2].disks) == 5


def main():
    clock = pygame.time.Clock()
    game = TowerOfHanoi()
    running = True
    game_solved = False
    game.draw()

    while running:
        clock.tick(60)  # Set FPS to 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_solved:
            # Solve the puzzle if not solved
            game.solve(5, game.poles[0], game.poles[2], game.poles[1])
            game_solved = True

        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()