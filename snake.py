import random
import pygame
import sys
from pygame.locals import *
import numpy as np

global go_self          #是不是自己操作游戏
go_self = False          #如果自己操作 改为True 如果让蛇自己跑  改为False

#列出各种可能用到的颜色
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
DarkGreen = (0, 155, 0)
DarkGray = (40, 40, 40)
Yellow = (255, 255, 0)
RedDark = (150, 0, 0)
Blue = (0, 0, 255)
BlueDark = (0, 0, 150)

#定义上下左右方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class background():
    def __init__(self,Width,Height,BlockSize,BackgroundColor):
        self.Width = Width
        self.Height = Height
        self.BlockSize = BlockSize
        self.BackgroundColor = BackgroundColor
        self.BlockWidth = int(Width/BlockSize)
        self.BlockHeight = int(Height/BlockSize)

    def showContinue(self):
        Screen.blit(print_text('Press any key to continue', 20, White), (self.Width - 250, self.Height - 30))

    # 画线形成表格
    def drawGrid(self):
        for x in range(0, self.Width, self.BlockSize):   # 从(x,0)画一条线到(x,Height)
            pygame.draw.line(Screen, DarkGray, (x, 0), (x, self.Height))
        for y in range(0, self.Height, self.BlockSize):  # 从(0,y)画一条线到(Width,y)
            pygame.draw.line(Screen, DarkGray, (0, y), (self.Width, y))
    # 打印游戏开始时界面
    def drawStartScreen(self):
        Screen.fill(White)
        MyFont = pygame.font.Font('内置文件/思源黑体.otf', 35)
        PressKeySurf = MyFont.render('欢迎来到贪吃蛇', True, Blue)
        pressKeyRect = PressKeySurf.get_rect()
        pressKeyRect.topleft = (self.Width - 270, self.Height - 450)
        Screen.blit(PressKeySurf, pressKeyRect)
        Screen.blit(print_text('按esc键可结束游戏', 25, Red), (self.Width - 280, self.Height - 350))
        Screen.blit(print_text('按键盘上的上下左右可以', 25, Red), (self.Width - 280, self.Height - 250))
        Screen.blit(print_text('控制蛇的方向', 25, Red), (self.Width - 280, self.Height - 220))
        Screen.blit(print_text('得了10分就不会打印表格', 25, Red), (self.Width - 280, self.Height - 190))
        Screen.blit(print_text('请按任意键开始游戏', 25, Red), (self.Width - 280, self.Height - 150))
        Screen.blit(print_text('祝你好运', 25, Red), (self.Width - 280, self.Height - 50))
        Screen.blit(PressKeySurf, pressKeyRect)
        picture = pygame.image.load('内置文件/u=20525293,3051623083&fm=26&gp=0.jpg')
        Screen.blit(picture, (0, 0))
        while True:
            if checkForKeyPress():
                pygame.event.get()
                return
            pygame.display.update()
            SnakeClock.tick(Snake.SnakeSpeed)
    # 打印游戏结束得界面
    def showGameOverScreen(self):
        GameOverFont = pygame.font.Font('freesansbold.ttf', 180)
        GameSurf = GameOverFont.render('Game', True, White)
        OverSurf = GameOverFont.render('Over', True, White)
        GameRect = GameSurf.get_rect()
        overRect = OverSurf.get_rect()
        GameRect.midtop = (self.Width / 2, 40)
        overRect.midtop = (self.Width / 2, GameRect.height + 100)
        Screen.blit(GameSurf, GameRect)
        Screen.blit(OverSurf, overRect)
        self.showContinue()
        pygame.display.update()
        pygame.time.wait(500)
        checkForKeyPress()
        while True:
            if checkForKeyPress():
                pygame.event.get()
                return

class snake():
    def __init__(self,SnakeSpeed,SnakeHead):
        self.SnakeSpeed = SnakeSpeed
        self.SnakeHead = SnakeHead
        HeadX = int(background.BlockWidth / 2)
        HeadY = int(background.BlockHeight / 2)
        self.SnakeBody = [{'x': HeadX, 'y': HeadY},
                          {'x': HeadX, 'y': HeadY + 1},
                          {'x': HeadX, 'y': HeadY + 2}]
        self.Stones = []
        self.Apple = {'x': int(1), 'y': int(1)}
    #随机生成石头
    def getStone(self):
        while True:
            temp = {'x': random.randint(0, background.BlockWidth - 1),
                    'y': random.randint(0, background.BlockHeight - 1)}
            if temp not in self.SnakeBody and temp not in self.Stones:
                self.Stones.append(temp)
                if len(self.Stones) == 20:
                    break
    # 随机生成苹果坐标
    def getRandomLocation(self):
        while True:  # 避免出现在蛇身上以及石头上
            temp=dict(x=random.randint(0, background.BlockWidth - 1),
                      y=random.randint(0, background.BlockHeight - 1))
            if temp not in self.SnakeBody and temp not in self.Stones:
                self.Apple = temp
                break
    # 加速
    def add_the_speed(self):
        self.SnakeSpeed +=0.2
    # 打印蛇身
    def drawWorm(self):
        index = 0
        for Body in self.SnakeBody:
            index += 1
            x = Body['x'] * background.BlockSize
            y = Body['y'] * background.BlockSize
            WormSegmentRect = pygame.Rect(x, y, background.BlockSize, background.BlockSize)
            pygame.draw.rect(Screen, DarkGreen, WormSegmentRect)
            WormInnerSegmentRect = pygame.Rect(
                x + 4, y + 4, background.BlockSize - 8, background.BlockSize - 8)
            if index == 1:  # 蛇头颜色与蛇身不一样
                pygame.draw.rect(Screen, White, WormInnerSegmentRect)
            else:
                pygame.draw.rect(Screen, Green, WormInnerSegmentRect)

    # 打印石头
    def drawStone(self):
        for stone in self.Stones:
            x = stone['x'] * background.BlockSize
            y = stone['y'] * background.BlockSize
            WormSegmentRect = pygame.Rect(x, y, background.BlockSize, background.BlockSize)
            pygame.draw.rect(Screen, Blue, WormSegmentRect)
            WormInnerSegmentRect = pygame.Rect(
                x + 4, y + 4, background.BlockSize - 8, background.BlockSize - 8)
            pygame.draw.rect(Screen, Yellow, WormInnerSegmentRect)

    # 打印苹果
    def drawApple(self):
        x = self.Apple['x'] * background.BlockSize
        y = self.Apple['y'] * background.BlockSize
        appleRect = pygame.Rect(x, y, background.BlockSize, background.BlockSize)
        pygame.draw.rect(Screen, Red, appleRect)
    # 打印分数
    def drawScore(self):
        BasicFont = pygame.font.Font('freesansbold.ttf', 20)
        scoreSurf = BasicFont.render('Score: ' + str(len(self.SnakeBody)-3), True, White)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (10, 10)
        Screen.blit(scoreSurf, scoreRect)

background = background(800, 500, 25, Black)
Snake = snake(6,0)

#游戏结束
def GameOver():
    pygame.quit()
    sys.exit()

def playGame():
    direction = 5        #不设置起始方向
    Snake.getStone()     #随机获得障碍
    Snake.getRandomLocation()
    SnakeHead = Snake.SnakeHead
    ans = goYourSelf(Snake.SnakeBody[SnakeHead],Snake.Apple,UP)
    while True:
        for event in pygame.event.get():  # 从队列当中获取事件
            if event.type == QUIT:
                GameOver()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT: #输入的方向不能与当前位置相反
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE   :
                    GameOver()

        #如果蛇到了边缘 就将蛇头放到对面边缘  不为墙体设置障碍
        if Snake.SnakeBody[SnakeHead]['x'] == -1:
            Snake.SnakeBody[SnakeHead]['x'] = background.BlockWidth - 1
        elif Snake.SnakeBody[SnakeHead]['x'] == background.BlockWidth:
            Snake.SnakeBody[SnakeHead]['x'] = 0
        elif Snake.SnakeBody[SnakeHead]['y'] == -1:
            Snake.SnakeBody[SnakeHead]['y'] = background.BlockHeight - 1
        elif Snake.SnakeBody[SnakeHead]['y'] == background.BlockHeight:
            Snake.SnakeBody[SnakeHead]['y'] = 0

        #判断蛇是否吃到自己
        for Body in Snake.SnakeBody[1:]:
            if Body['x'] == Snake.SnakeBody[SnakeHead]['x'] and Body['y'] == Snake.SnakeBody[SnakeHead]['y']:
                return  # game over

        #判断蛇是否撞到了石头
        for stone in Snake.Stones[0:]:
            if stone['x'] == Snake.SnakeBody[SnakeHead]['x'] and stone['y'] == Snake.SnakeBody[SnakeHead]['y']:
                return  # game over

        # 判断是否吃到苹果
        # 每次更新蛇的方法为 删掉尾巴  并且重新加一个蛇头
        # 如果吃到苹果 就不要删尾巴 这样就加了一个长度
        if Snake.SnakeBody[SnakeHead]['x'] == Snake.Apple['x'] and Snake.SnakeBody[SnakeHead]['y'] == Snake.Apple['y']:
            Snake.getRandomLocation()
            Snake.add_the_speed()
            ans = goYourSelf(Snake.SnakeBody[SnakeHead],Snake.Apple,direction)
        elif direction!=5:
            del Snake.SnakeBody[-1]

        if go_self == False:
            if len(ans) > 0:
                direction = ans[0]
                del ans[0]
        #确定方向 重新定义一个蛇头
        if direction == UP:
            Head = {'x': Snake.SnakeBody[SnakeHead]['x'],
                       'y': Snake.SnakeBody[SnakeHead]['y'] - 1}
        elif direction == DOWN:
            Head = {'x': Snake.SnakeBody[SnakeHead]['x'],
                       'y': Snake.SnakeBody[SnakeHead]['y'] + 1}
        elif direction == LEFT:
            Head = {'x': Snake.SnakeBody[SnakeHead][
                                'x'] - 1, 'y': Snake.SnakeBody[SnakeHead]['y']}
        elif direction == RIGHT:
            Head = {'x': Snake.SnakeBody[SnakeHead][
                                'x'] + 1, 'y': Snake.SnakeBody[SnakeHead]['y']}
        if direction != 5:
            Snake.SnakeBody.insert(0, Head)

        #每次操作完成  把表格 蛇 石头 苹果 分数全部重新打印一遍
        Screen.fill(background.BackgroundColor)
        #增加游戏难度 得了10分就不会打印表格
        if len(Snake.SnakeBody) < 13:
            background.drawGrid()
        Snake.drawWorm()
        Snake.drawStone()
        Snake.drawApple()
        Snake.drawScore()
        pygame.display.update()
        SnakeClock.tick(Snake.SnakeSpeed)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        GameOver()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        GameOver()
    return keyUpEvents[0].key

def print_text(content, size, color):
    font = pygame.font.SysFont('kaiti', size)
    text = font.render(content, True, color)
    return text

def goYourSelf(start,point,dir):
    map = np.zeros((background.BlockWidth+5, background.BlockHeight+5))
    direction = np.zeros((background.BlockWidth+5, background.BlockHeight+5))
    queue = []
    queue.append(start)
    direction[start['x']][start['y']] = dir
    for stone in Snake.Stones[0:]:
        x = stone['x']
        y = stone['y']
        map[x][y] = 1
    for body in Snake.SnakeBody[0:]:
        x = body['x']
        y = body['y']
        map[x][y] = 1
    while True:
        now = queue[0]
        x = now['x']
        y = now['y']
        del queue[0]
        if direction[x][y] != 2:
            xx = x  
            yy = y - 1
            if xx == -1:
                xx = background.BlockWidth-1
            if xx == background.BlockWidth:
                xx = 0
            if yy == -1:
                yy = background.BlockHeight-1
            if yy == background.BlockHeight:
                yy = 0
            if map[xx][yy] != 1 and direction[xx][yy] == 0:
                direction[xx][yy] = 1
                if xx == point['x'] and yy == point['y']:
                    break
                temp = {'x': xx, 'y': yy}
                queue.append(temp)
        if direction[x][y] != 1:
            xx = x
            yy = y + 1
            if xx == -1:
                xx = background.BlockWidth - 1
            if xx == background.BlockWidth:
                xx = 0
            if yy == -1:
                yy = background.BlockHeight - 1
            if yy == background.BlockHeight:
                yy = 0
            if map[xx][yy] != 1 and direction[xx][yy] == 0:
                direction[xx][yy] = 2
                if xx == point['x'] and yy == point['y']:
                    break
                temp = {'x': xx, 'y': yy}
                queue.append(temp)
        if direction[x][y] != 4:
            xx = x - 1
            yy = y
            if xx == -1:
                xx = background.BlockWidth - 1
            if xx == background.BlockWidth:
                xx = 0
            if yy == -1:
                yy = background.BlockHeight - 1
            if yy == background.BlockHeight:
                yy = 0
            if map[xx][yy] != 1 and direction[xx][yy] == 0:
                direction[xx][yy] = 3
                if xx == point['x'] and yy == point['y']:
                    break
                temp = {'x': xx, 'y': yy}
                queue.append(temp)
        if direction[x][y] != 3:
            xx = x + 1
            yy = y
            if xx == -1:
                xx = background.BlockWidth - 1
            if xx == background.BlockWidth:
                xx = 0
            if yy == -1:
                yy = background.BlockHeight - 1
            if yy == background.BlockHeight:
                yy = 0
            if map[xx][yy] != 1 and direction[xx][yy] == 0:
                direction[xx][yy] = 4
                if xx == point['x'] and yy == point['y']:
                    break
                temp = {'x': xx, 'y': yy}
                queue.append(temp)
        if len(queue) == 0:
            break
    ans = []
    x = point['x']
    y = point['y']
    if direction[x][y] == 0:
        return ans
    while True:
        ans.append(direction[x][y])
        if direction[x][y] == 1:
            y += 1
        elif direction[x][y] == 2:
            y -= 1
        elif direction[x][y] == 3:
            x += 1
        elif direction[x][y] == 4:
            x -= 1
        if x == -1:
            x = background.BlockWidth - 1
        if x == background.BlockWidth:
            x = 0
        if y == -1:
            y = background.BlockHeight - 1
        if y == background.BlockHeight:
            y = 0
        if x == start['x'] and y == start['y']:
            ans.append(direction[x][y])
            break
    ans.reverse()
    return ans[1:]

if __name__ == '__main__':
    global SnakeClock, Screen
    pygame.init()
    SnakeClock = pygame.time.Clock()
    Screen = pygame.display.set_mode((background.Width, background.Height))  # 设置背景
    pygame.display.set_caption('贪吃蛇   author:宣启楠')
    background.drawStartScreen()
    while True:
        pygame.mixer.music.load('内置文件/买辣椒也用券 - 起风了.mp3')
        pygame.mixer.music.play(-1, 0)  # 背景音乐循环播放
        Snake = snake(10,0)
        playGame()
        # 游戏运行与Game Over播放不一样的背景音乐
        pygame.mixer.music.load('内置文件/妹尾武 - 夏祭り、夢花火。 (夏日祭，梦花火。).mp3')
        pygame.mixer.music.play(-1, 0)  # 背景音乐循环播放
        background.showGameOverScreen()
        pygame.mixer.music.stop()