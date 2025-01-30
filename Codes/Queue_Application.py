import pygame
import sys
import os
from Pause_Menu import PauseMenu  # Import PauseMenu

sys.path.append(os.path.join(os.path.dirname(__file__), 'Pictures'))

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height, target_y, plate_number, image):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_y = target_y
        self.plate_number = plate_number
        self.image_path = image_path
        self.is_departing = False

    def update(self):
        if self.is_departing:
            self.rect.y -= 5  # Move the car upwards for departure
        else:
            if self.rect.y < self.target_y:
                self.rect.y += 5  # Move the car downwards to its target position

class ParkingLot:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up screen and background
        self.screen = pygame.display.set_mode((800, 600))
        self.bg = pygame.image.load('Pictures/Cars and Parking/bg_stacks.png')
        self.bg = pygame.transform.scale(self.bg, (int(self.screen.get_width() * 1), int(self.screen.get_height() * 1)))

        # Set up sprite groups
        self.all_sprites = pygame.sprite.Group()

        # List of car images (im1, im2, im3, ..., im10)
        self.car_images = ['Pictures/Cars and Parking/im1.png', 'Pictures/Cars and Parking/im2.png', 'Pictures/Cars and Parking/im3.png', 
                           'Pictures/Cars and Parking/im4.png', 'Pictures/Cars and Parking/im5.png', 'Pictures/Cars and Parking/im6.png', 
                           'Pictures/Cars and Parking/im7.png', 'Pictures/Cars and Parking/im8.png', 'Pictures/Cars and Parking/im9.png',
                           'Pictures/Cars and Parking/im10.png']

        # Increase the scale width and height of the car images to make them bigger
        self.scale_width = 20
        self.scale_height = 50

        # Create vertical queue positions for the cars
        self.car_positions = []

        # Set initial positions and target positions for cars
        self.base_y = -self.scale_height  # Starting position off-screen at the top
        self.queue_spacing = 55  # Decrease vertical spacing between cars (smaller gap)

        # Create more space at the bottom for the first car by shifting it down slightly
        self.max_target_y = self.screen.get_height() - self.scale_height - 15  # Start the first car 30px from the bottom side

        # Calculate the center position for the cars horizontally
        self.center_x = (self.screen.get_width() - self.scale_width) // 1.87  # Center of the screen minus half the car's width

        # Create cars' target positions starting from the bottom and stacking upwards
        for i in range(10):  # Create 10 cars
            target_y = self.max_target_y - i * self.queue_spacing  # Decrease target_y for each car to stack them
            self.car_positions.append((self.center_x, self.base_y, target_y))  # Center cars horizontally, start off-screen vertically

        # Initialize cars
        self.cars_objects = []
        self.plate_numbers = []  # List to hold plate numbers
        self.parked_cars = []  # List to hold parked cars

        self.clock = pygame.time.Clock()
        self.current_car = -1  # Index of the car currently moving (-1 means no car moving yet)
        self.waiting_for_input = True
        self.arrived_count = 0  # Counter for the number of cars that have arrived
        self.departed_count = 0  # Counter for the number of cars that have departed
        self.total_arrivals = 0  # Add this line to initialize total arrivals

        # Buttons
        self.show_license_plate_button = pygame.Rect(250, 540, 300, 50)
        self.back_button = pygame.Rect(10, 10, 50, 50)  # Back button

        self.animation_in_progress = False  # Flag to indicate if animation is in progress
        self.selected_plate_number = None  # Initialize selected plate number
        self.pause_menu = PauseMenu(self.screen, pygame.font.SysFont(None, 48))  # Initialize PauseMenu
        self.is_paused = False  # Pause state
        self.pause_button = pygame.Rect(10, 10, 40, 40)  # Pause button

    def get_plate_number(self, arrived_count, is_departure=False, message=None):
        font = pygame.font.SysFont(None, 48)
        font_message = pygame.font.SysFont(None, 36)
        input_box = pygame.Rect(250, 250, 300, 50)
        text = ''
        active = True
        clock = pygame.time.Clock()
        cursor_visible = True
        cursor_timer = 0
        message_timer = pygame.time.get_ticks() if message else None

        button_rect_arrival = pygame.Rect(300, 390, 200, 50)  # Arrival button
        button_rect_departure = pygame.Rect(300, 460, 200, 50)  # Departure button
        button_color = (0, 128, 0)  # Green button for arrival
        button_hover_color = (0, 255, 0)  # Lighter green for hover effect
        departure_button_color = (255, 0, 0)  # Red button for departure
        departure_button_hover_color = (255, 50, 50)  # Lighter red for hover effect
        arrival_button_disabled_color = (169, 169, 169)  # Gray color for disabled arrival button

        departure_count = len(self.plate_numbers) - arrived_count

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Toggle pause menu with 'P' key
                        self.is_paused = not self.is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_paused:
                        self.pause_menu.handle_click(event.pos)
                    elif self.pause_button.collidepoint(event.pos):
                        self.is_paused = not self.is_paused

                if not self.animation_in_progress and not self.is_paused:  # Disable input during animation and pause
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect_arrival.collidepoint(event.pos) and arrived_count < 10:  # Arrival button clicked
                            if not text.strip():
                                message = "No plate number entered"
                                message_timer = pygame.time.get_ticks()
                            else:
                                return text, 'arrival'
                        if button_rect_departure.collidepoint(event.pos):  # Departure button clicked
                            if not text.strip():
                                message = "No plate number entered"
                                message_timer = pygame.time.get_ticks()
                            else:
                                plate_number_cleaned = text.strip().upper()
                                found_car = None
                                for car in self.cars_objects:
                                    if car.plate_number.strip().upper() == plate_number_cleaned:
                                        found_car = car
                                        break

                                if not found_car:
                                    message = "Car cannot be found."
                                    message_timer = pygame.time.get_ticks()
                                else:
                                    car_index = self.cars_objects.index(found_car)
                                    if car_index > len(self.cars_objects) - 1:
                                        message = "You cannot depart this car. There is a car parked above it."
                                        message_timer = pygame.time.get_ticks()
                                    else:
                                        return text, 'departure'
                        if self.show_license_plate_button.collidepoint(event.pos):
                            self.show_license_plate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]  # Remove last character on backspace
                        else:
                            text += event.unicode  # Add typed character

            if self.is_paused:
                self.pause_menu.draw()
                if self.pause_menu.action == "resume":
                    self.is_paused = False
                    self.pause_menu.action = None  # Reset the action
                elif self.pause_menu.action == "main_menu":
                    # Handle returning to the main menu
                    self.pause_menu.action = None  # Reset the action
                    # Implement main menu logic here if needed
                self.draw_pause_play_button()
            else:
                # Draw background and text input box
                self.screen.fill((255, 255, 255))  # White background for the input screen

                # Display the message if there is one
                if message and pygame.time.get_ticks() - message_timer < 2000:  # Display message for 2 seconds
                    message_surface = font_message.render(message, True, (255, 0, 0))
                    message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, 50))
                    self.screen.blit(message_surface, message_rect)
                else:
                    message = None

                # Display the message "Please enter your plate number" centered above the input box
                prompt_message = font_message.render("Please enter your plate number", True, (0, 0, 0))
                prompt_message_x = input_box.x + (input_box.width - prompt_message.get_width()) // 2  # Center horizontally
                self.screen.blit(prompt_message, (prompt_message_x, input_box.y - 40))  # Position the message above the input box

                # Display the message "Cars parked: n" below the input box, or "Parking full" if max cars reached
                arrived_message = font_message.render(f"Cars parked: {arrived_count}" if arrived_count < 10 else "Parking full", True, (0, 0, 0))
                self.screen.blit(arrived_message, (input_box.x + (input_box.width - arrived_message.get_width()) // 2, input_box.y + input_box.height + 10))

                # Display arrival and departure counts below the "Cars parked" message
                arrival_departure_message = font_message.render(f"Arrivals: {self.total_arrivals}  Departures: {self.departed_count}", True, (0, 0, 0))
                self.screen.blit(arrival_departure_message, (input_box.x + (input_box.width - arrival_departure_message.get_width()) // 2, input_box.y + input_box.height + 40))

                # Draw the input box and the text inside
                pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)  # Input box outline
                txt_surface = font.render(text, True, (0, 0, 0))
                self.screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

                # Blinking cursor
                cursor_timer += clock.get_time()
                if cursor_timer >= 500:
                    cursor_visible = not cursor_visible
                    cursor_timer = 0
                if cursor_visible:
                    cursor_rect = pygame.Rect(input_box.x + 10 + txt_surface.get_width(), input_box.y + 10, 2, font.get_height())
                    pygame.draw.rect(self.screen, (0, 0, 0), cursor_rect)

                # Draw the "Arrival" button
                if arrived_count < 10:
                    if button_rect_arrival.collidepoint(pygame.mouse.get_pos()):  # Hover effect
                        pygame.draw.rect(self.screen, button_hover_color, button_rect_arrival)
                    else:
                        pygame.draw.rect(self.screen, button_color, button_rect_arrival)
                else:
                    pygame.draw.rect(self.screen, arrival_button_disabled_color, button_rect_arrival)

                button_text_arrival = font_message.render("Arrival", True, (255, 255, 255))
                self.screen.blit(button_text_arrival, (button_rect_arrival.x + (button_rect_arrival.width - button_text_arrival.get_width()) // 2, 
                                                button_rect_arrival.y + (button_rect_arrival.height - button_text_arrival.get_height()) // 2))

                # Draw the "Departure" button
                if button_rect_departure.collidepoint(pygame.mouse.get_pos()):  # Hover effect
                    pygame.draw.rect(self.screen, departure_button_hover_color, button_rect_departure)
                else:
                    pygame.draw.rect(self.screen, departure_button_color, button_rect_departure)

                button_text_departure = font_message.render("Departure", True, (255, 255, 255))
                self.screen.blit(button_text_departure, (button_rect_departure.x + (button_rect_departure.width - button_text_departure.get_width()) // 2, 
                                                button_rect_departure.y + (button_rect_departure.height - button_text_departure.get_height()) // 2))

                # Draw the "Show License Plate" button
                pygame.draw.rect(self.screen, (0, 0, 255), self.show_license_plate_button)
                show_license_plate_text = font_message.render("Show License Plate", True, (255, 255, 255))
                self.screen.blit(show_license_plate_text, (self.show_license_plate_button.x + (self.show_license_plate_button.width - show_license_plate_text.get_width()) // 2, 
                                                        self.show_license_plate_button.y + (self.show_license_plate_button.height - show_license_plate_text.get_height()) // 2))

                self.draw_pause_play_button()

            pygame.display.flip()
            clock.tick(30)

    def run(self):
        font = pygame.font.SysFont(None, 48)  # Define the font here
        self.reuse_car = None  # Initialize reuse_car to None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Toggle pause menu with 'P' key
                        self.is_paused = not self.is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_paused:
                        self.pause_menu.handle_click(event.pos)
                    elif self.pause_button.collidepoint(event.pos):
                        self.is_paused = not self.is_paused

            if self.is_paused:
                self.pause_menu.draw()
                if self.pause_menu.action == "resume":
                    self.is_paused = False
                    self.pause_menu.action = None  # Reset the action
                elif self.pause_menu.action == "main_menu":
                    # Handle returning to the main menu
                    self.pause_menu.action = None  # Reset the action
                    # Implement main menu logic here if needed
                self.draw_pause_play_button()
            else:
                self.draw_pause_play_button()

                # Step 1: Get plate number for the current car using the "Arrival" button
                plate_number, action = self.get_plate_number(len(self.cars_objects))

                if action == 'arrival':
                    # Check if the car with the plate number already exists
                    existing_car = None
                    for car in self.cars_objects:
                        if car.plate_number.strip().upper() == plate_number.strip().upper():
                            existing_car = car
                            break

                    if existing_car:
                        # Display a message if the car is already parked
                        self.get_plate_number(len(self.cars_objects), message="Car is already parked.")
                        continue  # Proceed to another input
                    else:
                        # Increment arrival counts correctly
                        self.total_arrivals += 1  # Increment total arrivals
                        self.arrived_count += 1  # Increment the arrived count directly

                        # Step 2: Animate the car
                        self.current_car += 1  # Move to the next car
                        if self.current_car < len(self.car_positions):
                            x, y, target_y = self.car_positions[self.current_car]
                            self.waiting_for_input = False  # Allow the car to start moving

                            if self.reuse_car:
                                # Reuse the departing car
                                car = self.reuse_car
                                car.rect.topleft = (x, y)
                                car.target_y = target_y
                                car.is_departing = False
                                self.reuse_car = None  # Reset reuse_car
                            else:
                                # Create a new car object and add it to the sprite group
                                car = Car(x, y, self.car_images[self.current_car % len(self.car_images)], self.scale_width, self.scale_height, target_y, plate_number, self.car_images[self.current_car % len(self.car_images)])
                                self.all_sprites.add(car)
                                self.cars_objects.append(car)
                                self.parked_cars.append(plate_number)

                        else:
                            print("Error: current_car index out of range")
                            self.current_car = len(self.car_positions) - 1  # Reset to the last valid index

                elif action == 'departure':
                    # Check if the user selected the bottom-most car (last car in the list)
                    if self.cars_objects:
                        bottom_car = self.cars_objects[0]  # Last parked car (bottom-most)
                        top_car = self.cars_objects[-1]  # First parked car (top-most)

                        if bottom_car and bottom_car.plate_number.strip().upper() == plate_number.strip().upper():
                            # If the bottom-most car is selected, make all cars depart
                            self.depart_all_cars()
                        elif top_car.plate_number.strip().upper() == plate_number.strip().upper():
                            # If the top-most car is selected, show a message that the first car should depart first
                            self.get_plate_number(len(self.cars_objects), is_departure=True, message="The first car should depart first.")
                        else:
                            # Handle other cases (not top or bottom-most cars)
                            self.get_plate_number(len(self.cars_objects), is_departure=True, message="Please pick the first or last car.")

                # Step 2: Animate the car if there are still cars
                while not self.waiting_for_input:
                    self.animation_in_progress = True  # Animation in progress
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    # Update car position for the car that is currently moving
                    if self.current_car >= 0 and self.current_car < len(self.cars_objects):
                        self.cars_objects[self.current_car].update()

                        # If the car has reached its target position, wait for 1 second before allowing input
                        if self.cars_objects[self.current_car].rect.y == self.cars_objects[self.current_car].target_y:
                            # Wait for 1 second before showing the next input box
                            pygame.time.delay(1000)  # 1000 milliseconds = 1 second
                            self.waiting_for_input = True

                    # Update car position for departing cars
                    for car in self.cars_objects:
                        if car.is_departing:
                            car.update()
                            if car.rect.y <= -car.rect.height:
                                self.all_sprites.remove(car)
                                self.cars_objects.remove(car)
                                self.parked_cars.remove(car.plate_number)
                                pygame.time.delay(500)  # 500 milliseconds = 0.5 seconds delay after car leaves
                                self.departed_count += 1  # Update the departed count after the car leaves
                                self.current_car -= 1  # Decrement the current car index
                                self.waiting_for_input = True  # Allow input after car departs

                    # Draw background and sprites
                    self.screen.blit(self.bg, (0, 0))
                    self.all_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.clock.tick(60)

                self.animation_in_progress = False

                pygame.display.flip()
                self.clock.tick(60)

    def show_license_plate(self):
        font = pygame.font.SysFont(None, 36)
        back_button_font = pygame.font.SysFont(None, 48)
        show_license_plate_active = True

        while show_license_plate_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        show_license_plate_active = False

            self.screen.fill((255, 255, 255))  # Clear the screen with a white background

            # Draw the back button
            back_button_text = back_button_font.render("<", True, (0, 0, 0))  # Black font color
            self.screen.blit(back_button_text, (self.back_button.x + 10, self.back_button.y + 5))

            # Display the parked cars
            y_offset = 50
            for i, car in enumerate(self.cars_objects, start=1):
                text_surface = font.render(f"Car number {i}: {car.plate_number}", True, (0, 0, 0))
                self.screen.blit(text_surface, (50, y_offset))
                car_image = pygame.image.load(car.image_path)
                car_image = pygame.transform.scale(car_image, (self.scale_width, self.scale_height))
                self.screen.blit(car_image, (400, y_offset - 10))
                y_offset += 60

            pygame.display.flip()

    def draw_pause_play_button(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_button)
        if self.is_paused:
            play_button_points = [
                (self.pause_button.x + 10, self.pause_button.y + 5),
                (self.pause_button.x + 10, self.pause_button.y + 35),
                (self.pause_button.x + 30, self.pause_button.y + 20)
            ]
            pygame.draw.polygon(self.screen, (0, 0, 0), play_button_points)
        else:
            bold_font = pygame.font.SysFont(None, 48, bold=True)  # Define bold font
            pause_text = bold_font.render("||", True, (0, 0, 0), (255, 255, 255))  # Bold text with background color
            self.screen.blit(pause_text, (self.pause_button.x + 10, self.pause_button.y + 5))

    def depart_all_cars(self):
        self.waiting_for_input = False
        departing_car = None

        for car in self.cars_objects:
            if car.plate_number == self.selected_plate_number:
                departing_car = car
            else:
                car.is_departing = True  # Mark all cars as departing except the selected one

        self.animation_in_progress = True  # Trigger animation for all cars

    def depart_all_cars(self):
        # Distance between cars (15 pixels)
        distance_between_cars = 10
        max_y_position = self.screen.get_height()  # This is the target position (off the screen)

        # Set initial positions of the cars based on their index, maintaining a 15-pixel gap
        for i, car in enumerate(self.cars_objects):
            car.target_y = max_y_position - (i + 1) * (car.rect.height + distance_between_cars)
            car.rect.y = max_y_position - (i + 1) * (car.rect.height + distance_between_cars)  # Start them at their target position

        self.animation_in_progress = True  # Trigger animation for departure

        # Move all cars upwards (departure animation)
        departing_car = self.cars_objects[0]  # Define departing_car as the first car in the list
        while self.animation_in_progress:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update the position of all cars (move them upwards to simulate departure)
            for car in self.cars_objects:
                if car.rect.y > -car.rect.height:  # If the car is not off-screen
                    car.rect.y -= car.speed  # Move the car upwards (departure)

            # If the first car has completely moved off-screen, stop the animation
            if all(car.rect.y <= -car.rect.height for car in self.cars_objects):
                self.animation_in_progress = False
                self.cars_objects.remove(departing_car)  # Remove the departing car from the list
                self.parked_cars.remove(departing_car.plate_number)  # Remove from parked cars list

            # Redraw screen and update display
            self.screen.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        # Now animate all cars coming back one by one while maintaining the 15-pixel gap
        self.animation_in_progress = True

        # Reset cars' departure state and prepare them for the return animation
        for i, car in enumerate(self.cars_objects):
            car.is_departing = False  # Reset the departing flag
            car.rect.y = -car.rect.height  # Start all cars from above the screen
            car.target_y = max_y_position - (i + 1) * (car.rect.height + distance_between_cars)  # Calculate target_y with 15-pixel gap

        # Animate the cars coming back into position, maintaining the 15-pixel distance
        car_index = 0  # Start with the first car
        while self.animation_in_progress:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Start moving the cars one by one, waiting for the previous car to be at the correct position
            if car_index < len(self.cars_objects):
                current_car = self.cars_objects[car_index]

                # Move the current car down to its target position, checking the gap
                if current_car.rect.y < current_car.target_y:
                    current_car.rect.y += current_car.speed  # Move the car down to its target position
                elif current_car.rect.y >= current_car.target_y:
                    # Once the current car reaches its target position, move to the next car
                    car_index += 1

            # If all cars have returned to their positions, stop the animation
            if all(car.rect.y >= car.target_y for car in self.cars_objects):
                self.animation_in_progress = False

            # Redraw the screen and update the display
            self.screen.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        self.departed_count += 1

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, image, scale_width, scale_height, target_y, plate_number=None, image_path=None):
        super().__init__()
        self.image = pygame.image.load(image)  # Load specific car image
        self.image = pygame.transform.scale(self.image, (scale_width, scale_height))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5  # Reduce speed to make the departure animation slower
        self.target_y = target_y  # Target position for car to move to
        self.plate_number = plate_number  # Store the plate number
        self.is_departing = False  # Flag to indicate if the car is departing
        self.image_path = image_path  # Store the image path

    def update(self):
        if not self.is_departing:
            # Move the car toward its target (downwards)
            if self.rect.y < self.target_y:  # Move down
                self.rect.y += self.speed
            elif self.rect.y > self.target_y:  # Move up (in case of slight overshooting)
                self.rect.y -= self.speed
        else:
            # Move the car upward for departure animation
            if self.rect.y > -self.rect.height:  # If the car has not moved out of the screen yet
                self.rect.y -= self.speed  # Move the car up
            else:
                self.kill()  # Remove the car from the sprite group once it goes off the screen

if __name__ == '__main__':
    ParkingLot().run()