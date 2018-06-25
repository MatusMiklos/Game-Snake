#Q-learning
class Qlearning:
    def __init__(self):
        self.player = (-1, -1)
        self.food = (-1, -1)

    def restartPos(self):
        self.player = (-1, -1)
        self.food = (-1, -1)

    def getMap(self, gameMap):
        self.gameMap = gameMap
        self.gameMapX = len(gameMap)
        self.gameMapY = len(gameMap[0])

    def getLoc(self, gameMap, obj):
        for i in range(len(gameMap)):
            for j in range(len(gameMap[0])):
                if (gameMap[i][j] == obj):
                    return j,i

    def reward(self):
        self.player = self.getLoc(2)
        if self.player[0] == 0 or self.player[0] == self.gameMapX or self.player[1] == 0 or self.player[1] == self.gameMapY:
            return -100


        #ked zje jedlo
        if self.food == (-1, -1):
            self.food = self.getLoc(1)
        else:
            if self.food != self.getLoc(1):
                self.food = (-1, -1)
                return 50

        return 0
