import pygame
import numpy as np
import time

class WaveSimulation:
    def __init__(self):
        # Define simulation parameters
        self.WIDTH, self.HEIGHT = 800, 700
        self.FPS = 60
        self.NUM_POINTS_X = 50
        self.NUM_POINTS_Y = 50
        self.SPACING_X = self.WIDTH // self.NUM_POINTS_X
        self.SPACING_Y = self.HEIGHT // self.NUM_POINTS_Y
        self.DAMPING = 0.9999999999  # Increase damping
        self.WAVE_SPEED = 0.0091  # Increase wave speed
        self.WAVE_HEIGHT_THRESHOLD = 0.01

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # Create grid of points
        self.points = np.zeros((self.NUM_POINTS_X, self.NUM_POINTS_Y, 2))
        self.velocities = np.zeros((self.NUM_POINTS_X, self.NUM_POINTS_Y, 2))
        self.wave_heights = np.zeros((self.NUM_POINTS_X, self.NUM_POINTS_Y))

        # Add an initial disturbance to the wave
        self.wave_heights[self.NUM_POINTS_X // 2, self.NUM_POINTS_Y // 2] = 1

    # Rest of the code remains the same...

    def run(self):
        # Main loop
        running = True
        while True:
            self.screen.fill((0, 0, 0))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = not running
                    elif event.key == pygame.K_r:
                        self.wave_heights = np.zeros((self.NUM_POINTS_X, self.NUM_POINTS_Y))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    i = x // self.SPACING_X
                    j = y // self.SPACING_Y
                    self.wave_heights[i, j] = 50  # Increase the disturbance created by the mouse click

            # Update wave simulation
            if running:
                for i in range(1, self.NUM_POINTS_X - 1):
                    for j in range(1, self.NUM_POINTS_Y - 1):
                        self.velocities[i, j, 0] += (self.wave_heights[i + 1, j] + self.wave_heights[i - 1, j] +
                                                    self.wave_heights[i, j + 1] + self.wave_heights[i, j - 1] -
                                                    4 * self.wave_heights[i, j]) * self.WAVE_SPEED
                        self.velocities[i, j, 0] *= self.DAMPING
                        self.velocities[i, j, 1] += self.velocities[i, j, 0]
                        self.wave_heights[i, j] += self.velocities[i, j, 1]
                        self.wave_heights[i, j] *= self.DAMPING

                        # Add a periodic disturbance to the wave height
                        self.wave_heights[i, j] += np.sin(time.time())

                # Set wave heights and velocities at the edges of the grid to zero
                self.wave_heights[0, :] = -self.wave_heights[1, :]
                self.wave_heights[-1, :] = -self.wave_heights[-2, :]
                self.wave_heights[:, 0] = -self.wave_heights[:, 1]
                self.wave_heights[:, -1] = -self.wave_heights[:, -2]
                self.velocities[0, :, :] = -self.velocities[1, :, :]
                self.velocities[-1, :, :] = -self.velocities[-2, :, :]
                self.velocities[:, 0, :] = -self.velocities[:, 1, :]
                self.velocities[:, -1, :] = -self.velocities[:, -2, :]

                # Draw wave
                for i in range(self.NUM_POINTS_X):
                    for j in range(self.NUM_POINTS_Y):
                        x = i * self.SPACING_X
                        y = j * self.SPACING_Y
                        color = abs(self.wave_heights[i, j])
                        max_value = np.max(np.abs(self.wave_heights))
                        if max_value != 0:                        
                            color /= max_value
                        else:
                            color = 0
                        color = int(color * 255)
                        pygame.draw.rect(self.screen, (color, color, color), (x, y, self.SPACING_X, self.SPACING_Y))

                pygame.display.flip()
                self.clock.tick(self.FPS)

# Create an instance of WaveSimulation and run the simulation
wave_simulation = WaveSimulation()
wave_simulation.run()