import pygame
import sys
import time
import random

# Tower of Hanoi function
def hanoi(n, source, target, auxiliary, draw):
    if n == 1:
        move_disk(source, target, draw)
    else:
        hanoi(n - 1, source, auxiliary, target, draw)
        move_disk(source, target, draw)
        hanoi(n - 1, auxiliary, target, source, draw)

# Move disk and draw
def move_disk(source, target, draw):
    if source:
        disk = source.pop()
        target.append(disk)
        draw()
        time.sleep(0.5)

# Pygame visualization
def visualize_hanoi():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tower of Hanoi")

    clock = pygame.time.Clock()

    # Disk data
    num_disks = 5
    disks = [i + 1 for i in range(num_disks)]
    random.shuffle(disks)  # Random shuffle of disks

    # Pegs and disks setup
    pegs = [disks, [], []]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

    def draw():
        screen.fill((0, 0, 0))
        peg_width = 20
        peg_height = 200
        peg_x_positions = [200, 400, 600]
        base_y = 500

        # Draw pegs
        for x in peg_x_positions:
            pygame.draw.rect(screen, (255, 255, 255), (x, base_y - peg_height, peg_width, peg_height))

        # Draw disks
        for i, peg in enumerate(pegs):
            x = peg_x_positions[i] + peg_width // 2
            y = base_y
            for disk in reversed(peg):
                width = disk * 20
                height = 20
                pygame.draw.rect(screen, colors[disk - 1], (x - width // 2, y - height, width, height))
                y -= height

        pygame.display.flip()

    draw()

    # Solve Tower of Hanoi
    hanoi(num_disks, pegs[0], pegs[2], pegs[1], draw)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)

if __name__ == "__main__":
    visualize_hanoi()