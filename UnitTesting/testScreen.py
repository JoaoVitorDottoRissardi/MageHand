import pygame
from time import sleep

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
originalImage = pygame.image.load('./images/screen1.png')
screen.blit(originalImage, (0,0))
pygame.display.flip()

sleep(5)

pygame.quit()

