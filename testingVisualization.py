import pygame
import sys #module system

#Step 1: Create a pygame window
#Step 2: Create a grid

window_width = 800
window_height = 800

window = pygame.display.set_mode((window_height,window_width))

columns = 50
rows = 50

boxWidth = window_width//columns
boxHeight = window_height//rows

grid = []

class Box:
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.destination = False
    def draw(self,win,color):
        pygame.draw.rect(win,color,(self.x * boxWidth, self.y * boxHeight, boxWidth - 2, boxHeight - 2))
        #Add margin



#Create grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

#The starting point is located at the top left vertex of the entire grid graph
startBox = grid[0][0]
startBox.start = True

def main():
    beginSearch= False
    destination_box_set = False




    while True:
        # Close window
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
        # Mouse Controls:
          elif event.type == pygame.MOUSEMOTION:
        #set the mouse cursor position
             x = pygame.mouse.get_pos()[0]
             y = pygame.mouse.get_pos()[1]
             # Draw Wall
             if event.buttons[0]:
                 i = x // boxWidth
                 j = y // boxHeight
                 grid[i][j].wall = True
            # Set destination
             if event.buttons[2] and not destination_box_set:
                 i = x // boxWidth
                 j = y // boxHeight
                 destination_box = grid[i][j]
                 destination_box.destination = True
                 destination_box_set = True

          # Algorithm implementation
          if event.type == pygame.KEYDOWN and destination_box_set:
              begin_search = True






        window.fill((0,0,0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window,(20,20,20))
                if box.start:
                     box.draw(window,(0, 200, 200))
                if box.wall:
                     box.draw(window, (90, 90, 90))
                if box.destination:
                     box.draw(window, (200, 200, 0))
        pygame.display.flip()


main()

