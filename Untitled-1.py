import random

class TowerOfHanoi:
    def __init__(self):
        self.towers = {
            'A': [],
            'B': [],
            'C': []
        }
        self.moves = []  # To store the moveset

    def setup(self):
        # Generate the first 5 counting numbers in random order
        self.towers['A'] = random.sample(range(1, 6), 5)  # Only include numbers 1 to 5
        print("Initial Setup:")
        self.display()

    def move(self, source, destination):
        # Ensure the move follows the rules of Tower of Hanoi
        if not self.towers[source]:
            print(f"Invalid move: {source} is empty.")
            return

        if not self.towers[destination] or self.towers[source][-1] < self.towers[destination][-1]:
            disk = self.towers[source].pop()  # Move the top disk from source
            self.towers[destination].append(disk)  # Place it on destination
            self.record_move(source, destination)
        else:
            print(f"Invalid move: Cannot place disk {self.towers[source][-1]} on top of disk {self.towers[destination][-1]}.")

    def record_move(self, source, destination):
        # Record the move as "Source -> Destination"
        disk = self.towers[destination][-1]
        self.moves.append(f"{source} -> {destination}")
        print(f"Moved disk {disk}: {source} -> {destination}")
        self.display()

    def display(self):
        print("Current Towers State:")
        for tower, disks in self.towers.items():
            print(f"Tower {tower}: {disks}")
        print("-" * 30)

    def solve(self, n, source, target, auxiliary):
        if n == 1:
            self.move(source, target)
        else:
            self.solve(n - 1, source, auxiliary, target)  # Move n-1 disks to auxiliary
            self.move(source, target)  # Move the nth disk to target
            self.solve(n - 1, auxiliary, target, source)  # Move n-1 disks from auxiliary to target

    def validate_end_state(self):
        # Ensure all disks are in Tower C and the count is 5
        if len(self.towers['C']) == 5 and self.towers['C'] == sorted(self.towers['C'], reverse=True):
            print("\nSuccess! All disks are in Tower C in the correct order.")
        else:
            print("\nIncomplete or invalid final state detected.")
            self.move_largest_to_front()

    def move_largest_to_front(self):
        # Find the largest disk in the current state and move it to the front of Tower C
        if self.towers['C']:
            largest_disk = max(self.towers['C'])
            self.towers['C'].remove(largest_disk)
            self.towers['C'].insert(0, largest_disk)  # Move to the front
            print(f"Moved largest disk {largest_disk} to the front of Tower C.")
            self.display()

    def show_moveset(self):
        print("\nMoveset:")
        for move in self.moves:
            print(move)


# Create an instance of the TowerOfHanoi class
game = TowerOfHanoi()
game.setup()  # Initialize the game with a random order of disks

# Solve the Tower of Hanoi for 5 disks
game.solve (len(game.towers['A']), 'A', 'C', 'B')

# Validate the final state
game.validate_end_state()

# Display the moveset
game.show_moveset()