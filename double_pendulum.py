import pygame
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
PENDULUM_LENGTH = 150
MASS_RADIUS = 10
GRAVITY = 9.81
TIME_STEP = 0.1

# Pendulum class
class Pendulum:
    def __init__(self, angle, angular_velocity, length, mass):
        self.angle = angle                       # Angle of the pendulum
        self.angular_velocity = angular_velocity # Angular velocity
        self.length = length                     # Length of the pendulum arm
        self.mass = mass                         # Mass of the pendulum bob
        self.positions = []                      # List to store the positions of the pendulum bob

    # Function to normalize the angle to be between -pi and pi
    @staticmethod
    def normalize_angle(angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    # Function to update the pendulum position
    def update(self, other_pendulum, origin):
        # Calculate the acceleration at the start of the time step
        a1_accel1, a2_accel1 = self.angular_velocity_derivative(other_pendulum)
        
        # Limit the angular velocities
        self.angular_velocity = max(min(self.angular_velocity, 1e100), -1e100)
        other_pendulum.angular_velocity = max(min(other_pendulum.angular_velocity, 1e100), -1e100)

        # Update the angles using the velocities and accelerations
        self.angle += self.angular_velocity * TIME_STEP + 0.5 * a1_accel1 * TIME_STEP**2
        other_pendulum.angle += other_pendulum.angular_velocity * TIME_STEP + 0.5 * a2_accel1 * TIME_STEP**2

        # Calculate the acceleration at the end of the time step
        a1_accel2, a2_accel2 = self.angular_velocity_derivative(other_pendulum)

        # Update the velocities using the average of the accelerations
        self.angular_velocity += 0.5 * (a1_accel1 + a1_accel2) * TIME_STEP
        other_pendulum.angular_velocity += 0.5 * (a2_accel1 + a2_accel2) * TIME_STEP
        
        # Add the new position to the list of positions
        x = origin[0] + self.length * math.sin(self.angle)
        y = origin[1] + self.length * math.cos(self.angle)
        self.positions.append((x, y))
            
    # Function to calculate the derivative of the angular velocity
    def angular_velocity_derivative(self, other_pendulum):
        G = GRAVITY
        m1 = self.mass
        m2 = other_pendulum.mass
        l1 = self.length
        l2 = other_pendulum.length
        a1 = self.angle
        a2 = other_pendulum.angle
        w1 = self.angular_velocity
        w2 = other_pendulum.angular_velocity

        num1 = -G * (2 * m1 + m2) * math.sin(a1)
        num2 = -m2 * G * math.sin(a1 - 2 * a2)
        num3 = -2 * math.sin(a1 - a2) * m2
        num4 = w2**2 * l2 + w1**2 * l1 * math.cos(a1 - a2)
        den = l1 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))

        w1_deriv = (num1 + num2 + num3 * num4) / den

        num1 = 2 * math.sin(a1 - a2)
        num2 = w1**2 * l1 * (m1 + m2)
        num3 = G * (m1 + m2) * math.cos(a1)
        num4 = w2**2 * l2 * m2 * math.cos(a1 - a2)
        den = l2 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))

        w2_deriv = (num1 * (num2 + num3 + num4)) / den

        return w1_deriv, w2_deriv # Return the derivatives of the angular velocities
    
    # Function to draw the pendulum
    def draw(self, screen, origin):
        x = origin[0] + self.length * math.sin(self.angle)
        y = origin[1] + self.length * math.cos(self.angle)  # Note the plus sign here
        pygame.draw.line(screen, WHITE, origin, (int(x), int(y)), 2)
        pygame.draw.circle(screen, RED, (int(x), int(y)), MASS_RADIUS)
        # Draw the path
        if len(self.positions) > 1:
            pygame.draw.lines(screen, WHITE, False, self.positions)

# Initialize pygame and the screen and clock objects
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Double Pendulum Simulation")

clock = pygame.time.Clock()

pendulum1 = Pendulum(math.pi / 2, 0, PENDULUM_LENGTH, 1.0)
pendulum2 = Pendulum(math.pi / 2, 0, PENDULUM_LENGTH, 2.0)

run_simulation = False

# Slider for controlling mass of the second pendulum
mass_slider_value = 1.0

font = pygame.font.Font(None, 36)
start_stop_button = pygame.Rect(50, 50, 150, 50)
reset_button = pygame.Rect(50, 120, 150, 50)

# Main loop
running = True
while running:
    screen.fill(LIGHT_BLUE) # Change the background color

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_stop_button.collidepoint(event.pos):
                run_simulation = not run_simulation
            elif reset_button.collidepoint(event.pos):
                pendulum1.angle = math.pi / 2
                pendulum1.angular_velocity = 0
                pendulum2.angle = math.pi / 2
                pendulum2.angular_velocity = 0
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1 and start_stop_button.collidepoint(event.pos):
                run_simulation = not run_simulation
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run_simulation = not run_simulation

    # Update the pendulum positions
    if run_simulation:
        pendulum1_origin = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pendulum2_origin = (SCREEN_WIDTH // 2 + pendulum1.length * math.sin(pendulum1.angle),
                            SCREEN_HEIGHT // 2 + pendulum1.length * math.cos(pendulum1.angle))
        pendulum1.update(pendulum2, pendulum1_origin)
        pendulum2.update(pendulum1, pendulum2_origin)

    pendulum1.draw(screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pendulum2.draw(screen, (SCREEN_WIDTH // 2 + pendulum1.length * math.sin(pendulum1.angle),
                                SCREEN_HEIGHT // 2 + pendulum1.length * math.cos(pendulum1.angle)))  # Note the plus sign here

    pygame.draw.rect(screen, WHITE, start_stop_button)
    pygame.draw.rect(screen, WHITE, reset_button)

    # Draw the text for the buttons
    start_stop_text = font.render("Start/Stop", True, BLACK)
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(start_stop_text, (start_stop_button.x + 10, start_stop_button.y + 10))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))

    # Draw the slider
    pygame.draw.rect(screen, WHITE, (250, 50, 200, 20))
    pygame.draw.rect(screen, RED, (250 + int((mass_slider_value - 0.5) * 200), 45, 10, 30))

    # Update slider value based on mouse position
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 250 <= mouse_x <= 450 and 45 <= mouse_y <= 75:
            mass_slider_value = (mouse_x - 250) / 200 + 0.5

    pygame.display.flip()
    clock.tick(30)
