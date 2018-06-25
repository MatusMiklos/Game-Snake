import pygame
import time

class gameScreen:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameScreenWidth = self.gameDisplay.get_width()
        self.gameScreenHeight = self.gameDisplay.get_height() -30

    def mapUpdate(self,  appleX, appleY, snake):#opravit ked nabura
        gameMap = [[0 for _ in range((int)(self.gameScreenHeight / 10))]
                   for _ in range((int)(self.gameScreenWidth / 10))]

        #for i in range(0, len(gameMap)):#steny
        #    gameMap[0][i]= 3
        #    gameMap[i][0] = 3
        #    gameMap[len(gameMap)-1][i] = 3
        #    gameMap[i][len(gameMap)-1] = 3
        # for i in range(0, int(len(gameMap) / 2)):
        #     gameMap[int(len(gameMap)/4)+ i][int(len(gameMap)/2)] = 4
        #     gameMap[int(len(gameMap) / 2)][int(len(gameMap)/4) +i] = 4


        for i in range(1, len(snake)):
            gameMap[(int)(snake[i][1]/10)][(int)(snake[i][0]/10)] = 3#telo hada

        gameMap[(int)(snake[0][1] / 10)][(int)(snake[0][0] / 10)] = 2#hlava hada

        gameMap[(int)(appleY / 10)][(int)(appleX / 10)] = 1#jedlo

        return gameMap

    def mapPrint(self, gameMap):
        toDisplay = ""
        for i in range(0, len(gameMap)):
            for j in range(0, len(gameMap)):
                toDisplay+=(str)(gameMap[i][j])
            toDisplay+='\n'
        print (toDisplay)

    def textObjects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def messageDisplay(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', int(30 / 2))
        TextSurf, TextRect = self.textObjects(text, largeText)
        TextRect.center = (self.gameScreenWidth * 3/4, self.gameScreenHeight + 30 /2)
        self.gameDisplay.blit(TextSurf, TextRect)

    def gameScreenDisplay(self, score):
        pygame.draw.line(self.gameDisplay, (255, 255, 255), (0, self.gameScreenHeight),
                         (self.gameScreenWidth, self.gameScreenHeight))
        text = 'Score: ' + str(score)
        largeText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = self.textObjects(text, largeText)
        TextRect.center = (
        self.gameScreenWidth * 3 / 4, self.gameScreenHeight + 10)
        self.gameDisplay.blit(TextSurf, TextRect)

    def messageCrashed(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', int(self.gameScreenWidth / 10))
        TextSurf, TextRect = self.textObjects(text, largeText)
        TextRect.center = (self.gameScreenWidth / 2, self.gameScreenHeight / 2)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(2)

    def displayWalls(self, gamemap):
        for i in range(0, len(gamemap)):
            for j in range(0, len(gamemap)):
                if gamemap[j][i] == 4:
                    pygame.draw.rect(self.gameDisplay, (255, 255, 255), (i*10, j*10, 10, 10))

