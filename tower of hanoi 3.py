import random
import logging

logging.basicConfig(level=logging.DEBUG)

class TowerOfHanoi:
    def __init__(self):
        self.towers = {
            'A': [],
            'B': [],
            'C': []
        }
        self.moves = []  # To store the moveset

    def setup(self):
        self.towers['A'] = random.sample(range(1, 6), 5)  # Only include numbers 1 to 5
        print("Initial Setup:")
        self.display()

    def display(self):
        print("Current Towers State:")
        for tower, disks in self.towers.items():
            print(f"Tower {tower}: {disks}")
        print("-" * 30)

    def move(self, source, destination):
        if self.is_valid_move(source, destination):
            disk = self.towers[source].pop()
            self.towers[destination].append(disk)
            self.record_move(source, destination, disk)
        else:
            print(f"Invalid move from {source} to {destination}. Attempting to correct...")
            auxiliary = 'B' if destination == 'C' else 'C'
            if self.is_valid_move(source, auxiliary):
                self.move(source, auxiliary)
                self.move(auxiliary, destination)

    def is_valid_move(self, source, destination):
        if source not in self.towers or destination not in self.towers:
            print(f"Invalid move: One of the towers '{source}' or '{destination}' does not exist.")
            return False
        
        if not self.towers[source]:
            print(f"Invalid move: {source} is empty.")
            return False
        
        if not self.towers[destination]:
            return True  # Can move to an empty peg
        
        if self.towers[source][-1] < self.towers[destination][-1]:
            return True
        
        print(f"Invalid move: Cannot place disk {self.towers[source][-1]} on top of disk {self.towers[destination][-1]}.")
        return False

    def record_move(self, source, destination, disk):
        self.moves.append(f"{source} -> {destination}")
        print(f"Moved disk {disk}: {source} -> {destination}")
        self.display()

    def solve(self, n, source, target, auxiliary):
        if n == 1:
            self.move(source, target)
        else:
            self.solve(n - 1, source, auxiliary, target)
            self.move(source, target)
            self.solve(n - 1, auxiliary, target, source)

    def validate_end_state(self):
        if len(self.towers['C']) == 5 and self.towers['C'] == sorted(self.towers['C'], reverse=True):
            print("\nSuccess! All disks are in Tower C in the correct order.")
        else:
            print("\nIncomplete or invalid final state detected.")

# Example usage
if __name__ == "__main__":
    game = TowerOfHanoi()
    game.setup()  # Initialize the game with a random order of disks

    # Solve the Tower of Hanoi for 5 disks
    game.solve(len(game.towers['A']), 'A', 'C', 'B')

    # Validate the final state
    game.validate_end_state()