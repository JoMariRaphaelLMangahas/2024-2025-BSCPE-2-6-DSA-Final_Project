import pygame
import time
import os
from pygame.locals import *
import sys
import pygame.sprite
import Main_Menu

sys.path.append(os.path.join(os.path.dirname(__file__), 'Pictures'))

os.environ['SDL_VIDEO_CENTERED'] = '1'

class SortingVisualizer:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        self.WIDTH = 800
        self.HEIGHT = 600

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (46, 46, 46)
        self.TEAL = (0, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        self.LIGHT_CYAN = (224, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BROWN = (139, 69, 19)
        self.BACKGROUND_COLOR = (20, 20, 50)  # Dark navy blue

        # Create screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        # Fonts
        self.font = pygame.font.SysFont("architype stedelijk", 20)
        self.input_font = pygame.font.SysFont("architype stedelijk", 30)
        self.menu_font = pygame.font.SysFont("architype fodor", 50)

        # Initialize background sprites
        self.first_homepage_bg = self.BackgroundSprite("Pictures/Sorting/start.png")
        self.second_homepage_bg = self.BackgroundSprite("Pictures/Sorting/select.png")

        # Sprite group to manage backgrounds
        self.background_group = pygame.sprite.Group()
        self.background_group.add(self.first_homepage_bg)  # Initially set the first homepage background

    class BackgroundSprite(pygame.sprite.Sprite):
        def __init__(self, image_path):
            super().__init__()
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (800, 600))
            self.rect = self.image.get_rect()

    def fade_in_out(self, next_screen_callback):
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill(self.BLACK)

        # Faster fade-out
        for alpha in range(0, 255, 20):  # Increase step size for a faster transition
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)  # Reduce delay for speed

        next_screen_callback()

        # Faster fade-in
        for alpha in range(255, 0, -20):  # Increase step size for a faster transition
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)  # Reduce delay for speed

    def draw_bars(self, numbers, highlight_indices=None):
        self.screen.fill(self.BACKGROUND_COLOR)
        max_val = max(numbers)
        num_bars = len(numbers)
        bar_width = (self.WIDTH // num_bars) - 2  # Added small gap

        for i, value in enumerate(numbers):
            color = self.BROWN if highlight_indices and i in highlight_indices else self.GREEN
            bar_height = int((value / max_val) * (self.HEIGHT - 100))
            bar_x = i * (bar_width + 2)
            bar_y = self.HEIGHT - bar_height

            # Draw the bar
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, bar_width, bar_height))

            # Render the number at the top of the bar
            number_surface = self.font.render(str(value), True, self.WHITE)
            number_rect = number_surface.get_rect(center=(bar_x + bar_width // 2, bar_y - 10))
            self.screen.blit(number_surface, number_rect)

        pygame.display.flip()

    def bubble_sort(self, numbers):
        n = len(numbers)
        for i in range(n):
            for j in range(0, n - i - 1):
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    self.draw_bars(numbers, highlight_indices=[j, j + 1])
                    pygame.time.wait(50)

    def insertion_sort(self, numbers):
        for i in range(1, len(numbers)):
            key = numbers[i]
            j = i - 1
            while j >= 0 and key < numbers[j]:
                numbers[j + 1] = numbers[j]
                j -= 1
                self.draw_bars(numbers, highlight_indices=[j + 1, j + 2])
                pygame.time.wait(50)
            numbers[j + 1] = key
            self.draw_bars(numbers, highlight_indices=[j + 1])
            pygame.time.wait(50)

    def selection_sort(self, numbers):
        for i in range(len(numbers)):
            min_idx = i
            for j in range(i + 1, len(numbers)):
                if numbers[j] < numbers[min_idx]:
                    min_idx = j
                self.draw_bars(numbers, highlight_indices=[i, j, min_idx])
                pygame.time.wait(50)
            numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]
            self.draw_bars(numbers, highlight_indices=[i, min_idx])
            pygame.time.wait(50)

    def merge_sort(self, numbers, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(numbers, left, mid)
            self.merge_sort(numbers, mid + 1, right)
            self.merge(numbers, left, mid, right)

    def merge(self, numbers, left, mid, right):
        left_half = numbers[left:mid + 1]
        right_half = numbers[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                numbers[k] = left_half[i]
                i += 1
            else:
                numbers[k] = right_half[j]
                j += 1
            k += 1
            self.draw_bars(numbers, highlight_indices=range(left, right + 1))
            pygame.time.wait(50)
        while i < len(left_half):
            numbers[k] = left_half[i]
            i += 1
            k += 1
            self.draw_bars(numbers, highlight_indices=range(left, right + 1))
            pygame.time.wait(50)
        while j < len(right_half):
            numbers[k] = right_half[j]
            j += 1
            k += 1
            self.draw_bars(numbers, highlight_indices=range(left, right + 1))
            pygame.time.wait(50)

    def quick_sort(self, numbers, low, high):
        if low < high:
            pi = self.partition(numbers, low, high)
            self.quick_sort(numbers, low, pi - 1)
            self.quick_sort(numbers, pi + 1, high)

    def partition(self, numbers, low, high):
        pivot = numbers[high]
        i = low - 1
        for j in range(low, high):
            if numbers[j] < pivot:
                i += 1
                numbers[i], numbers[j] = numbers[j], numbers[i]
                self.draw_bars(numbers, highlight_indices=[i, j, high])
                pygame.time.wait(50)
        numbers[i + 1], numbers[high] = numbers[high], numbers[i + 1]
        self.draw_bars(numbers, highlight_indices=[i + 1, high])
        pygame.time.wait(50)
        return i + 1

    def shell_sort(self, numbers):
        n = len(numbers)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = numbers[i]
                j = i
                while j >= gap and numbers[j - gap] > temp:
                    numbers[j] = numbers[j - gap]
                    j -= gap
                    self.draw_bars(numbers, highlight_indices=[j, j + gap])
                    pygame.time.wait(50)
                numbers[j] = temp
                self.draw_bars(numbers, highlight_indices=[j, i])
                pygame.time.wait(50)
            gap //= 2

    def heap_sort(self, numbers):
        n = len(numbers)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(numbers, n, i)
        for i in range(n - 1, 0, -1):
            numbers[i], numbers[0] = numbers[0], numbers[i]
            self.draw_bars(numbers, highlight_indices=[0, i])
            pygame.time.wait(50)
            self.heapify(numbers, i, 0)

    def heapify(self, numbers, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and numbers[i] < numbers[left]:
            largest = left
        if right < n and numbers[largest] < numbers[right]:
            largest = right
        if largest != i:
            numbers[i], numbers[largest] = numbers[largest], numbers[i]
            self.draw_bars(numbers, highlight_indices=[i, largest])
            pygame.time.wait(50)
            self.heapify(numbers, n, largest)

    def second_homepage(self):
        self.background_group.empty()
        self.background_group.add(self.second_homepage_bg)  # Switch to the second homepage background

        def render():
            running = True
            button_width, button_height = 120, 30  # Button dimensions
            button_spacing_x = 40  # Horizontal space between buttons
            button_spacing_y = 20  # Vertical space between rows

            # Adjusted starting position for buttons
            start_x = self.WIDTH // 2 - 30  # Move the buttons further to the right
            start_y = 170  # Move the buttons lower

            # Define button positions and actions
            buttons = [
                ("BUBBLE", start_x, start_y + 75, self.bubble_sort),
                ("SHELL", start_x + 160, start_y + 80, self.shell_sort),
                ("INSERTION", start_x + 2, start_y + 150, self.insertion_sort),
                ("QUICK", start_x + button_width + button_spacing_x + 10, start_y + button_height + button_spacing_y + 100, lambda nums: self.quick_sort(nums, 0, len(nums) - 1)),
                ("SELECTION", start_x, start_y + 4.4 * (button_height + button_spacing_y), self.selection_sort),
                ("HEAP", start_x + button_width + button_spacing_x, start_y + 4.4 * (button_height + button_spacing_y), self.heap_sort),
                ("MERGE", start_x, start_y + 5.8 * (button_height + button_spacing_y), lambda nums: self.merge_sort(nums, 0, len(nums) - 1)),
                ("BACK", start_x + button_width + button_spacing_x, start_y + 5.8 * (button_height + button_spacing_y), "back"),
            ]

            while running:
                self.screen.fill(self.BACKGROUND_COLOR)
                self.background_group.draw(self.screen)  # Draw the second homepage background

                # Draw invisible buttons (no visible shape or text)
                for text, x, y, action in buttons:
                    button_rect = pygame.Rect(x, y, button_width, button_height)
                    # Do not draw anything for the button region, making it invisible
                    # No hover or color change

                # Event Handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for text, x, y, action in buttons:
                            button_rect = pygame.Rect(x, y, button_width, button_height)
                            if button_rect.collidepoint(event.pos):  # Click detection remains
                                if action == "back":
                                    self.fade_in_out(self.first_homepage)  # Action for "Back" button
                                elif action:
                                    self.fade_in_out(lambda: self.input_numbers(action))

                pygame.display.flip()

        self.fade_in_out(render)

    def input_numbers(self, algorithm):
        def render():
            running = True
            numbers = []
            
            input_box = pygame.Rect(self.WIDTH // 2 - 320, self.HEIGHT // 2 - 50, 400, 150)  
            input_text = ""
            cursor_visible = True
            cursor_timer = pygame.time.get_ticks()
            select_all = False
            undo_stack = []
            redo_stack = []

            background_image = pygame.image.load("Pictures/Sorting/input.png")
            background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))

            while running:
                self.screen.blit(background_image, (0, 0))

                pygame.draw.rect(self.screen, self.WHITE, input_box, border_radius=10)  # Corrected the first argument
                wrapped_text = self.wrap_text(input_text, self.input_font, input_box.width)

                for i, line in enumerate(wrapped_text):
                    if select_all:
                        # Draw blue background for selected text
                        text_surface = self.input_font.render(line, True, self.BLACK)
                        text_rect = text_surface.get_rect(topleft=(input_box.x + 10, input_box.y + 10 + i * 30))
                        pygame.draw.rect(self.screen, self.LIGHT_BLUE, text_rect)
                        self.screen.blit(text_surface, text_rect)
                    else:
                        text_surface = self.input_font.render(line, True, self.BLACK)
                        self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 10 + i * 30))

                # Blinking cursor logic
                if pygame.time.get_ticks() - cursor_timer > 500:
                    cursor_visible = not cursor_visible
                    cursor_timer = pygame.time.get_ticks()

                if cursor_visible and not select_all:
                    # Calculate cursor position based on wrapped text
                    if wrapped_text:
                        last_line = wrapped_text[-1]
                        cursor_x = input_box.x + 10 + self.input_font.size(last_line)[0]
                        cursor_y = input_box.y + 10 + (len(wrapped_text) - 1) * 30
                    else:
                        cursor_x = input_box.x + 10
                        cursor_y = input_box.y + 10
                    pygame.draw.rect(self.screen, self.BLACK, (cursor_x, cursor_y, 2, self.input_font.get_height()))

                back_button = pygame.Rect(self.WIDTH // 2 + 120, self.HEIGHT // 2 + 30, 150, 50)
                enter_button = pygame.Rect(self.WIDTH // 2 + 120, self.HEIGHT // 2 - 30, 150, 50)

                # Buttons remain interactive but are not drawn
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if back_button.collidepoint(mouse_pos):
                            self.fade_in_out(self.second_homepage)  # Ensures proper transition back
                            return  

                        if enter_button.collidepoint(mouse_pos):
                            try:
                                numbers = list(map(int, input_text.split()))
                                if numbers:  # Ensure at least one number is entered
                                    self.fade_in_out(lambda: algorithm(numbers))  # Run the sorting algorithm
                                    return  
                            except ValueError:
                                input_text = "Invalid input, try again!"  

                    if event.type == pygame.KEYDOWN:
                        if select_all:
                            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                undo_stack.append(input_text)
                                input_text = ""
                                select_all = False
                            else:
                                continue
                        elif event.key == pygame.K_BACKSPACE:
                            undo_stack.append(input_text)
                            input_text = input_text[:-1]
                        elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            select_all = True
                        elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            try:
                                clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')
                                undo_stack.append(input_text)
                                input_text += clipboard_text
                            except:
                                pass
                        elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            if undo_stack:
                                redo_stack.append(input_text)
                                input_text = undo_stack.pop()
                        elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            if redo_stack:
                                undo_stack.append(input_text)
                                input_text = redo_stack.pop()
                        else:
                            undo_stack.append(input_text)
                            input_text += event.unicode

                pygame.display.flip()  # Ensure screen updates properly

        self.fade_in_out(render)

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def first_homepage(self):
        self.background_group.empty()
        self.background_group.add(self.first_homepage_bg)  # Switch to the first homepage background

        running = True
        start_button = pygame.Rect(300, 280, 200, 50)  # Start button area
        exit_button = pygame.Rect(10, 10, 200, 50)   # Exit button area

        while running:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.background_group.draw(self.screen)  # Draw the first homepage background

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.fade_in_out(self.second_homepage)
                    if exit_button.collidepoint(event.pos):
                        Main_Menu.MainMenu().display()  # Call the main menu
                        return  # Exit the current function

            pygame.display.update()

    def run(self):
        self.first_homepage()