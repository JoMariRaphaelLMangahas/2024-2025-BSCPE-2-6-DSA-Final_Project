import random

class TowerOfHanoi:
    def __init__(self):
        self.list_a = []
        self.list_b = []
        self.list_c = []
        self.moves = []  # To store the moveset
    
    def setup(self):
        # Generate the first 5 counting numbers in random order
        self.list_a = random.sample(range(1, 6), 5)
        print("Initial Setup:")
        self.display()
    
    def move(self, source, destination, auxiliary):
        # Ensure the move follows the rules of Tower of Hanoi
        if source and (not destination or source[-1] < destination[-1]):
            disk = source.pop()  # Use pop() for efficiency
            destination.append(disk)  # Use append() for efficiency
            self.record_move(source, destination)
        else:
            # If the move to the target is invalid, try moving to the auxiliary
            if source and (not auxiliary or source[-1] < auxiliary[-1]):
                disk = source.pop()
                auxiliary.append(disk)
                self.record_move(source, auxiliary)
                print(f"Moved disk {disk} to auxiliary: {self.get_list_name(source)} -> {self.get_list_name(auxiliary)}")
            else:
                # If the move to the auxiliary is also invalid, log the invalid move
                print(f"Invalid move attempted from {self.get_list_name(source)} to {self.get_list_name(destination)} and auxiliary.")
    
    def record_move(self, source, destination):
        # Record the move as "Source -> Destination"
        source_name = self.get_list_name(source)
        dest_name = self.get_list_name(destination)
        self.moves.append(f"{source_name} -> {dest_name}")
        print(f"Moved disk {destination[-1]}: {source_name} -> {dest_name}")
        self.display()

    def get_list_name(self, lst):
        if lst == self.list_a:
            return "A"
        elif lst == self.list_b:
            return "B"
        elif lst == self.list_c:
            return "C"
        return "Unknown"
    
    def display(self):
        print(f"List A: {self.list_a}")
        print(f"List B: {self.list_b}")
        print(f"List C: {self.list_c}")
        print("-" * 30)
    
    def solve(self, n, source, target, auxiliary):
        if n > 0:
            # Move n-1 disks from source to auxiliary using target as temporary
            self.solve(n - 1, source, target, auxiliary)
            # Attempt to move the nth disk from source to target
            self.move(source, target, auxiliary)
            # Move the n-1 disks from auxiliary to target using source as temporary
            self.solve(n - 1, auxiliary, source, target)
    
    def validate_and_fix(self):
        # Check if all numbers are in List C
        missing_disks = set(range(1, 6)) - set(self.list_c)
        if missing_disks:
            print(f"Missing disks in List C: {missing_disks}")
            self.undo_and_rebuild(missing_disks)
        
        # Ensure the largest disk is at the last index
        if self.list_c and max(self.list_c) != len(self.list_c):
            print("Adjusting to place the largest disk at the bottom of List C.")
            self.rearrange_largest_to_last()
    
    def undo_and_rebuild(self, missing_disks):
        print("Performing undo and rebuilding List C.")
        auxiliary = self.list_b if self.list_a else self.list_a  # Choose the auxiliary list
        
        # Step 1: Undo by moving all disks out of List C
        while self.list_c:
            self.move(self.list_c, auxiliary, self.list_b if auxiliary == self.list_a else self.list_a)
        
        # Step 2: Retrieve the missing disks in ascending order
        for missing_disk in sorted(missing_disks):
            source = self.list_a if missing_disk in self.list_a else self.list_b
            self.move(source, self.list_c, auxiliary)
        
        # Step 3: Rebuild List C in ascending order
        while auxiliary:
            self.move(auxiliary, self.list_c, self.list_a if auxiliary == self.list_b else self.list_b)
        
        print("Rebuild complete.")
        self.display()
    
    def rearrange_largest_to_last(self):
        # Ensure the largest disk is at the bottom of List C
        if self.list_c and max(self.list_c) != self.list_c[-1]:
            largest = max(self.list_c)
            self.list_c.remove(largest)
            self.list_c.append(largest)
            self.moves.append("Manual adjustment: Move largest disk to the bottom")
            print(f"Largest disk {largest} moved to the bottom of List C.")
            self.display()

    def validate_end_state(self):
        # Ensure all disks are in List C, and Lists A and B are empty
        if not self.list_a and not self.list_b and self.is_correct_order():
            print("\nSuccess! All disks are in List C in ascending order.")
        else:
            print("\nIncomplete or invalid final state detected.")
            self.validate_and_fix()

    def is_correct_order(self):
        # Check if List C contains disks in the correct order
        expected_order = list(range(5, 0, -1))  # [5, 4, 3, 2, 1]
        if self.list_c == expected_order:
            print("List C is in the correct order.")
            return True
        else:
            print("List C is not in the correct order.")
            return False
    
    def show_moveset(self):
        print("\nMoveset:")
        for move in self.moves:
            print(move)


# Create an instance of the TowerOfHanoi class
game = TowerOfHanoi()
game.setup()  # Initialize the game with a random order of disks

# Solve the Tower of Hanoi for 5 disks
game.solve(len(game.list_a), game.list_a, game.list_c, game.list_b)

# Validate and fix the final state
game.validate_end_state()

# Display the moveset
game.show_moveset()