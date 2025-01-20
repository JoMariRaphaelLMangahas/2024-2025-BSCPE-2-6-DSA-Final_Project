import pygame
import random
import sys
from Pause_Menu import PauseMenu
import os
# Add the Pictures folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Pictures'))

os.environ['SDL_VIDEO_CENTERED'] = '1'

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeVisualizer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def calculate_tree_height(self, node):
        if not node:
            return 0
        return 1 + max(self.calculate_tree_height(node.left), self.calculate_tree_height(node.right))

    def draw_tree(self, node, x, y, spacing):
        if node:
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 20)
            text = self.font.render(str(node.value), True, (255, 255, 255))
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
            if node.left:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x - spacing, y + 80), 2)
                self.draw_tree(node.left, x - spacing, y + 80, spacing // 2)
            if node.right:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + spacing, y + 80), 2)
                self.draw_tree(node.right, x + spacing, y + 80, spacing // 2)

    def highlight_node(self, node, x, y):
        pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 20)
        text = self.font.render(str(node.value), True, (255, 255, 255))
        self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(500)

    def animate_traversal(self, node, order, x, y, spacing):
        if not node:
            return
        if order == "preorder":
            self.highlight_node(node, x, y)
        self.animate_traversal(node.left, order, x - spacing, y + 80, spacing // 2)
        if order == "inorder":
            self.highlight_node(node, x, y)
        self.animate_traversal(node.right, order, x + spacing, y + 80, spacing // 2)
        if order == "postorder":
            self.highlight_node(node, x, y)

class BinaryTree:
    def __init__(self, elements, max_depth):
        self.root = None
        self.root_elements = elements
        self.retained_elements = []  # Store elements actually in the tree
        for el in elements:
            self.root = self.insert(self.root, el)
        self.root = self.clamp_depth(self.root, 0, max_depth)
        self.retained_elements = []  # Update the retained elements list
        self.collect_retained_elements(self.root)

    def collect_retained_elements(self, node):
        """Collect all elements actually present in the tree."""
        if node:
            self.retained_elements.append(node.value)
            self.collect_retained_elements(node.left)
            self.collect_retained_elements(node.right)

    def insert(self, root, value):
        if not root:
            return TreeNode(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    def clamp_depth(self, node, current_depth, max_depth):
        if not node or current_depth >= max_depth:
            return None
        node.left = self.clamp_depth(node.left, current_depth + 1, max_depth)
        node.right = self.clamp_depth(node.right, current_depth + 1, max_depth)
        return node

    def traverse(self, node, order, result):
        if not node:
            return
        if order == "preorder":
            result.append(node.value)
        self.traverse(node.left, order, result)
        if order == "inorder":
            result.append(node.value)
        self.traverse(node.right, order, result)
        if order == "postorder":
            result.append(node.value)

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.is_open = False

    def draw_pause_menu_button(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, 40, 40))
        text = self.font.render("lll", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

    def handle_button_click(self, pos):
        """Handle click on the 'lll' pause button."""
        # Check if the click is within the 'lll' button bounds
        if 10 <= pos[0] <= 50 and 10 <= pos[1] <= 50:
            return True  # Indicate that the button was clicked
        return False
    
    def draw_level_selector(self, screen_width, screen_height, max_levels, selected_level):
        # Button dimensions and location
        button_width, button_height = 40, 40
        total_width = button_width * max_levels + (max_levels - 1) * 10
        start_x = (screen_width - total_width) // 2
        y = screen_height - button_height - 80  # 80px above "Generate New List" button

        for i in range(1, max_levels + 1):
            x = start_x + (i - 1) * (button_width + 10)
            color = (0, 200, 0) if i == selected_level else (200, 200, 200)
            pygame.draw.rect(self.screen, color, (x, y, button_width, button_height))

            # Draw the level number inside the button
            text = self.font.render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (x + (button_width - text.get_width()) // 2, y + (button_height - text.get_height()) // 2))

    def draw_generate_button(self, screen_width, screen_height):
        button_width, button_height = 200, 50
        x = (screen_width - button_width) // 2
        y = screen_height - button_height - 20  # 20px padding from the bottom
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, button_width, button_height))
        text = self.font.render("Generate New List", True, (255, 255, 255))
        self.screen.blit(text, (x + (button_width - text.get_width()) // 2, y + (button_height - text.get_height()) // 2))

    def handle_level_click(self, pos, screen_width, screen_height, max_levels):
        # Button dimensions and location
        button_width, button_height = 40, 40
        total_width = button_width * max_levels + (max_levels - 1) * 10
        start_x = (screen_width - total_width) // 2
        y = screen_height - button_height - 80  # Same y-coordinate as the level selector

        for i in range(1, max_levels + 1):
            x = start_x + (i - 1) * (button_width + 10)
            if x <= pos[0] <= x + button_width and y <= pos[1] <= y + button_height:
                return i
        return None

    def handle_generate_click(self, pos, screen_width, screen_height):
        button_width, button_height = 200, 50
        x = (screen_width - button_width) // 2
        y = screen_height - button_height - 20  # 20px padding from the bottom
        return x <= pos[0] <= x + button_width and y <= pos[1] <= y + button_height

class Application:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Binary Tree Traversal Visualizer")
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()
        elements = random.sample(range(1, 100), random.randint(5, 31))
        self.tree = BinaryTree(elements, 5)
        self.visualizer = TreeVisualizer(self.screen, self.font)
        self.menu = Menu(self.screen, self.font)
        self.pause_menu = PauseMenu(self.screen, self.font)
        self.orders = ["preorder", "inorder", "postorder"]
        self.order_names = {"preorder": "Pre-order (TLR)", "inorder": "In-order (LRT)", "postorder": "Post-order (LTR)"}
        self.current_order = 0
        self.max_levels = 5
        self.selected_level = 5

        # Store traversal results
        self.traversals = {order: [] for order in self.orders}
        for order in self.orders:
            self.tree.traverse(self.tree.root, order, self.traversals[order])
        
        self.is_paused = False

    def split_text(self, text, max_width):
        """Splits the text into multiple lines to fit within the screen width."""
        words = text.split(', ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (", " if current_line else "") + word
            rendered_line = self.font.render(test_line, True, (0, 0, 0))
            if rendered_line.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
    
    def generated_list(self, start_y_offset=470, padding=20, font_color=(0, 0, 0)):
        list_text = f"Generated List : {', '.join(map(str, self.tree.retained_elements))}"
        lines = self.split_text(list_text, self.WIDTH - padding)  # Adjust width for padding
        y_offset = start_y_offset  # Start position for the first line

        for line in lines:
            rendered_line = self.font.render(line, True, font_color)
            self.screen.blit(rendered_line, (10, y_offset))  # Render the line at (10, y_offset)
            y_offset += rendered_line.get_height() + 5  # Increment y_offset for line spacing

    def generated_list(self):
        list_text = f"Generated List : {', '.join(map(str, self.tree.retained_elements))}"
        lines = self.split_text(list_text, self.WIDTH - 20)  # 20 px padding
        y_offset = 470  # Start position below the BST
        for line in lines:
            rendered_line = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(rendered_line, (10, y_offset))
            y_offset += rendered_line.get_height() + 5  # Line spacing

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            # Draw the binary search tree
            self.visualizer.draw_tree(self.tree.root, self.WIDTH // 2, 100, 200)

            # Draw the menu button
            self.menu.draw_pause_menu_button()

            # If the game is paused, display the pause menu
            if self.is_paused:
                self.pause_menu.draw()
                if self.pause_menu.action == "resume":
                    self.is_paused = False
                    self.pause_menu.action = None  # Reset the action
                elif self.pause_menu.action == "main_menu":
                    # Handle returning to the main menu
                    self.pause_menu.action = None  # Reset the action
                    # Implement main menu logic here if needed
            else:
                # Draw menu or traversal text
                if self.menu.is_open:
                    self.menu.draw_pause_menu_button()
                else:
                    # Center the traversal text at the top
                    traversal_text = self.font.render(f"Traversal: {self.order_names[self.orders[self.current_order]]}", True, (0, 0, 0))
                    self.screen.blit(traversal_text, (self.WIDTH // 2 - traversal_text.get_width() // 2, 10))

            # Display the level selector
            self.menu.draw_level_selector(self.WIDTH, self.HEIGHT, self.max_levels, self.selected_level)

            # Display the "Generate New List" button
            self.menu.draw_generate_button(self.WIDTH, self.HEIGHT)

            # Display the generated list, split into multiple lines
            list_text = f"Generated List : {', '.join(map(str, self.tree.retained_elements))}"
            lines = self.split_text(list_text, self.WIDTH - 20)  # 20 px padding
            y_offset = 470  # Start position below the BST
            for line in lines:
                rendered_line = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(rendered_line, (10, y_offset))
                y_offset += rendered_line.get_height() + 5  # Line spacing

            # Display traversals
            for order in self.orders:
                traversal_text = f"{self.order_names[order]}: {', '.join(map(str, self.traversals[order]))}"
                lines = self.split_text(traversal_text, self.WIDTH - 20)
                for line in lines:
                    rendered_line = self.font.render(line, True, (0, 0, 0))
                    self.screen.blit(rendered_line, (10, y_offset))
                    y_offset += rendered_line.get_height() + 5  # Line spacing

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.menu.is_open:
                        self.visualizer.animate_traversal(self.tree.root, self.orders[self.current_order], self.WIDTH // 2, 100, 200)
                        self.current_order = (self.current_order + 1) % len(self.orders)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_paused:
                        self.pause_menu.handle_click(event.pos)
                    else:
                        if self.menu.handle_button_click(event.pos):
                            self.is_paused = not self.is_paused  # Toggle pause state

                        # Handle level selection
                        selected_level = self.menu.handle_level_click(event.pos, self.WIDTH, self.HEIGHT, self.max_levels)
                        if selected_level:
                            self.selected_level = selected_level
                            self.tree = BinaryTree(random.sample(range(1, 100), random.randint(5, 31)), self.selected_level)
                            self.traversals = {order: [] for order in self.orders}
                            for order in self.orders:
                                self.tree.traverse(self.tree.root, order, self.traversals[order])

                        # Handle generate new list button
                        elif self.menu.handle_generate_click(event.pos, self.WIDTH, self.HEIGHT):
                            self.tree = BinaryTree(random.sample(range(1, 100), random.randint(5, 31)), self.selected_level)
                            self.traversals = {order: [] for order in self.orders}
                            for order in self.orders:
                                self.tree.traverse(self.tree.root, order, self.traversals[order])

            # Update the display
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()