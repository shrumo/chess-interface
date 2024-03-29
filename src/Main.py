__author__ = 'Maksymilian Mika'

import sys, pygame
import Display

pygame.init()
pygame.font.init()
size = width, height = 60*8, 60*8
black = 0, 0, 0
screen = pygame.display.set_mode(size)

board_display = Display.BoardDisplay()

set = False

while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board_display.dragged(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                board_display.dropped(pygame.mouse.get_pos())

    
        screen.fill(black)
        board_display.display(screen)
        pygame.display.flip()
