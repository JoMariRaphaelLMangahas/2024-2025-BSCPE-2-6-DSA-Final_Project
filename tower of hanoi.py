import random
import pygame
import time

class TowerOfHanoi:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.towers = {
            'A': list(range(num_disks, 0, -1)),
            'B': [],
            'C': []
        }
        self.moves = []

    def shuffle_disks(self):
        random.shuffle(self.towers['A'])

    def solve(self, n, source, destination, auxiliary):
        if n == 0:
            return
        self.solve(n-1, source, auxiliary, destination)
        self.move_disk(source, destination)
        self.visualize()
        self.solve(n-1, auxiliary, destination, source)

    def can_move(self, source, destination):
        if not self.towers[source]:
            return False
        if not self.towers[destination]:
            return True
        return self.towers[source][-1] < self.towers[destination][-1]

    def move_disk(self, source, destination):
        if self.can_move(source, destination):
            disk = self.towers[source].pop()
            self.towers[destination].append(disk)
            self.moves.append(f"Move disk {disk} from {source} to {destination}")

    def transfer_numbers(self, source, destination, auxiliary, n):
        if n == 0:
            return
        self.transfer_numbers(source, auxiliary, destination, n-1)
        self.move_disk(source, destination)
        self.transfer_numbers(auxiliary, destination, source, n-1)

    def insertion_sort(self, tower):
        """Sort the disks in the specified tower using insertion sort."""
        for i in range(1, len(self.towers[tower])):
            key = self.towers[tower][i]
            j = i - 1
            while j >= 0 and key < self.towers[tower][j]:
                j -= 1
            self.towers[tower].insert(j + 1, self.towers[tower].pop(i))

    def check_and_fix_errors(self):
        if len(self.towers['C']) != self.num_disks or sorted(self.towers['C']) != list(range(1, self.num_disks + 1)):
            print("Error detected: Tower C does not have all the numbers.")
            # Transfer numbers from Tower C to Tower B
            self.transfer_numbers('C', 'B', 'A', len(self.towers['C']))
            # Place missing numbers in Tower C
            for i in range(1, self.num_disks + 1):
                if i not in self.towers['C']:
                    print(f"Placing missing number {i} in Tower C")
                    self.towers['C'].append(i)
            # Transfer numbers back from Tower B to Tower C
            self.transfer_numbers('B', 'C', 'A', len(self.towers['B']))
            # Sort Tower C using insertion sort
            self.insertion_sort('C')

    def fix_stationary_disk(self):
        if len(self.towers['C']) > 1 and self.towers['C'][-2] == self.num_disks - 1:
            print("Stationary disk detected: Fixing the issue.")
            empty_tower = 'A' if not self.towers['A'] else 'B'
            # Transfer all disks from Tower C to the empty tower
            self.transfer_numbers('C', empty_tower, 'A' if empty_tower == 'B' else 'B', len(self.towers['C']))
            # Place the largest disk in Tower C
            self.towers['C'].append(self.num_disks)
            # Transfer all disks back to Tower C
            self.transfer_numbers(empty_tower, 'C', 'A' if empty_tower == 'B' else 'B', len(self.towers[empty_tower]))

    def visualize(self):
        screen.fill((255, 255, 255))
        for i, tower in enumerate(['A', 'B', 'C']):
            for j, disk in enumerate(self.towers[tower]):
                pygame.draw.rect(screen, (0, 0, 255), (i*200 + 100 - disk*10, 400 - j*20, disk *20, 20))
        pygame.display.flip()
        time.sleep(0.5)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Tower of Hanoi")

# Example usage
num_disks = 5  # You can change this to any number of disks
game = TowerOfHanoi(num_disks)

# Shuffle the disks on Tower A
game.shuffle_disks()

# Visualize the initial state
game.visualize()

# Solve the Tower of Hanoi for the specified number of disks
game.solve(num_disks, 'A', 'C', 'B')

# Display the moves made
print("\nMoves made:")
for move in game.moves:
    print(move)

# Check and fix errors if any
game.check_and_fix_errors()

# Fix stationary disk if detected
game.fix_stationary_disk()

# Keep the final visualization open
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()