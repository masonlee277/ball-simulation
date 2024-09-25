from pygame.math import Vector2
from ball import Ball
from logger import main_logger  # Import the logger

class PhysicsEngine:
    def __init__(self, gravity=0.5):
        self.gravity = gravity

    def update(self, balls, width, height):
        try:
            for ball in balls:
                ball.apply_gravity(self.gravity)
                ball.update_position()
                ball.check_boundary_collision(width, height)
            # Optional: Handle inter-ball collisions here
        except Exception as e:
            main_logger.error(f"Error during physics update: {e}", exc_info=True)
            raise