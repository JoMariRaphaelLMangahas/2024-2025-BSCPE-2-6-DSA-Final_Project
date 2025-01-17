import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Experimental")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)

# Peg and disk dimensions
PEG_WIDTH = 10
PEG_HEIGHT = 200
DISK_HEIGHT = 20
DISK_COLORS = [(200, 100, 100), (100, 200, 100), (100, 100, 200), (200, 200, 100), (150, 150, 250)]

# Font setup
pygame.font.init()
font = pygame.font.SysFont(None, 24)

def draw_peg(x, y):
    pygame.draw.rect(screen, BLACK, (x - PEG_WIDTH // 2, y, PEG_WIDTH, PEG_HEIGHT))

def draw_disk(x, y, width, color, label):
    pygame.draw.rect(screen, color, (x - width // 2, y, width, DISK_HEIGHT))
    text = font.render(label, True, BLACK)
    screen.blit(text, (x - text.get_width() // 2, y + DISK_HEIGHT // 4))

# Peg positions
PEG_X_POSITIONS = [200, 400, 600]
PEG_Y = 400

# Disk setup
disks = []
num_disks = len(DISK_COLORS)
for i in range(num_disks):
    disks.append({
        "rect": pygame.Rect(200 - (120 - i * 20) // 2, PEG_Y - (i + 1) * DISK_HEIGHT, 120 - i * 20, DISK_HEIGHT),
        "color": DISK_COLORS[i],
        "label": str(num_disks - i),
        "held": False
    })

# Game loop
running = True
selected_disk = None
mouse_offset_x = 0
mouse_offset_y = 0

while running:
    screen.fill(WHITE)

    # Draw pegs
    for x in PEG_X_POSITIONS:
        draw_peg(x, PEG_Y)

    # Draw disks
    for disk in disks:
        rect = disk["rect"]
        color = disk["color"]
        label = disk["label"]
        draw_disk(rect.centerx, rect.y, rect.width, color, label)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for disk in disks:
                if disk["rect"].collidepoint(event.pos):
                    selected_disk = disk
                    mouse_offset_x = disk["rect"].x - event.pos[0]
                    mouse_offset_y = disk["rect"].y - event.pos[1]
                    disk["held"] = True
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if selected_disk:
                selected_disk["held"] = False
                selected_disk = None

    # Update selected disk position
    if selected_disk:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_disk["rect"].x = mouse_x + mouse_offset_x
        selected_disk["rect"].y = mouse_y + mouse_offset_y

    # Refresh the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()