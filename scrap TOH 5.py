import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Define screen size
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tower of Hanoi')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Disk Class
class Disk:
    def __init__(self, radius):
        self.radius = radius
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    
    def __repr__(self):
        return f"Disk({self.radius})"

# Pole Class
class Pole:
    def __init__(self, name, x):
        self.name = name
        self.x = x
        self.disks = []
    
    def add_disk(self, disk):
        self.disks.append(disk)
    
    def remove_disk(self):
        return self.disks.pop() if self.disks else None
    
    def top_disk(self):
        return self.disks[-1] if self.disks else None
    
    def __repr__(self):
        return f"Pole({self.name}, {self.disks})"

# Tower of Hanoi Class
class TowerOfHanoi:
    def __init__(self):
        self.poles = {
            'A': Pole('A', 150),
            'B': Pole('B', 300),
            'C': Pole('C', 450)
        }
        self.moves = []
        self.game_over = False

        # Initialize disks
        self.init_disks()

    def init_disks(self):
        # Create disks of sizes 1 to 5
        self.disks = [Disk(i * 30) for i in range(1, 6)]
        random.shuffle(self.disks)

        # Add disks to Pole A
        for disk in self.disks:
            self.poles['A'].add_disk(disk)

    def move_disk(self, from_pole, to_pole):
        # Get the disk to move
        disk = from_pole.remove_disk()

        # Validate move: can only move a smaller disk on top of a larger one
        if to_pole.top_disk() is None or disk.radius < to_pole.top_disk().radius:
            to_pole.add_disk(disk)
            self.moves.append((from_pole, to_pole, disk))
            return True
        else:
            # Invalid move, put it back
            from_pole.add_disk(disk)
            return False

    def solve(self, n, from_pole, to_pole, aux_pole):
        # Base case: If there are no disks to move, return
        if n == 0:
            return

        # Move n-1 disks to auxiliary pole
        self.solve(n - 1, from_pole, aux_pole, to_pole)

        # Move the nth disk to the target pole
        if from_pole.disks:  # Check if there's a disk to move
            if self.move_disk(from_pole, to_pole):
                self.animate_move(from_pole, to_pole)

        # Move n-1 disks from auxiliary pole to target pole
        self.solve(n - 1, aux_pole, to_pole, from_pole)

    def animate_move(self, from_pole, to_pole):
        # Pygame animation for moving disks
        screen.fill(WHITE)

        # Draw poles
        for pole in self.poles.values():
            self.draw_pole(pole)
        
        # Draw disks
        for pole in self.poles.values():
            self.draw_disks(pole)

        pygame.display.flip()
        time.sleep(0.5)  # Delay to visualize the move

    def draw_pole(self, pole):
        # Draw the pole as a rectangle
        pygame.draw.rect(screen, BLACK, (pole.x - 5, HEIGHT - 100, 10, 100))

    def draw_disks(self, pole):
        # Draw disks on the pole
        for i, disk in enumerate(pole.disks):
            pygame.draw.rect(screen, disk.color, 
                             (pole.x - disk.radius / 2, HEIGHT - 100 - (i + 1) * 30, disk.radius, 30))

    def is_solved(self):
        # Check if all disks are on pole C
        return len(self.poles['C'].disks) == 5

    def run(self):
        # Main game loop
        while not self.game_over:
            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            # Solve the puzzle
            if not self.is_solved():
                self.solve(5, self.poles['A'], self.poles['C'], self.poles['B'])
            
            # Game is over
            if self.is_solved():
                print("Puzzle solved!")
                self.game_over = True

        pygame.quit()

# Run the game
game = TowerOfHanoi()
game.run()