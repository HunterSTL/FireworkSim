import random
import pygame
import math

HEIGHT = 1000
WIDTH = 1000
PI = 3.1415926
GRAVITY = 0.1

class Firework:
    def __init__(self, x, target_y, speed, color, color_complexity, particle_count):
        self.x = x
        self.y = 0
        self.target_y = HEIGHT - target_y
        self.speed = speed
        self.color = color
        self.color_complexity = color_complexity
        self.particle_count = particle_count
        self.has_exploded = False
        self.particles = []

    def update(self):
        if not self.has_exploded:
            self.y += self.speed
            self.speed -= GRAVITY
            if self.y >= self.target_y:
                self.explode()
    
    def draw(self, surface):
        dark_orange = (150, 50, 0)
        pygame.draw.circle(surface, dark_orange, (self.x, HEIGHT - int(self.y)), 3)

    def explode(self):
        self.has_exploded = True

        for _ in range(self.particle_count):
            angle = random.uniform(0, 2 * PI)
            speed = random.uniform(0.1, 10)
            lifetime = random.randint(50, 100)
            max_lifetime = lifetime
            self.particles.append(Particle(self.x, self.y, speed, angle, max_lifetime, lifetime, self.color, self.speed))
        
        if self.color_complexity > 1:
            self.color = random_vibrant_color()
            for _ in range(self.particle_count // 2):
                angle = random.uniform(0, 2 * PI)
                speed = random.uniform(0.1, 9)
                lifetime = random.randint(50, 100)
                max_lifetime = lifetime
                self.particles.append(Particle(self.x, self.y, speed, angle, max_lifetime, lifetime, self.color, self.speed))
        
        if self.color_complexity > 2:
            self.color = random_vibrant_color()
            for _ in range(self.particle_count // 3):
                angle = random.uniform(0, 2 * PI)
                speed = random.uniform(0.1, 8)
                lifetime = random.randint(50, 100)
                max_lifetime = lifetime
                self.particles.append(Particle(self.x, self.y, speed, angle, max_lifetime, lifetime, self.color, self.speed))

class Particle:
    def __init__(self, x, y, explosion_speed, angle, max_lifetime, lifetime, color, inherited_speed):
        self.x = x
        self.y = y
        self.explosion_speed = explosion_speed
        self.angle = angle
        self.max_lifetime = max_lifetime
        self.lifetime = lifetime
        self.color = color
        self.vertical_speed = inherited_speed

    def update(self):
        horizontal_component = self.explosion_speed * math.cos(self.angle)
        vertical_component = self.explosion_speed * math.sin(self.angle)

        self.x += horizontal_component
        self.y += vertical_component + self.vertical_speed

        self.vertical_speed -= GRAVITY

        self.explosion_speed *= 0.98
        self.lifetime -= 1

        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.lifetime = 0

    def draw(self, surface):
        if self.lifetime > 0:
            ratio = self.lifetime / self.max_lifetime
            red = self.color[0] * ratio
            green = self.color[1] * ratio
            blue = self.color[2] * ratio
            particle_color = (red, green, blue)
            pygame.draw.circle(surface, particle_color, (int(self.x), HEIGHT - int(self.y)), 2)

def random_vibrant_color():
    values = [
        random.randint(200, 255),
        random.randint(100, 200),
        random.randint(50, 150)
    ]
    random.shuffle(values)
    return tuple(values)

def main():
    fireworks = []

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target_height = HEIGHT - mouse_y
                initial_speed = math.sqrt(2 * GRAVITY * target_height)
                color = random_vibrant_color()
                color_complexity = random.randint(1, 3)
                particle_count = random.randint(50, 400)
                fireworks.append(Firework(mouse_x, mouse_y, initial_speed, color, color_complexity, particle_count))

        for firework in fireworks:
            firework.update()
            if firework.has_exploded:
                for particle in firework.particles:
                    particle.update()
                    particle.draw(screen)
            else:
                firework.draw(screen)

        fireworks = [f for f in fireworks if not (f.has_exploded and all(p.lifetime <= 0 for p in f.particles))]

        pygame.display.flip()
        clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

if __name__ == "__main__":
    main()