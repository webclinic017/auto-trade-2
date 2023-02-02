import sys
import numpy as np
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 300))

r = np.zeros((3, 2), dtype=float)
v = np.zeros((3, 2), dtype=float)
a = np.zeros((3, 2), dtype=float)
m = np.array([1, 1, 1], dtype=float)

r[0] = [200, 150]
r[1] = [100, 100]
r[2] = [300, 200]

clock = pygame.time.Clock()

while True:
    dt = clock.tick(30) / 1000.0

    for i in range(3):
        for j in range(3):
            if i == j:
                continue

            dr = r[i] - r[j]
            a[i] += -m[j] * dr / np.linalg.norm(dr)**3

    v += a * dt
    r += v * dt

    screen.fill((255, 255, 255))

    for i in range(3):
        pygame.draw.circle(screen, (255, 0, 0), (int(r[i, 0]), int(r[i, 1])), 5)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
