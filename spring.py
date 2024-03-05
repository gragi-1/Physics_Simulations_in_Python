import pygame
import pygame_gui

# Inicializar pygame
pygame.init()

# Definir colores
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
DARK_RED = (139, 0, 0)

width, height = 800, 700 # Define the screen size
initial_displacement = 150  # Displacement from the center
gravity = 0.5 # Acceleration due to gravity
damping = 0.001  # Damping factor

def draw_spring(start, end, num_coils, thickness):
    """
    Dibuja un muelle entre dos puntos.

    Args:
        start (tuple): punto de inicio del muelle.
        end (tuple): punto final del muelle.
        num_coils (int): número de espirales en el muelle.
        thickness (int): grosor de las líneas del muelle.
    """
    x1, y1 = start
    x2, y2 = end
    coil_length = abs(y2 - y1) / num_coils
    coil_width = 20  # width of each coil

    points = []
    for i in range(num_coils * 2 + 1):
        x = x1 + ((i % 2) * coil_width) - (coil_width / 2) if i % 2 == 0 else x1 + ((i % 2) * coil_width) + (coil_width / 2)
        y = y1 + (i // 2) * coil_length
        points.append((x, y))

    pygame.draw.lines(screen, BLACK, False, points, thickness)

# Define a class for the mass
class Mass(pygame.sprite.Sprite):
    def __init__(self, x, y, mass):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(DARK_RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.mass = mass
        self.velocity = 0

    # Function to apply a force to the mass
    def apply_force(self, force):
        acceleration = force / self.mass  # Calculate the acceleration based on the force
        self.velocity += acceleration     # Update the velocity based on the acceleration
        self.velocity *= (1 - damping)    # Apply damping to the velocity to simulate friction
        self.rect.y += int(self.velocity) # Update the position of the mass based on the velocity

# Function to reset the simulation
def reset_simulation():
    masa.rect.y = height // 2 + initial_displacement
    masa.velocity = 0

# Inicialize the screen and set the caption
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulación de Muelle')
screen.fill(LIGHT_BLUE)  # Cambiar el color de fondo

# Inicialize the UI manager
manager = pygame_gui.UIManager((width, height))

# Inicialize the mass and spring
mass_value = 20
masa = Mass(width // 2, height // 2 + initial_displacement, mass_value)

# Flag to check if the simulation is running
simulation_started = False

# Create buttons and sliders for the UI
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                             text='Start',
                                             manager=manager)
reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 10), (100, 50)),
                                             text='Reset',
                                             manager=manager)

# Labels for the sliders
mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 70), (200, 20)),
                                         text='Masa: ' + str(mass_value),
                                         manager=manager)
spring_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 110), (200, 20)),
                                           text='Constante del Resorte',
                                           manager=manager)
gravity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 150), (200, 20)),
                                            text='Gravedad',
                                            manager=manager)

# Sliders to adjust the mass, spring constant, and gravity
mass_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 90), (200, 20)),
                                                     start_value=mass_value,
                                                     value_range=(1, 50),
                                                     manager=manager)
spring_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 130), (200, 20)),
                                                       start_value=0.5,  # Valor inicial de la constante del resorte
                                                       value_range=(0.1, 1.0),  # Rango de valores ajustables
                                                       manager=manager)
gravity_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 170), (200, 20)),
                                                        start_value=0.5,  # Valor inicial de la gravedad
                                                        value_range=(0.1, 1.0),  # Rango de valores ajustables
                                                        manager=manager)

# Main loop to run the simulation
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    simulation_started = not simulation_started
                elif event.ui_element == reset_button:
                    reset_simulation()
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == mass_slider:
                    mass_value = int(mass_slider.get_current_value())
                    mass_label.set_text('Masa: ' + str(mass_value) + ' kg')
        manager.process_events(event)

    manager.update(time_delta)

    screen.fill(LIGHT_BLUE)
    
    # If the simulation is running, calculate the spring force and apply it to the mass
    if simulation_started:
        # Calculate the displacement of the mass from the center
        displacement = masa.rect.y - (height // 2 + initial_displacement)
        spring_constant = spring_slider.get_current_value()  # Obtain the current value of the spring constant
        spring_force = -spring_constant * displacement

        # Apply the force of gravity to the mass
        gravity_force = masa.mass * gravity_slider.get_current_value()  # Obtaining the current value of gravity

        # Apply the forces to the mass
        total_force = spring_force + gravity_force
        masa.apply_force(total_force)

    # Draw the spring between the mass and the center
    draw_spring((width // 2, height // 2), (width // 2, masa.rect.y), 10, 4)

    # Draw the mass
    screen.blit(masa.image, masa.rect)

    # Draw the UI elements on the screen
    manager.draw_ui(screen)

    pygame.display.flip()

