import pygame
import sys
import os
import random
from Pause_Menu import PauseMenu

os.environ['SDL_VIDEO_CENTERED'] = '1'

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def in_order_traversal(self, node, result):
        if node:
            self.in_order_traversal(node.left, result)
            result.append(node.value)
            self.in_order_traversal(node.right, result)

    def pre_order_traversal(self, node, result):
        if node:
            result.append(node.value)
            self.pre_order_traversal(node.left, result)
            self.pre_order_traversal(node.right, result)

    def post_order_traversal(self, node, result):
        if node:
            self.post_order_traversal(node.left, result)
            self.post_order_traversal(node.right, result)
            result.append(node.value)

class TreeVisualizer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_tree(self, node, x, y, spacing, y_offset):
        if node:
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y + y_offset), 20)
            text = self.font.render(str(node.value), True, (255, 255, 255))
            self.screen.blit(text, (x - text.get_width() // 2, y + y_offset - text.get_height() // 2))
            if node.left:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y + y_offset), (x - spacing, y + 80 + y_offset), 2)
                self.draw_tree(node.left, x - spacing, y + 80, spacing // 2, y_offset)
            if node.right:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y + y_offset), (x + spacing, y + 80 + y_offset), 2)
                self.draw_tree(node.right, x + spacing, y + 80, spacing // 2, y_offset)

    def highlight_node(self, node, x, y, y_offset):
        pygame.draw.circle(self.screen, (255, 0, 0), (x, y + y_offset), 20)
        text = self.font.render(str(node.value), True, (255, 255, 255))
        self.screen.blit(text, (x - text.get_width() // 2, y + y_offset - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(500)

    def animate_traversal(self, node, order, x, y, spacing, y_offset):
        if not node:
            return
        if order == "preorder":
            self.highlight_node(node, x, y, y_offset)
        self.animate_traversal(node.left, order, x - spacing, y + 80, spacing // 2, y_offset)
        if order == "inorder":
            self.highlight_node(node, x, y, y_offset)
        self.animate_traversal(node.right, order, x + spacing, y + 80, spacing // 2, y_offset)
        if order == "postorder":
            self.highlight_node(node, x, y, y_offset)

class BinarySearchTreeApp:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1200, 800  # Increased screen size
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Binary Search Tree")
        self.font = pygame.font.Font(None, 36)
        self.bold_font = pygame.font.Font(None, 36)
        self.bold_font.set_bold(True)
        self.clock = pygame.time.Clock()

        self.bst = BinarySearchTree()
        self.visualizer = TreeVisualizer(self.screen, self.font)
        self.pause_menu = PauseMenu(self.screen, self.font)  # Initialize the PauseMenu

        self.number_to_generate = ""
        self.input_active = False
        self.input_box = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 100, 200, 40)
        self.generate_button = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT - 50, 300, 50)
        self.toggle_button = pygame.Rect(50, self.HEIGHT - 50, 300, 50)

        self.running = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.show_results = False
        self.is_paused = False
        self.scroll_y = 0

        self.in_order_result = []
        self.pre_order_result = []
        self.post_order_result = []
        self.random_values = []

        self.orders = ["preorder", "inorder", "postorder"]
        self.order_names = {"preorder": "Pre-order (TLR)", "inorder": "In-order (LRT)", "postorder": "Post-order (LTR)"}
        self.current_order = 0

        self.blink = True
        self.blink_timer = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self.handle_events()
            self.update_screen()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_paused:
                    self.pause_menu.handle_click(event.pos)
                else:
                    if self.input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

                    if self.generate_button.collidepoint(event.pos):
                        if self.number_to_generate.isdigit() and 0 < int(self.number_to_generate) <= 30:
                            self.number_to_generate = int(self.number_to_generate)
                            self.bst = BinarySearchTree()
                            self.random_values = [random.randint(1, 100) for _ in range(self.number_to_generate)]
                            for value in self.random_values:
                                self.bst.insert(value)

                            self.in_order_result = []
                            self.pre_order_result = []
                            self.post_order_result = []

                            self.bst.in_order_traversal(self.bst.root, self.in_order_result)
                            self.bst.pre_order_traversal(self.bst.root, self.pre_order_result)
                            self.bst.post_order_traversal(self.bst.root, self.post_order_result)

                            print("Generated List:", self.random_values)
                            print("In-order Traversal (LRT):", self.in_order_result)
                            print("Pre-order Traversal (TLR):", self.pre_order_result)
                            print("Post-order Traversal (LTR):", self.post_order_result)

                            self.number_to_generate = ""  # Reset input box

                    if self.toggle_button.collidepoint(event.pos):
                        self.show_results = not self.show_results

                    if self.pause_menu.is_open:
                        self.pause_menu.handle_click(event.pos)
                    elif pygame.Rect(10, 10, 40, 40).collidepoint(event.pos):
                        self.is_paused = not self.is_paused
                        self.pause_menu.toggle()

            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.number_to_generate = self.number_to_generate[:-1]
                    else:
                        self.number_to_generate += event.unicode
                elif event.key == pygame.K_SPACE and not self.is_paused:
                    self.visualizer.animate_traversal(self.bst.root, self.orders[self.current_order], self.WIDTH // 2, 50, self.WIDTH // 4, self.scroll_y)
                    self.current_order = (self.current_order + 1) % len(self.orders)
                elif event.key == pygame.K_UP:
                    self.scroll_y += 20
                elif event.key == pygame.K_DOWN:
                    self.scroll_y -= 20

            if event.type == pygame.MOUSEWHEEL:
                self.scroll_y += event.y * 20

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        if self.show_results:
            self.display_results()
        else:
            self.display_main()

        if self.is_paused:
            self.pause_menu.draw()
            if self.pause_menu.action == "resume":
                self.is_paused = False
                self.pause_menu.action = None  # Reset the action
            elif self.pause_menu.action == "main_menu":
                # Handle returning to the main menu
                self.pause_menu.action = None  # Reset the action
                # Implement main menu logic here if needed

        self.draw_pause_menu_button()

        pygame.display.flip()

    def draw_pause_menu_button(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 40, 40))
        if self.is_paused:
            text = self.bold_font.render("▶", True, (0, 0, 0))
        else:
            text = self.bold_font.render("||", True, (0, 0, 0))
        self.screen.blit(text, (20, 20))

    def display_main(self):
        # Draw input box
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)
        input_text = self.font.render(str(self.number_to_generate), True, (0, 0, 0))
        self.screen.blit(input_text, (self.input_box.x + 5, self.input_box.y + 5))

        # Blinking cursor
        if self.input_active:
            self.cursor_timer += 1
            if self.cursor_timer % 60 < 30:
                cursor = self.font.render("|", True, (0, 0, 0))
                self.screen.blit(cursor, (self.input_box.x + 5 + input_text.get_width(), self.input_box.y + 5))

        # Draw generate button with rounded corners
        pygame.draw.rect(self.screen, (0, 0, 0), self.generate_button, border_radius=10)
        generate_text = self.font.render("GENERATE LIST", True, (255, 255, 255))
        self.screen.blit(generate_text, (self.generate_button.x + (self.generate_button.width - generate_text.get_width()) // 2, self.generate_button.y + (self.generate_button.height - generate_text.get_height()) // 2))

        # Draw toggle button with rounded corners
        pygame.draw.rect(self.screen, (0, 0, 0), self.toggle_button, border_radius=10)
        toggle_text = self.font.render("SHOW RESULTS", True, (255, 255, 255))
        self.screen.blit(toggle_text, (self.toggle_button.x + (self.toggle_button.width - toggle_text.get_width()) // 2, self.toggle_button.y + (self.toggle_button.height - toggle_text.get_height()) // 2))

        # Draw labels
        label_text = self.font.render("NUMBER TO GENERATE (max 30)", True, (0, 0, 0))
        self.screen.blit(label_text, (self.WIDTH // 2 - label_text.get_width() // 2, self.HEIGHT - 150))

        if self.bst.root:
            self.visualizer.draw_tree(self.bst.root, self.WIDTH // 2, 50, self.WIDTH // 4, self.scroll_y)

        # Draw traversal results at the top center
        traversal_text = self.font.render(f"Traversal: {self.order_names[self.orders[self.current_order]]}", True, (0, 0, 0))
        self.screen.blit(traversal_text, (self.WIDTH // 2 - traversal_text.get_width() // 2, 20))

        # Blinking text "Press SPACE to start the traversal"
        if pygame.time.get_ticks() - self.blink_timer > 500:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()
        if self.blink:
            blink_text = self.font.render("Press SPACE to start the traversal", True, (255, 0, 0))
            self.screen.blit(blink_text, (self.WIDTH // 2 - blink_text.get_width() // 2, 100))

    def display_results(self):
        # Draw toggle button with rounded corners
        pygame.draw.rect(self.screen, (0, 0, 0), self.toggle_button, border_radius=10)
        toggle_text = self.font.render("BACK TO TREE", True, (255, 255, 255))
        self.screen.blit(toggle_text, (self.toggle_button.x + (self.toggle_button.width - toggle_text.get_width()) // 2, self.toggle_button.y + (self.toggle_button.height - toggle_text.get_height()) // 2))

        # Display generated list and traversal results
        y_offset = 50
        results = [
            ("Generated List:", self.random_values),
            ("Pre-order Traversal (TLR):", self.pre_order_result),
            ("In-order Traversal (LRT):", self.in_order_result),
            ("Post-order Traversal (LTR):", self.post_order_result)
        ]

        for title, result in results:
            title_text = self.font.render(title, True, (0, 0, 0))
            self.screen.blit(title_text, (50, y_offset))
            y_offset += 30

            # Split the result list into multiple lines if it's too long
            result_str = str(result)
            max_line_length = 110  # Adjust this value as needed
            while len(result_str) > max_line_length:
                split_index = result_str.rfind(',', 0, max_line_length) + 1
                if split_index == 0:
                    split_index = max_line_length
                line = result_str[:split_index]
                result_str = result_str[split_index:]
                result_text = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(result_text, (50, y_offset))
                y_offset += 30

            result_text = self.font.render(result_str, True, (0, 0, 0))
            self.screen.blit(result_text, (50, y_offset))
            y_offset += 50