import pygame
import pygame_gui
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Pendulum parameters
length = 200  # length of the pendulum arm (pixels)
initial_angle = math.pi / 4  # initial angle in radians
gravity = 1.0  # acceleration due to gravity (adjusted for pixels)
mass = 10  # mass of the pendulum bob (kg)
damping = 0.05  # damping coefficient

# Create a UI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Simulation parameters
fps = 60
dt = 40 / fps

# Create a label for the mass slider
mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (200, 20)),
                                         text='Mass',
                                         manager=manager)

# Create a slider to control the mass of the pendulum
mass_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 40), (200, 20)),
                                                     start_value=mass,
                                                     value_range=(1, 50),
                                                     manager=manager)

# Create a start/stop button
start_stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 70), (150, 50)),
                                                 text='Start/Stop',
                                                 manager=manager)

# Create a restart button
restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((170, 70), (150, 50)),
                                              text='Restart',
                                              manager=manager)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation")
clock = pygame.time.Clock()

# Function to calculate the position of the pendulum bob
def calculate_position(angle):
    x = WIDTH // 2 + length * math.sin(angle)
    y = HEIGHT // 2 + length * math.cos(angle)
    return x, y

# Initialize a list to store the positions of the pendulum bob
trajectory = []

# Function to draw the pendulum
def draw_pendulum(angle):
    x, y = calculate_position(angle)
    pygame.draw.line(screen, RED, (WIDTH // 2, HEIGHT // 2), (x, y), 2)
    pygame.draw.circle(screen, BLUE, (x, y), 20)
    trajectory.append((x, y))  # Append the current position to the trajectory

    # Draw the trajectory
    if len(trajectory) > 1:
        pygame.draw.lines(screen, WHITE, False, trajectory, 1)

mass  # Make mass a global variable

angle = initial_angle
angular_velocity = 0

running = True
simulation_running = False  # New variable to control the pendulum simulation
while running:
    time_delta = clock.tick(fps)/1000.0
    screen.fill(LIGHT_BLUE)
        
    mass = mass_slider.get_current_value()  # Update the value of mass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_stop_button:
                    simulation_running = not simulation_running  # Toggle the simulation state
                elif event.ui_element == restart_button:  # Check if the restart button was pressed
                    angle = initial_angle  # Reset the angle
                    angular_velocity = 0  # Reset the angular velocity
                    simulation_running = False  # Stop the simulation
                    trajectory.clear()  # Clear the trajectory

        manager.process_events(event)

    if simulation_running:  # Only update the pendulum if the simulation is running
        # Calculate acceleration using equation of motion
        acceleration = -gravity / length * math.sin(angle) - damping * angular_velocity / mass

        # Update velocity and angle using Euler's method
        angular_velocity += acceleration * dt
        angle += angular_velocity * dt

    # Draw the pendulum
    draw_pendulum(angle)

    # Update the UI
    manager.update(time_delta)

    # Draw the UI
    manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()
