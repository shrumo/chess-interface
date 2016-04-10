__author__ = 'Maksymilian Mika'

import sys, pygame
import Display

pygame.init()
pygame.font.init()
size = width, height = 60*8, 60*8
speed = [1, 1]
black = 0, 0, 0
screen = pygame.display.set_mode(size)

ball = pygame.image.load("lol.png")
ballrect = ball.get_rect()
ballrect.center = (width/2,height/2+180)

board_display = Display.BoardDisplay()

set = False

drag = False
while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ballrect.collidepoint(pygame.mouse.get_pos()):
                    drag = True
                board_display.dragged(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False
                board_display.dropped(pygame.mouse.get_pos())

        if drag: ballrect.center = (pygame.mouse.get_pos())
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = - speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        screen.fill(black)
        board_display.display(screen)
        if board_display.board.win is not None:
            if not set:
                ballrect.center = (width/2,height/2+200)
                set = True
            if board_display.board.win == "White":
                ball = pygame.image.load("black_king.png")
                screen.blit(ball,ballrect)
            else:
                ball = pygame.image.load("white_king.png")
                screen.blit(ball,ballrect)

        pygame.display.flip()