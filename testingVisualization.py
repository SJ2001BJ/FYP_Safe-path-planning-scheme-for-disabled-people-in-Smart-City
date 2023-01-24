import pygame
import sys #module system
from tkinter import  messagebox, Tk

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
queue = []
path = []
class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.destination = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
    def draw(self,win,color):
        pygame.draw.rect(win,color,(self.x * boxWidth, self.y * boxHeight, boxWidth - 2, boxHeight - 2))
        #Add margin

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


#Create grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

#Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()



#The starting point is located at the top left vertex of the entire grid graph
startBox = grid[0][0]
startBox.start = True
startBox.visited = True
queue.append(startBox)



def main():
    beginSearch= False
    destination_box_set = False
    searching = True
    destination_box = None
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
              beginSearch = True

        if beginSearch:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == destination_box:
                    searching = False
                    while current_box.prior != startBox:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window,(100,100,100))

                if box.queued:
                    box.draw(window, (200, 0, 0))
                if box.visited:
                    box.draw(window, (0, 200, 0))
                if box in path:
                    box.draw(window, (0, 0, 200))

                if box.start:
                     box.draw(window, (0, 200, 200))
                if box.wall:
                     box.draw(window, (10, 10, 10))
                if box.destination:
                     box.draw(window, (200, 200, 0))
        pygame.display.flip()


main()

