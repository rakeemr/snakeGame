import sys
import pygame
import pygame.constants
from pygame.locals import *


# Establecemos el LARGO y ALTO de cada celda.
height = 32
width = 32

# Establecemos el margen entre las celdas.
margin = 3

# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
MORADO = (77, 0, 192)
ROJO = (245, 8, 40)


def load_image(fileName, transparent=None):
    try:
        image = pygame.image.load(fileName)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image



def displayGraphics(matrix):
    pygame.init()
    # Establecemos el LARGO y ALTO de la pantalla
    DIMENSION_VENTANA = [704, 634]
    pantalla = pygame.display.set_mode(DIMENSION_VENTANA)

    # Establecemos el título de la pantalla.
    pygame.display.set_caption("SNAKE")

    # Establecemos imagenes
    snake_draw = load_image('snake.png')
    chicken_draw = load_image('chicken.png')

    # Lo usamos para establecer cuán rápido de refresca la pantalla.
    reloj = pygame.time.Clock()


    while True:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                sys.exit()

        ##pantalla.blit(snake_draw, (0, 0))
        ##pantalla.blit(chicken_draw, (35, 0))

        pantalla.fill(NEGRO)

        # Dibujamos la retícula
        for i in range(18):
            for j in range(20):
                color = BLANCO
                if matrix[i][j] == 'o':
                    color = MORADO
                if matrix[i][j] == 'x':
                    color = ROJO
                pygame.draw.rect(pantalla,
                                 color,
                                 [(margin + width) * j + margin,
                                  (margin + height) * i + margin,
                                  width,
                                  height])
        reloj.tick(60)

        pygame.display.flip()
    pygame.quit()


# Lógica del juego

def copyList(list, copy):
    for i in list:
        copy.append(i)
    return copy

def removeElement(list, element):
    list.remove(element)
    return list

def moveSnake(solution, selectedDot, snake):
    moveIndex(solution, selectedDot, snake, 0) #mueve en eje X
    moveIndex(solution, selectedDot, snake, 1) #mueve en eje Y
    return solution

def moveIndex(solution, selectedDot, snake, index):
    if snake[index] > selectedDot[index]:
        while (snake[index] != selectedDot[index]):
            snake[index] = snake[index] - 1
            solution.append((snake[0], snake[1]))
    else:
        while (snake[index] != selectedDot[index]):
            snake[index] = snake[index] + 1
            solution.append((snake[0], snake[1]))

def profundity(dots, solution, snake, result):
    if(len(dots) == 0):
        if len(result) > 0:
            if len(result[0]) > len(solution):
                result.pop()
                result.append(solution)
        else:
            result.append(solution)
    for i in dots:
        profundity(removeElement(copyList(dots, []), i), moveSnake(copyList(solution, []), i, copyList(snake, [])), [i[0], i[1]], result)

def fillMatrix(matrix, dots, snake):
    for i in dots:
        matrix[i[0]][i[1]] = 'x'
    matrix[snake[0]][snake[1]] = 'o'
    return matrix

def main(matrix, dots, snake, result):
    #displayGraphics(fillMatrix(matrix, dots, snake))
    profundity(dots, [(0, 0)], snake, result)#el resultado esta en result[0]
    fillMatrix(matrix, dots, snake)

main([['-'] * 20 for _ in range(18)], [(9, 5), (2, 11), (8, 18), (17, 4), (13, 19)], [0, 0], [])
