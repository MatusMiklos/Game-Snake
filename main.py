import pygame
import snake
import food
import gameScreen
import qlearning
from fann2 import libfann
from random import randint
import math

ann = libfann.neural_net()

ann.create_standard_array([4, 12, 1])
ann.set_learning_rate(0.7)
ann.set_learning_momentum(0.1)
ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC)



def createInput(d = -1):
    inputs = [0, 0, 0, 0]

    headPos = [int(xyOfSnake[0][0] / 10), int(xyOfSnake[0][1] / 10)]
    applePos = [apple.x / 10, apple.y/ 10]
    direct = direction

    # smer hada 0-hore 1-doprava 2-dole 3-dolava
    if(d != -1):
        direct = makeDir(direction, d)
        if(direct == 0): #hore
            headPos[1] = headPos[1] - 1
        elif(direct == 2): #dole
            headPos[1] = headPos[1] + 1
        elif(direct == 3): #dolava
            headPos[0] = headPos[0] - 1
        else:
            headPos[0] = headPos[0] + 1

    inputs[0] = math.sqrt(math.pow(applePos[0] - headPos[0], 2) + math.pow(applePos[1] - headPos[1], 2)) / (math.sqrt(2) * gameDisplayWidth / 10)


    left = [headPos[0], headPos[1]]
    front = [headPos[0], headPos[1]]
    right = [headPos[0], headPos[1]]
    # if(direct == 0): #hore
    #     left[0] = left[0] - 1
    #     front[1] = front[1] - 1
    #     right[0] = right[0] + 1
    # elif(direct == 2): #dole
    #     left[0] = left[0] + 1
    #     front[0] = front[0] - 1
    #     right[1] = right[1] - 1
    # elif(direct == 3): #dolava
    #     left[1] = left[1] + 1
    #     front[1] = front[1] - 1
    #     right[0] = right[0] + 1
    # else: #doprava
    #     left[1] = left[1] - 1
    #     front[0] = front[0] + 1
    #     right[1] = right[1] + 1
    if (direct == 0):  # hore
        left[0] = left[0] - 1
        front[1] = front[1] - 1
        right[0] = right[0] + 1
    elif (direct == 2):  # dole
        left[0] = left[0] + 1
        front[1] = front[1] + 1
        right[0] = right[0] - 1
    elif (direct == 3):  # dolava
        left[1] = left[1] + 1
        front[0] = front[0] - 1
        right[1] = right[1] - 1
    else:  # doprava
        left[1] = left[1] - 1
        front[0] = front[0] + 1
        right[1] = right[1] + 1

    if(left[1] >= 0 and left[1] < gameDisplayWidth /10 and left[0] >= 0 and left[0] < gameDisplayWidth /10):
        if(gameMap[left[1]][left[0]] == 0):
            inputs[1] = 0
        elif(left[0] == applePos[0] and left[1] == applePos[1]):
            inputs[1] = 1
        else:
            inputs[1]=-1
    else:
        inputs[1] = -1

    if(front[1] >= 0 and front[1] < gameDisplayWidth / 10 and front[0] >= 0 and front[0] < gameDisplayWidth / 10):
        if( gameMap[front[1]][front[0]] == 0):
            inputs[2] = 0
        elif(front[0] == applePos[0] and front[1] == applePos[1]):
            inputs[2] = 1
        else:
            inputs[2]=-1
    else:
        inputs[2] = -1

    if(right[1] >= 0 and right[1] < gameDisplayWidth /10 and right[0] >= 0 and right[0] < gameDisplayWidth /10 ):
        if(gameMap[right[1]][right[0]] == 0):
            inputs[3] = 0
        elif(right[0] == applePos[0] and right[1] == applePos[1]):
            inputs[3] = 1
        else:
            inputs[3]=-1
    else:
        inputs[3] = -1

    return inputs

def think(life = False):
    global curiosity

    rand = randint(0, 100)
    if(life == False and rand < curiosity):
        d = randint(0, 2)
        curiosity -= 1
    else:
        #Qlearning.getMap(gameMap) # musi byt kvoli pouzitiu funkcie Qlearning.getLoc()
        maxQ = - 999
        input_front = createInput(1)
        tempQ = ann.run(input_front)
        if(tempQ[0] > maxQ):
            maxQ = tempQ[0]
            d = 1

        input_left = createInput(0)
        tempQ = ann.run(input_left)
        if(tempQ[0] > maxQ):
            maxQ = tempQ[0]
            d = 0

        input_right = createInput(2)
        tempQ = ann.run(input_right)
        if(tempQ[0] > maxQ):
            maxQ = tempQ[0]
            d = 2


    inputs = createInput()
    global direction
    direction = makeDir(direction, d)
    if(life == True):
        iteration(1)
    else:
        iteration("UCIME")
        ann.train(inputs, [odmena])
        #print(inputs, odmena)

#base - podla toho vracia
#0 hore
#1 doprava
#2 dole
#3 dolava
def makeDir(base, d): #d=0 dolava, d=1 dopredu, d=2 doprava
    if (d == 0):
        if (base == 0):
            return 3
        elif (base == 2):
            return 1
        elif (base == 3):
            return 2
        elif(base==1):
            return 0
    elif (d == 1):
        return base
    elif (d == 2):
        if (base == 0):
            return 1
        elif (base == 2):
            return 3
        elif (base == 3):
            return 0
        elif(base==1):
            return 2


#jeden pohyb
#mode = 0 ucenie
#     = 1 vykresluje
def iteration(mode):
    global xyOfSnake, lenSnake, score, odmena, gameMap, steps, paused

    headPos = [int(xyOfSnake[0][0] / 10), int(xyOfSnake[0][1] / 10)]
    applePos = [apple.x / 10, apple.y / 10]

    xyOfSnake = player.movement(xyOfSnake, direction)

    if player.crashed(xyOfSnake, gameMap):
        odmena = -100
        #gameScreen.messageCrashed('You crashed!')
        #gameMap = gameScreen.mapUpdate(apple.x, apple.y, xyOfSnake)
        #crashed = True
        reset(True)
    elif apple.eaten(xyOfSnake[0][0], xyOfSnake[0][1]):
        odmena = 100
        lenSnake += 1
        score += 1
        xyOfSnake = player.update(xyOfSnake, apple.x, apple.y)
        apple.spawnNew(xyOfSnake, gameMap)
        steps = 0
    else:
        #dava divne hodnoty
        #odmena = -1.0 * math.sqrt(math.pow(apple.x - xyOfSnake[0][0], 2) + math.pow(apple.y - xyOfSnake[0][1], 2)) / (math.sqrt(2)*gameDisplayWidth/10)
        odmena = -1.0 * math.sqrt(math.pow(applePos[0] - headPos[0], 2) + math.pow(applePos[1] - headPos[1], 2)) / (math.sqrt(2) * gameDisplayWidth / 10)

    gameDisplay.fill(black)
    gameScreen.gameScreenDisplay(score)
    gameMap = gameScreen.mapUpdate(apple.x, apple.y, xyOfSnake)


    # #VYKRESLOVANIE
    if mode == 1:
        gameScreen.displayWalls(gameMap)
        player.display(xyOfSnake)
        apple.display()
        pygame.display.update()
        clock.tick(45)

def reset(badmove = False):
    # inicializacia hada
    global xyOfSnake, lenSnake, odmena, eaten, crashed, score, direction, steps, gameMap
    xyOfSnake = []
    lenSnake = 2
    if not badmove:
        odmena = 0

    steps = 0
    for i in range(0, lenSnake):
        xySnake = []
        xySnake.append(20)
        xySnake.append(20 + i*10)
        # xySnake.append(gameDisplayWidth / 2)
        # xySnake.append((gameDisplayHeight - 30) / 2 + i * 10)
        xyOfSnake.append(xySnake)


    player = snake.Snake(gameDisplay)  # had
    #apple = food.Food(gameDisplay)  # jablko
    eaten = True
    crashed = False  # naburanie
    score = 0  # score
    direction = 0  # smer hada 0-hore 1-doprava 2-dole 3-dolava

    # pridame prveho jedla na mapu
    gameMap = gameScreen.mapUpdate(0, 0, xyOfSnake)
    apple.spawnNew(xyOfSnake, gameMap)
    gameMap = gameScreen.mapUpdate(apple.x, apple.y, xyOfSnake)

#global xyOfSnake, lenSnake, odmena, eaten, crashed, score, direction, steps, gameMap
black = (0, 0, 0)
pygame.init()

gameDisplayWidth = 50
gameDisplayHeight = 50

#uprava pre rozlisenie
gameDisplayHeight = gameDisplayHeight * 10
gameDisplayHeight += 30
gameDisplayWidth = gameDisplayWidth * 10

#nastavenie displeja
pygame.display.set_caption('Snake')
gameDisplay = pygame.display.set_mode((gameDisplayWidth, gameDisplayHeight))
gameDisplay.fill(black)

clock = pygame.time.Clock()
gameScreen = gameScreen.gameScreen(gameDisplay)


# inicializacia hada
xyOfSnake = []
lenSnake = 2
odmena = 0
for i in range(0, lenSnake):
    xySnake = []
    xySnake.append(gameDisplayWidth / 2)
    xySnake.append((gameDisplayHeight - 30) / 2 + i * 10)
    xyOfSnake.append(xySnake)

#print(xyOfSnake[0][1])
#print(xyOfSnake[0][1] / 10)

player = snake.Snake(gameDisplay)  # had
apple = food.Food(gameDisplay)  # jablko
Qlearning = qlearning.Qlearning()
eaten = True
crashed = False  # naburanie
score = 0  # score
direction = 0  # smer hada 0-hore 1-doprava 2-dole 3-dolava

# pridame prveho jedla na mapu
gameMap = gameScreen.mapUpdate(apple.x, apple.y, xyOfSnake)

x = 0
epochs = 10000
curiosity = epochs
steps = 0

for x in range(epochs):
    #if(steps > 2*gameDisplayWidth/10):
    #    reset()

    #if(x % 1000 == 0):
    print("epoch: ", x)

    think()
    #steps += 1

reset()
steps = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset()
    think(True)

pygame.quit()
quit()
