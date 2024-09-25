import pygame
import random
from pygame.math import Vector2
from ball import Ball
from physics_engine import PhysicsEngine
from ui_manager import UIManager
from logger import main_logger  # Import the logger

# Initialize Pygame
pygame.init()

# Window Setup
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Simulation")

# Colors
BACKGROUND_COLOR = (30, 30, 30)

# Clock for FPS
CLOCK = pygame.time.Clock()
FPS = 60

def main():
    try:
        # Initialize components
        balls = [
            Ball(
                position=Vector2(
                    random.randint(50, WIDTH - 50),
                    random.randint(50, HEIGHT - 50)
                ),
                radius=random.randint(10, 30),
                color=(
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255),
                ),
                velocity=Vector2(
                    random.uniform(-5, 5),
                    random.uniform(-5, 5)
                ),
            )
            for _ in range(5)
        ]

        physics = PhysicsEngine(gravity=0.5)
        ui = UIManager()

        running = True
        paused = False

        while running:
            CLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                ui.handle_event(event, balls, physics)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                paused = not paused
                main_logger.info(f"Paused: {paused}")
            if keys[pygame.K_r]:
                try:
                    # Reset to initial state
                    balls.clear()
                    for _ in range(5):
                        balls.append(
                            Ball(
                                position=Vector2(
                                    random.randint(50, WIDTH - 50),
                                    random.randint(50, HEIGHT - 50)
                                ),
                                radius=random.randint(10, 30),
                                color=(
                                    random.randint(50, 255),
                                    random.randint(50, 255),
                                    random.randint(50, 255),
                                ),
                                velocity=Vector2(
                                    random.uniform(-5, 5),
                                    random.uniform(-5, 5)
                                ),
                            )
                        )
                    physics.gravity = 0.5
                    main_logger.info("Simulation reset to initial state.")
                except Exception as e:
                    main_logger.error(f"Error during reset: {e}", exc_info=True)

            # Update gravity
            ui.update_gravity(physics, 0.01)

            if not paused:
                physics.update(balls, WIDTH, HEIGHT)

            # Drawing
            WINDOW.fill(BACKGROUND_COLOR)
            for ball in balls:
                try:
                    ball.draw(WINDOW)
                except Exception as e:
                    main_logger.error(f"Error drawing ball: {e}", exc_info=True)

            # Display gravity
            try:
                font = pygame.font.SysFont(None, 24)
                gravity_text = font.render(f"Gravity: {physics.gravity:.2f}", True, (255, 255, 255))
                WINDOW.blit(gravity_text, (10, 10))
            except Exception as e:
                main_logger.error(f"Error rendering gravity text: {e}", exc_info=True)

            try:
                pygame.display.flip()
            except Exception as e:
                main_logger.error(f"Error updating display: {e}", exc_info=True)

    except Exception as e:
        main_logger.critical(f"Unhandled exception: {e}", exc_info=True)
    finally:
        pygame.quit()
        main_logger.info("Pygame terminated gracefully.")

if __name__ == "__main__":
    main()