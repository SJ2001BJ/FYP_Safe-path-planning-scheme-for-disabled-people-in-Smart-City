import pygame
import sys

window_width = 900
window_height = 900

window = pygame.display.set_mode((window_height,window_width))

def main():
    while True:
        for event in pygame.event.get():
            #quit window
          if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()


        window.fill((0,0,0))

        pygame.display.flip()


main()
