import pygame
import pygame_gui
import runpy

# Initialize pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Physics Simulation Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

# Create GUI manager
gui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to handle button clicks
def handle_button_click(button_text):
    if button_text == 'simulate spring':
        print("Simulating spring...")
        # Run the spring.py script
        runpy.run_path('./spring.py')
    elif button_text == 'simulate pendulum':
        print("Simulating pendulum...")
        # Run the pendulum.py script
        runpy.run_path('./pendulum.py')
    elif button_text == 'simulate double pendulum':
        print("Simulating double pendulum...")
        # Run the double_pendulum.py script
        runpy.run_path('./double_pendulum.py')
    elif button_text == 'simulate wave':
        print("Simulating wave...")
        # Run the wave.py script
        runpy.run_path('./wave_simulate.py')

# Create buttons
button_positions = [(300, 100), (300, 200), (300, 300), (300, 400)]
button_texts = ["Simulate Spring", "Simulate Pendulum", "Simulate Double Pendulum", "Simulate Wave"]
button_events = ['simulate_spring', 'simulate_pendulum', 'simulate_double_pendulum', 'simulate_wave']
buttons = []
for i in range(len(button_positions)):
    button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(button_positions[i], (200, 50)),
                                          text=button_texts[i],
                                          manager=gui_manager)
    buttons.append(button)

# Main loop
clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                handle_button_click(event.ui_element.text.lower())

        gui_manager.process_events(event)

    gui_manager.update(time_delta)
    screen.fill(LIGHT_BLUE)
    gui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
