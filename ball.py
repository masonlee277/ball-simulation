import pygame
from pygame.math import Vector2
from logger import main_logger  # Import the logger

class Ball:
    def __init__(self, position, radius, color, velocity):
        try:
            self.position = Vector2(position)
            self.radius = radius
            self.color = color
            self.velocity = Vector2(velocity)
            self.is_dragging = False
        except Exception as e:
            main_logger.error(f"Error initializing Ball: {e}", exc_info=True)
            raise

    def draw(self, surface):
        try:
            pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        except Exception as e:
            main_logger.error(f"Error drawing ball at position {self.position}: {e}", exc_info=True)
            raise

    def update_position(self):
        try:
            self.position += self.velocity
        except Exception as e:
            main_logger.error(f"Error updating position for ball: {e}", exc_info=True)
            raise

    def apply_gravity(self, gravity):
        try:
            self.velocity.y += gravity
        except Exception as e:
            main_logger.error(f"Error applying gravity to ball: {e}", exc_info=True)
            raise

    def check_boundary_collision(self, width, height, damping=0.9):
        try:
            # Left or Right
            if self.position.x - self.radius <= 0:
                self.position.x = self.radius
                self.velocity.x *= -damping
            elif self.position.x + self.radius >= width:
                self.position.x = width - self.radius
                self.velocity.x *= -damping

            # Top or Bottom
            if self.position.y - self.radius <= 0:
                self.position.y = self.radius
                self.velocity.y *= -damping
            elif self.position.y + self.radius >= height:
                self.position.y = height - self.radius
                self.velocity.y *= -damping
        except Exception as e:
            main_logger.error(f"Error checking boundary collision for ball at position {self.position}: {e}", exc_info=True)
            raise

    def is_clicked(self, mouse_pos):
        try:
            return self.position.distance_to(Vector2(mouse_pos)) <= self.radius
        except Exception as e:
            main_logger.error(f"Error in is_clicked method: {e}", exc_info=True)
            raise