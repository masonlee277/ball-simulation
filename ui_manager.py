import pygame
from pygame.math import Vector2
from ball import Ball
import random
from logger import main_logger  # Import the logger

class UIManager:
    def __init__(self):
        self.dragging_ball = None
        self.offset = Vector2(0, 0)
        self.drag_start_pos = Vector2(0, 0)
        self.mouse_influence_radius = 100  # Radius of mouse influence

    def handle_event(self, event, balls, physics):
        try:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    for ball in reversed(balls):
                        if ball.is_clicked(mouse_pos):
                            self.dragging_ball = ball
                            self.offset = ball.position - mouse_pos
                            self.drag_start_pos = Vector2(event.pos)
                            main_logger.info(f"Started dragging ball at {ball.position}")
                            break
                    else:
                        # Add new ball
                        new_ball = Ball(
                            position=Vector2(mouse_pos),
                            radius=random.randint(10, 30),
                            color=(
                                random.randint(50, 255),
                                random.randint(50, 255),
                                random.randint(50, 255),
                            ),
                            velocity=Vector2(random.uniform(-5, 5), random.uniform(-5, 5)),
                        )
                        balls.append(new_ball)
                        main_logger.info(f"Added new ball at {mouse_pos}")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging_ball:
                    drag_end_pos = Vector2(event.pos)
                    drag_vector = drag_end_pos - self.drag_start_pos
                    velocity_scale = 0.2
                    self.dragging_ball.velocity = drag_vector * velocity_scale
                    main_logger.info(f"Released ball with velocity {self.dragging_ball.velocity}")
                    self.dragging_ball = None
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_ball:
                    self.dragging_ball.position = mouse_pos + self.offset
                else:
                    # Influence nearby balls when not dragging
                    for ball in balls:
                        distance = ball.position.distance_to(mouse_pos)
                        if distance < self.mouse_influence_radius and distance != 0:
                            try:
                                force = (mouse_pos - ball.position).normalize() * (1 - distance / self.mouse_influence_radius) * 0.5
                                ball.velocity += force
                            except Exception as e:
                                main_logger.error(f"Error applying force to ball at {ball.position}: {e}", exc_info=True)
        except Exception as e:
            main_logger.error(f"Error handling event: {e}", exc_info=True)
            raise

    def update_gravity(self, physics, delta):
        try:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                physics.gravity -= delta
                main_logger.info(f"Gravity decreased to {physics.gravity}")
            if keys[pygame.K_DOWN]:
                physics.gravity += delta
                main_logger.info(f"Gravity increased to {physics.gravity}")
            physics.gravity = max(0, min(physics.gravity, 2.0))  # Clamp gravity between 0 and 2
        except Exception as e:
            main_logger.error(f"Error updating gravity: {e}", exc_info=True)
            raise