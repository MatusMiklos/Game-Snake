import pygame

class Snake:
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.gameScreenWidth = self.gameDisplay.get_width()
        self.gameScreenHeight = self.gameDisplay.get_height() - 30


    def display(self, coordinates):
        for i in range (0, len(coordinates)):
            if i == 0:
                pygame.draw.rect(self.gameDisplay, (0,0,255), (coordinates[i][0], coordinates[i][1], 10, 10))
            else:
                pygame.draw.rect(self.gameDisplay, (255, 255, 255), (coordinates[i][0], coordinates[i][1], 10, 10))

    def update(self, coordinates, x, y):#ked sa nazere
        temp = []
        temp.append(coordinates[-1][0])
        temp.append(coordinates[-1][1])
        coordinates.append(temp)

        for i in range(len(coordinates)-2, -1, -1):
            if i> 0:
                coordinates[i][0] = coordinates[i-1][0]
                coordinates[i][1] = coordinates[i-1][1]
            else:
                coordinates[i][0] = x
                coordinates[i][1] = y
        return coordinates

    def movement(self, coordinates, direction):#ked sa hybe
        for i in range(len(coordinates) - 1, -1, -1):
            if i > 0:
                coordinates[i][0] = coordinates[i-1][0]
                coordinates[i][1] = coordinates[i-1][1]
            else:
                if direction == 0:
                    coordinates[i][1] -= 10
                elif direction == 1:
                    coordinates[i][0] += 10
                elif direction == 2:
                    coordinates[i][1] += 10
                else:
                    coordinates[i][0] -= 10
        return coordinates

    def crashed(self, coordinates, gamemap):
        if (coordinates[0][0] < 0) or (coordinates[0][0] >= self.gameScreenWidth) or (coordinates[0][1] < 0) or  (coordinates[0][1] >= self.gameScreenHeight):
            return True

        for i in range(1, len(coordinates)):
            if coordinates[0][0] == coordinates[i][0] and coordinates[0][1] == coordinates[i][1]:
                return True

        if gamemap[int(coordinates[0][1]/10)][int(coordinates[0][0]/10)] == 4:
            return  True
        return False

    def distanceFromFood(self, ):
        distance = 0

        return distance