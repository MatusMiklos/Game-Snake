import pygame
import random

class Food:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameScreenWidth = self.gameDisplay.get_width()
        self.gameScreenHeight = self.gameDisplay.get_height()-30
        self.x = random.randint(1, (self.gameScreenWidth - 20) / 10)*10
        self.y = random.randint(1, (self.gameScreenHeight - 20) / 10)*10

    #coordinates - snake's body
    def spawnNew(self, coordinates, gamescreen):
        goodCor = False
        pygame.draw.rect(self.gameDisplay, (0, 0, 0), (self.x, self.y, 10, 10))
        while not goodCor:
            self.x = random.randint(1, (self.gameScreenWidth - 20)/ 10)*10
            self.y = random.randint(1, (self.gameScreenHeight - 20) / 10)*10
            for i in range(0, len(coordinates)):
                if self.x != coordinates[i][0] and self.y != coordinates[i][1]:
                    goodCor = True
                else:
                    goodCor = False
                    break
            if gamescreen[int(self.y / 10)][int(self.x / 10)] == 4:
                goodCor = False

    def display(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), (self.x, self.y, 10, 10))

    #x,y coordinates of snake's head
    def eaten(self, x, y):
        if x == self.x and y == self.y:
            return True
        else:
            return False

