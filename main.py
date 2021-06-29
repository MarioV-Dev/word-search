import random
import string
import pygame

pygame.init()

win = pygame.display.set_mode((752, 387))
pygame.display.set_caption("Word Search")
clock = pygame.time.Clock()

words = []
wordsSpotted = []

wordsText = []
highlightedLetters = []
highlightedGrid = []
revealedLetters = []

grid = []

rows = 10
columns = 10

#print(pygame.font.get_fonts())

wordsFont = pygame.font.SysFont("cambria", 40)
alphabet = string.ascii_lowercase

def createWordsText():
    wordsText.clear()
    num = 0
    for word in words:
        color = (0, 0, 0)
        num +=1
        if word in wordsSpotted:
            color = (105, 105, 105)
        text = wordsFont.render(str(num) + ". " + word, 1, color)
        wordsText.append(text)

def drawWords():
    x = 450
    y = -38
    for word in wordsText:
        y +=40
        win.blit(word, (x, y))

def generateWords(count = 10):
    wordListFile = open('wordList.txt')
    wordListContent = wordListFile.readlines()

    for i in range(count):
        getRandomWord(wordListContent)

    wordListFile.close()

def getRandomWord(wordList):
    word = random.choice(wordList).strip()
    word = word.lower()
    if len(word) > rows and len(word) > columns:
        getRandomWord(wordList)
    elif word in words:
        getRandomWord(wordList)
    else:
        words.append(word)


def createGrid():
    x = -40
    width = 35
    height = 35

    for row in range(rows):
        x += 39
        y = -40
        tempList = []

        grid.append(tempList)
        for column in range(columns):
            y += 39
            randomLetter = random.choice(alphabet)
            Button = button((255, 255, 255), x, y, width, height, randomLetter)
            grid[row].append(Button)

def addWordsToGrid(wordsToAdd):
    for r in range(rows):
        for c in range(columns):
            grid[r][c].locked = False

    newWords = []
    newWords.clear()
    for word in wordsToAdd:
        newWords.append(word)
    addToGrid(newWords, 0)

def addToGrid(wordsToAdd, count):
    if count < len(wordsToAdd):
        freeSpace = []
        for r in range(rows):
            for c in range(columns):
                if grid[r][c].locked is False:
                    freeSpace.append((r, c))

        if ifAblePlaceWordRandomly(freeSpace, wordsToAdd[count]):
            count +=1
        else:
            grid.clear()
            createGrid()
            count = 0
        addToGrid(wordsToAdd, count)

def ifSpaceOnGridForWord(freeSpace, word):
    for cord in freeSpace:
        if canGoLeft(word, cord[0], cord[1]):
            return True

        elif canGoUp(word, cord[0], cord[1]):
            return True

        elif canGoDown(word, cord[0], cord[1]):
            return True

        elif canGoRight(word, cord[0], cord[1]):
            return True
    return False

def ifAblePlaceWordRandomly(freeSpace, word):
    randomCord = random.choice(freeSpace)
    freeSpace.remove(randomCord)

    if canGoLeft(word, randomCord[0], randomCord[1]):
        placeLeft(word, randomCord[0], randomCord[1])
        return True

    elif canGoUp(word, randomCord[0], randomCord[1]):
        placeUp(word, randomCord[0], randomCord[1])
        return True

    elif canGoDown(word, randomCord[0], randomCord[1]):
        placeDown(word, randomCord[0], randomCord[1])
        return True

    elif canGoRight(word, randomCord[0], randomCord[1]):
        placeRight(word, randomCord[0], randomCord[1])
        return True
    elif len(freeSpace) == 0:
        return False
    return ifAblePlaceWordRandomly(freeSpace, word)

def canGoDown(word, row, column):
    for x in range(len(word) - 1):
        column += 1
        if column >= columns:
            return False
        if grid[row][column] is None:
            return False
        if grid[row][column].locked is True:
            return False

    return True

def canGoUp(word, row, column):
    for x in range(len(word) - 1):
        column -= 1
        if column < 0:
            return False
        if grid[row][column] is None:
            return False
        if grid[row][column].locked is True:
            return False

    return True

def canGoRight(word, row, column):
    for x in range(len(word) - 1):
        row +=1
        if row >= rows:
            return False
        if grid[row][column] is None:
            return False
        if grid[row][column].locked is True:
            return False

    return True

def canGoLeft(word, row, column):
    for x in range(len(word) - 1):
        row -=1
        if row < 0:
            return False
        if grid[row][column] is None:
            return False
        if grid[row][column].locked is True:
            return False

    return True

def placeLeft(word, row, column):
    for x in range(len(word)):
        grid[row][column].locked = True
        grid[row][column].changeText(word[x])
        row -=1

def placeUp(word, row, column):
    for x in range(len(word)):
        grid[row][column].locked = True
        grid[row][column].changeText(word[x])
        column -=1

def placeDown(word, row, column):
    for x in range(len(word)):
        grid[row][column].locked = True
        grid[row][column].changeText(word[x])
        column +=1

def placeRight(word, row, column):
    for x in range(len(word)):
        grid[row][column].locked = True
        grid[row][column].changeText(word[x])
        row +=1

def isHorizontal(buttons):
    if len(buttons) < 1:
        return
    previous = buttons[0]

    for item in buttons:
        if item.x != previous.x:
            return False
        previous = item
    return True

def isVertical(buttons):
    if len(buttons) < 1:
        return
    previous = buttons[0]

    for item in buttons:
        if item.y != previous.y:
            return False
        previous = item
    return True

def isConsecutiveVertical(buttons):
    if len(buttons) < 1:
        return False

    yCordinates = []
    min = buttons[0][1]
    max = buttons[0][1]

    for item in buttons:
        yCordinates.append(item[1])
        if item[1] > max:
            max = item[1]
        if item[1] < min:
            min = item[1]

    for i in range(len(yCordinates)):
        if min not in yCordinates:
            return False
        min += 1

    return True

def isConsecutiveHorizontal(buttons):
    if len(buttons) < 1:
        return False
    xCordinates = []
    min = buttons[0][0]
    max = buttons[0][0]
    for item in buttons:
        xCordinates.append(item[0])
        if item[0] > max:
            max = item[0]
        if item[0] < min:
            min = item[0]

    for i in range(len(xCordinates)):
        if min not in xCordinates:
            return False
        min += 1
    return True

class button():
    def __init__(self, color, x, y, width, height, text='', locked=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.locked = locked

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('cambria', 33)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    def changeText(self, newText):
        self.text = newText

def newPuzzle():
    win.fill((255, 255, 255))
    words.clear()
    wordsSpotted.clear()
    wordsText.clear()
    highlightedLetters.clear()
    revealedLetters.clear()
    grid.clear()

    createGrid()
    generateWords(7)
    createWordsText()
    addWordsToGrid(words)
    drawWords()

def redrawGameWindow():
    newGameButton.draw(win, (0, 0, 0))
    for r in range(rows):
        for c in range(columns):
            grid[r][c].draw(win, (0, 0, 0))
    pygame.display.update()

def isInWords(listOfButtons):
    listOfLetters = []
    for item in listOfButtons:
        listOfLetters.append(item.text)

    for word in words:
        if len(word) == len(listOfLetters):
            for x in range(len(listOfLetters)):
                if listOfLetters[x] in word:
                    if x == len(listOfLetters) - 1:
                        wordsSpotted.append(word)
                        createWordsText()
                        return True
                else:
                    break
    return False


win.fill((255, 255, 255))
createGrid()
generateWords(7)
createWordsText()
addWordsToGrid(words)
drawWords()
newGameButton = button((0, 255, 0), 500, 320, 85, 50, 'New')
run = True
dragging = False

while run:
    clock.tick(30)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if newGameButton.isOver(pos):
                newPuzzle()

            dragging = True
            for r in range(rows):
                for c in range(columns):
                    if grid[r][c].isOver(pos):
                        grid[r][c].color = (255, 255, 0)
                        if grid[r][c] not in highlightedLetters and grid[r][c] not in revealedLetters:
                            highlightedLetters.append(grid[r][c])
                            highlightedGrid.append((r, c))

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

            if not isHorizontal(highlightedLetters) and not isConsecutiveHorizontal(highlightedGrid):
                for x in highlightedLetters:
                    x.color = (255, 255, 255)

            elif not isVertical(highlightedLetters) and not isConsecutiveVertical(highlightedGrid):
                for x in highlightedLetters:
                    x.color = (255, 255, 255)

            elif not isInWords(highlightedLetters):
                for x in highlightedLetters:
                    x.color = (255, 255, 255)
            else:
                for item in highlightedLetters:
                    revealedLetters.append(item)
                    win.fill((255, 255, 255))
                    drawWords()
            highlightedLetters.clear()
            highlightedGrid.clear()

        if event.type == pygame.MOUSEMOTION:

            if newGameButton.isOver(pos):
                newGameButton.color = (255, 255, 0)
            else:
                newGameButton.color = (0, 255, 0)

            for r in range(rows):
                for c in range(columns):
                    if grid[r][c].isOver(pos) and dragging:
                        grid[r][c].color = (255, 255, 0)
                        if grid[r][c] not in highlightedLetters and grid[r][c] not in revealedLetters:
                            highlightedLetters.append(grid[r][c])
                            highlightedGrid.append((r, c))

    redrawGameWindow()

pygame.quit()
