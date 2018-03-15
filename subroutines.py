# Gnome Launch
# Subroutines

import csv, pygame, math

def importRawSettings(filename='settings.csv'):
    # Read and return raw settings data from the settings file.
    try:
        file = open(filename, 'r')

    except:
        print("An error has occured in importRawSettings")
        return False

    else:
        reader = csv.reader(file)
        settings = []
        for row in reader:
            settings.append(row)

        file.close()
        return settings


def hexcodeToRGB(hexcode):
    RGBCol = []
    for i in range(0, 5, 2):
        RGBCol.append(int(hexcode[i:i+2], 16))
    return RGBCol

def RGBToHexcode(*args):
    hexcode = ''
    for col in args:
        newSection = hex(col)[2:]
        if len(newSection) < 2:
            newSection = '0' + newSection
        hexcode += newSection
    return hexcode

def parseSettings(settings):
    for line in settings:
        if line[0] == 'colour schemes':
            colSettings = settings[settings.index(line):settings.index(line)+int(line[1])+1]
            colourPackage = parseColourSchemes(colSettings)

    return colourPackage


def parseColourSchemes(colSettings):
    schemes = {}
    titles = ['background', 'outline', 'on', 'off', 'text']
    reservedNames = ['colour schemes']
    for scheme in colSettings[1:]:
        if scheme[0] not in reservedNames:
            schemes[scheme[0]] = {}
            for index, colour in enumerate(scheme[1:]):
                schemes[scheme[0]][titles[index]] = hexcodeToRGB(colour)
            reservedNames.append(scheme[0])
    return [schemes, colSettings[0][2]]


def startupPygame(caption='Gnome Launch', size=[700,500]):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return [screen, clock]


def startMenu(font):

    screen, clock = startupPygame('Gnome Launch - Start Menu')

    done = False

    coords = generateMainBlockCoords([700, 500], ['NasalizationRg-Regular', 50, 'GNOME LAUNCH'], [3, 180, 50])
    buttonNames = ['Tutorials', 'Level Designer', 'Load Level']
    buttons = generateButtons(screen, font, coords[1:], buttonNames, [180, 50])

    settingsButton = PicButton(screen, font, [640, 10], [50,50])
    settingsButton.assignDrawFunc(drawGear)


    while not done:
        for e in pygame.event.get():
            for key, value in buttons.items():
                value.detect(e)
            settingsButton.detect(e)
            if e.type == pygame.QUIT:
                pygame.quit()

        # Import settings
        rawSettings = importRawSettings('settings.csv')
        colourPackage = parseSettings(rawSettings)
        defaultColourScheme = colourPackage[1]
        scheme = colourPackage[0][defaultColourScheme]

        # Reset caption after other screens have been visited
        pygame.display.set_caption('Gnome Launch - Start Menu')

        # Fill screen
        screen.fill(scheme['background'])

        # Draw text
        drawTitle(screen, scheme, coords[0], 'NasalizationRg-Regular', 50, 'GNOME LAUNCH')
        drawCredits(screen, scheme, font, [5, 470])

        # Draw buttons
        for key, value in buttons.items():
            value.draw(scheme, key)
        settingsButton.draw(scheme)

        # Button Logic
        if settingsButton.state:
            settingsScreen(font, screen, clock)
            settingsButton.state = False

        if buttons['Level Designer'].state:
            levelDesigner(font)
            buttons['Level Designer'].state = False

        pygame.display.flip()
        screen, clock = startupPygame('Gnome Launch - Start Menu')
        clock.tick(60)


def generateMainBlockCoords(screensize, titleParams, buttonParams, offset=[0,0]): # titleParams = [fontName, size, title], buttonParams = [numberOfButtons, width, height]
    titleFont = pygame.font.SysFont(titleParams[0], titleParams[1], False, True)
    renderedTitle = titleFont.render(titleParams[2], True, (0,0,0)) # Doesn't matter what colour as it won't be drawn. Only needed for measurements.
    titleHeight, titleWidth = renderedTitle.get_height(), renderedTitle.get_width()

    padding = 50

    totalHeight = titleHeight + (buttonParams[0] * buttonParams[2]) + (buttonParams[0] * padding)

    startingY = (screensize[1]//2) - (totalHeight//2) - offset[1]

    coordList = []
    for count in range(buttonParams[0]+1):
        coord = [(screensize[0]//2) - (buttonParams[1]//2) + offset[0], startingY+titleHeight+(buttonParams[2]*(count-1))+(padding*(count-1))]
        if count == 0:
            coord = [(screensize[0]//2) - (titleWidth//2) + offset[0], startingY]
        coordList.append(coord)

    return coordList

def drawTitle(screen, scheme, position, fontName, size, title):
    font = pygame.font.SysFont(fontName, size, False, True)
    renderedTitle = font.render(title, True, scheme['text'])
    screen.blit(renderedTitle, position)

def generateButtons(screen, font, coords, names, dimensions):
    buttons = {}
    for index, buttonName in enumerate(names):
        buttons[buttonName] = Button(screen, font, coords[index], dimensions)
    return buttons

def drawCredits(screen, scheme, font, position):
    credits = "Written by Kai Tindall"
    credits = font.render(credits, True, scheme['text'])
    screen.blit(credits, position)


# Draws the gear (used for settings symbol)
def drawGear(screen, scheme, position, dimensions):
    # Assumes the button is square
    # Assign vars
    centre = [int(position[0]+(dimensions[0]//2)), int(position[1]+(dimensions[1]//2))] # Centre of the button
    gearRad = int(dimensions[0] * 0.4)
    outerRad = int(dimensions[0] * 0.6) // 2
    innerRad = int(dimensions[0] * 0.3) // 2
    cornerRad = int(dimensions[0] * 0.1)
    rectWidth = math.sqrt((cornerRad**2)*2)

    # Draw outer circle
    pygame.draw.circle(screen, scheme['text'], centre, outerRad)

    # Draw straight rects
    # Vertical
    pygame.draw.rect(screen, scheme['text'], [centre[0] - rectWidth//2, centre[1] - gearRad, rectWidth, gearRad * 2])
    # Horizontal
    pygame.draw.rect(screen, scheme['text'], [centre[0] - gearRad, centre[1] - rectWidth//2, gearRad * 2, rectWidth])

    # Draw polygons
    # Top Right -> Bottom Left
    degs = 45 * (math.pi / 180)
    barRad = int(math.cos(degs) * gearRad)
    diff = int(rectWidth / 2 / math.sqrt(2))
    # points go clockwise
    one   = [centre[0] + barRad - diff, centre[1] - barRad - diff]
    two   = [centre[0] + barRad + diff, centre[1] - barRad + diff]
    three = [centre[0] - barRad + diff, centre[1] + barRad + diff]
    four  = [centre[0] - barRad - diff, centre[1] + barRad - diff]
    pygame.draw.polygon(screen, scheme['text'], [one, two, three, four])

    # Top Left -> Bottom Right
    # points go clockwise
    one   = [centre[0] - barRad + diff, centre[1] - barRad - diff]
    two   = [centre[0] + barRad + diff, centre[1] + barRad - diff]
    three = [centre[0] + barRad - diff, centre[1] + barRad + diff]
    four  = [centre[0] - barRad - diff, centre[1] - barRad + diff]
    pygame.draw.polygon(screen, scheme['text'], [one, two, three, four])

    # Draw inner circle
    pygame.draw.circle(screen, scheme['off'], centre, innerRad)

def settingsScreen(font, screen, clock):
    done = False

    pygame.display.set_caption('Gnome Launch - Settings Screen')
    rawSettings = importRawSettings('settings.csv')
    colourPackage = parseSettings(rawSettings)
    defaultColourScheme = colourPackage[1]
    scheme = colourPackage[0][defaultColourScheme]

    colSchemeTextCoords, colSchemeButtons = genColourSchemeSettings(screen, scheme, font, [10,50], [100, 40], colourPackage)

    backButton = Button(screen, font, [590, 10], [100, 40])

    while not done:
        for e in pygame.event.get():
            backButton.detect(e)

            for key, value in colSchemeButtons.items():
                if value.detect(e):
                    for key2, value2 in colSchemeButtons.items():
                        value2.state = False
                    value.state = True
                    newSchemeName, colourPackage = changeColPackage(key, colourPackage)
                    scheme = colourPackage[0][newSchemeName]

            if e.type == pygame.QUIT:
                pygame.quit()

        screen.fill(scheme['background'])
        backButton.draw(scheme, 'Back')
        if backButton.state:
            done = True
            backButton.state = False

        drawText(screen, scheme, font, 'Colour scheme:', colSchemeTextCoords) # Draws colScheme label

        for key, value in colSchemeButtons.items():
            value.draw(scheme, key)


        pygame.display.flip()
        clock.tick(60)
    writeSettings(colourPackage)

def genColourSchemeSettings(screen, scheme, font, position, buttonSize, colourPackage):
    text = font.render('Colour scheme:', True, scheme['text']) # For measuring purposes.
    text_width, text_height = text.get_width(), text.get_height()
    padding = 10

    textCoords = [position[0], position[1]-(text_height//2)]
    buttons = {}

    keys = [] # Keeps the colour schemes in alphabetical order
    for key, value in sorted(colourPackage[0].items()):
        keys.append(key)

    for index, name in enumerate(keys):
        buttonCoords = [position[0]+text_width+(padding*(index+1))+(buttonSize[0]*index), position[1]-(buttonSize[1]//2)]
        buttons[name] = Button(screen, font, buttonCoords, buttonSize)
        if name == colourPackage[1]:
            buttons[name].state = True

    return textCoords, buttons

def drawText(screen, scheme, font, theString, coords):
    text = font.render(theString, True, scheme['text'])
    screen.blit(text, coords)

def changeColPackage(newScheme, oldColourPackage):
    oldColourPackage[1] = newScheme
    return newScheme, oldColourPackage

def writeSettings(colourPackage):
    colSchemeLines = writeColSchemes(colourPackage)
    with open('settings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for line in colSchemeLines:
            writer.writerow(line)

def writeColSchemes(colourPackage):
    lines = [['colour schemes', len(colourPackage[0]), colourPackage[1]]]
    for schemeName, scheme in colourPackage[0].items():
        # [Name, Background, Outline, On, Off, Text]
        newLine = [schemeName]
        elements = ['background', 'outline', 'on', 'off', 'text']
        for element in elements:
            colour = scheme[element]
            newLine.append(RGBToHexcode(colour[0], colour[1], colour[2]))
        lines.append(newLine)
    return lines

def levelDesigner(font):
    levelEntities = {
        'Gravity Well' : [],
        'Player Area'  : None,
        'Goal Area'    : None,
        'Wall'         : [],
    }
    done = False
    screensize = [950, 550]
    screen, clock = startupPygame('', screensize)

    backButton = Button(screen, font, [550,5], [125, 40])
    button1 = Button(screen, font, [25, 5], [125, 40])
    button2 = Button(screen, font, [200, 5], [125, 40])
    button3 = Button(screen, font, [375, 5], [125, 40])

    Y = 45 # Y displacement for toolbox
    names = ['Player Area', 'Gravity Well', 'Goal Area', 'Wall']
    toolboxCoords = [[725, Y+((50+30)*i)] for i in range(len(names))]
    toolboxButtons = createToolboxButtons(screen, font, toolboxCoords, names, [200, 50])

    testPlayer = Player(screen, 1, [100, 100], [0.45, -0.1], [0, 50, 700, 550])
    testWell = Well(screen, [250, 200], 10, 1000000000000)
    drawTest = False

    ts = LabelToggleSwitch(screen, font, [725,550-50-25], [200, 50], 0)

    pygame.display.set_caption('Gnome Launch - Level Designer')
    rawSettings = importRawSettings('settings.csv')
    colourPackage = parseSettings(rawSettings)
    defaultColourScheme = colourPackage[1]
    scheme = colourPackage[0][defaultColourScheme]

    while not done:
        for e in pygame.event.get():
            ts.detect(e)
            if backButton.detect(e):
                done = True

            for key, value in toolboxButtons.items():
                if value.detect(e):
                    for keyB, valueB in toolboxButtons.items():
                        valueB.state = False
                    value.state = True

            if e.type == pygame.QUIT:
                pygame.quit()

            if not ts.state and e.type == pygame.MOUSEBUTTONDOWN: # If drawing
                mpos = pygame.mouse.get_pos()
                if 0 <= mpos[0] <= 700 and 50 <= mpos[1] <= 550: # If in game space
                    for key, value in toolboxButtons.items():
                        if value.state:
                            print(key)
                            if key == 'Gravity Well': # If Gravity Well selected
                                temp = Well(screen, mpos, 10, 10**12)
                                levelEntities[key].append(temp)
                            if key == 'Player Area':
                                levelEntities = checkAreas(key, screen, PlayerArea, levelEntities)
                            if key == 'Goal Area':
                                levelEntities = checkAreas(key, screen, GoalArea, levelEntities)
                            if key == 'Wall':
                                if not Wall.isDrawing:
                                    mpos = pygame.mouse.get_pos()
                                    levelEntities[key].append(Wall(screen, mpos))
                                    Wall.isDrawing = True
                                else:
                                    mpos = pygame.mouse.get_pos()
                                    levelEntities[key][-1] = Wall(screen, levelEntities[key][-1].origin, mpos)
                                    Wall.isDrawing = False



        screen.fill(scheme['background'])
        backButton.draw(scheme, 'Back')
        button1.draw(scheme, 'Button1')
        button2.draw(scheme, 'Button2')
        button3.draw(scheme, 'Button3')
        drawGuideLines(screen, scheme)


        # Testing instances.
        if drawTest:
            testPlayer.draw(scheme)
            testWell.draw(scheme, testPlayer)
        ts.draw(scheme, ['Draw', 'Select'])

        # Draw toolbox title
        drawToolbarTitle(screen, font, scheme)

        # Draw toolbox buttons
        for key, value in toolboxButtons.items():
            value.draw(scheme, key)

        if len(levelEntities['Gravity Well']) > 0:
            for i in levelEntities['Gravity Well']:
                i.draw(scheme, None)

        if levelEntities['Player Area'] != None:
            levelEntities['Player Area'].draw(scheme)

        if levelEntities['Goal Area'] != None:
            levelEntities['Goal Area'].draw(scheme)

        if len(levelEntities['Wall']) > 0:
            for i in levelEntities['Wall']:
                i.draw(scheme)

        pygame.display.flip()
        clock.tick(60)


def drawGuideLines(screen, scheme):
    pygame.draw.line(screen, scheme['outline'], [700, 0], [700, 550], 2)
    pygame.draw.line(screen, scheme['outline'], [0, 50], [700, 50], 2)
    pygame.draw.rect(screen, scheme['outline'], [0,0, 950, 550], 2)


def drawToolbarTitle(screen, font, scheme):
    font.set_underline(True)
    title = font.render('Toolbox', True, scheme['text']) # Draw Pannel, Toolbox, Select Tool
    width = title.get_width()
    font.set_underline(False)
    startX, spaceWidth = 700, 250
    screen.blit(title, [startX + ((spaceWidth//2)-(width//2)), 10])


def createToolboxButtons(screen, font, coords, names, dimensions):
    buttons = {}
    for index, name in enumerate(names):
        buttons[name] = Button(screen, font, coords[index], dimensions)
        if not index:
            buttons[name].state = True
    return buttons


def checkAreas(key, screen, selectedClass, levelEntities):
    if not selectedClass.isDrawing:
        mpos = pygame.mouse.get_pos()
        levelEntities[key] = selectedClass(screen, mpos)
        selectedClass.isDrawing = True
    else:
        mpos = pygame.mouse.get_pos()
        levelEntities[key] = selectedClass(screen, levelEntities[key].origin, mpos)
        selectedClass.isDrawing = False
    return levelEntities

class Button():
    def __init__(self, screen, font, position, dimensions):
        self.screen, self.font, self.position, self.dimensions = screen, font, position, dimensions
        self.state = False

        def rect(mousepos):
            if self.position[0] <= mousepos[0] <= (self.position[0] + self.dimensions[0]):
                if self.position[1] <= mousepos[1] <= (self.position[1] + self.dimensions[1]):
                    return True
            return False

        def circ(mousepos):
            dx, dy = self.position[0] - mousepos[0], self.position[1] - mousepos[1]
            if dx ** 2 + dy ** 2 <= self.dimensions ** 2:
                return True
            return False

        if type(dimensions) is list:
            self.equation = rect
            self.correctDraw = self.rectDraw
        else:
            self.equation = circ
            self.correctDraw = self.circDraw

    def detect(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.equation(pygame.mouse.get_pos()):
                self.state = not self.state
                return True
        return False

    def rectDraw(self, scheme, label):
        drawCol = scheme['off']
        if self.state:
            drawCol = scheme['on']

        # Draw rectangles
        pygame.draw.rect(self.screen, drawCol, [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]])
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]], 3)

        # Draw label
        if label != '' and type(label) is str:
            text = self.font.render(label, True, scheme['text'])
            width, height = text.get_width() // 2, text.get_height() // 2
            self.screen.blit(text, [self.position[0]+(self.dimensions[0]//2)-width, self.position[1]+(self.dimensions[1]//2)-height])

    def circDraw(self, scheme, label):
        drawCol = scheme['off']
        if self.state:
            drawCol = scheme['on']

        # Draw rectangles
        pygame.draw.circle(self.screen, drawCol, self.position, self.dimensions)
        pygame.draw.circle(self.screen, scheme['outline'], self.position, self.dimensions, 3)

        # Draw label
        if label != '' and type(label) is str:
            text = self.font.render(label, True, scheme['text'])
            width, height = text.get_width() // 2, text.get_height() // 2
            self.screen.blit(text, [self.position[0]-width, self.position[1]-height])

    def draw(self, scheme, label=''):
        self.correctDraw(scheme, label)

    def identity(self):
        return 'Button'

# Instead of displaying text it draws a picture
class PicButton(Button):
    def assignDrawFunc(self, func):
        self.drawFunc = func

    def draw(self, scheme):
        self.rectDraw(scheme, '')
        self.drawFunc(self.screen, scheme, self.position, self.dimensions)

    def identity(self):
        return 'PicButton'

class Player():
    def __init__(self, screen, mass, startCoords, vectorComps, range=[0,0,700,500]):
        self.screen, self.coords, self.vComps = screen, startCoords, vectorComps
        self.range, self.mass = range, mass

    def draw(self, scheme):
        pygame.draw.circle(self.screen, scheme['text'], [int(self.coords[0]), int(self.coords[1])], 5)
        self.move()

    def move(self):
        self.coords = [self.coords[0]+self.vComps[0], self.coords[1]+self.vComps[1]]
        self.check()

    def check(self):
        if self.coords[0] < self.range[0]:
            self.coords[0] = self.range[0]
            self.vComps[0] *= -1
        if self.coords[1] < self.range[1]:
            self.coords[1] = self.range[1]
            self.vComps[1] *= -1
        if self.coords[0] > self.range[2]:
            self.coords[0] = self.range[2]
            self.vComps[0] *= -1
        if self.coords[1] > self.range[3]:
            self.coords[1] = self.range[3]
            self.vComps[1] *= -1

    def identity(self):
        return 'Player'


class Well():
    def __init__(self, screen, position, size, mass):
        self.screen, self.position, self.mass = screen, position, mass
        self.size = size

    def draw(self, scheme, player):
        pygame.draw.circle(self.screen, scheme['text'], self.position, self.size)
        if player != None:
            self.calc(player)

    def calc(self, player):
        dx = abs(self.position[0] - player.coords[0])
        dy = abs(self.position[1] - player.coords[1])
        theta = math.atan(dy/dx)

        G = 6.67 * (10**-11)
        r = math.sqrt((dx**2)+(dy**2))
        if r < self.size:
            r = self.size

        g = (-G*self.mass)/(r**2)
        Fx = g*math.cos(theta)
        Fy = g * math.sin(theta)

        ax = abs(Fx / player.mass)
        ay = abs(Fy / player.mass)

        # Check where player is in relation to well
        # Is player below
        if player.coords[1] > self.position[1]:
            ay *= -1
        # Is player to the right
        if player.coords[0] > self.position[0]:
            ax *= -1

        player.vComps[0] += ax
        player.vComps[1] += ay

    def identity(self):
        return 'Well'


class ToggleSwitch():
    def __init__(self, screen, font, position, dimensions, default):
        self.screen, self.font, self.position, self.dimensions, self.state = screen, font, position, dimensions, default
        self.blockWidth = self.dimensions[0] * 0.4
        self.blockEnds = [0, self.dimensions[0] * 0.6]
        self.goal = self.blockEnds[self.state]
        self.blockX = self.goal
        self.speed = 7


    def draw(self, scheme):
        pygame.draw.rect(self.screen, scheme['on'], [self.position[0]+ self.blockX, self.position[1], self.blockWidth, self.dimensions[1]])
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0] + self.blockX, self.position[1], self.blockWidth, self.dimensions[1]], 3)
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]], 3)
        self.move()


    def detect(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if self.position[0] <= mpos[0] <= (self.position[0]+self.dimensions[0]):
                if self.position[1] <= mpos[1] <= (self.position[1] + self.dimensions[1]):
                    if self.state:
                        self.state = 0
                    else:
                        self.state = 1
                    self.goal = self.blockEnds[self.state]


    def move(self):
        if self.goal != self.blockX:
            temp = self.goal - self.blockX
            change = temp // abs(temp)
            change *= self.speed
            # Need to validate coords.
            self.blockX += change
            if self.blockX < self.blockEnds[0]:
                self.blockX = self.blockEnds[0]
            if self.blockX > self.blockEnds[1]:
                self.blockX = self.blockEnds[1]

    def identity(self):
        return 'ToggleSwitch'

class LabelToggleSwitch(ToggleSwitch):
    def draw(self, scheme, labels=['On', 'Off']):
        super().draw(scheme)
        leftText = self.font.render(labels[0], True, scheme['off'])
        rightText = self.font.render(labels[1], True, scheme['off'])
        if self.state:
            rightText = self.font.render(labels[1], True, scheme['on'])
        else:
            leftText = self.font.render(labels[0], True, scheme['on'])
        leftWidth, leftHeight = leftText.get_width(), leftText.get_height()
        rightWidth, rightHeight = rightText.get_width(), rightText.get_height()
        self.screen.blit(leftText, [self.blockEnds[0]+self.position[0]+5, self.position[1]-leftHeight-5])
        self.screen.blit(rightText, [self.position[0]+self.dimensions[0]-rightWidth-5, self.position[1]-rightHeight-5])

    def identity(self):
        return 'LabelToggleSwitch'

class Area():
    isDrawing = False
    def __init__(self, screen, cornerOne, cornerTwo=None):
        self.screen = screen
        self.origin = cornerOne
        self.drawAtMouse = False
        if cornerTwo != None:
            self.dx, self.dy = cornerTwo[0] - cornerOne[0], cornerTwo[1] - cornerOne[1]
        else:
            self.drawAtMouse = True

    def draw(self):
        if self.drawAtMouse:
            cornerTwo = pygame.mouse.get_pos()
            self.dx, self.dy = cornerTwo[0] - self.origin[0], cornerTwo[1] - self.origin[1]

    def detect(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            pass

    def identity(self):
        return 'Area'

class PlayerArea(Area):
    def draw(self, scheme):
        super().draw()
        pygame.draw.rect(self.screen, scheme['off'], [self.origin[0], self.origin[1], self.dx, self.dy], 3)

    def identity(self):
        return 'PlayerArea'

class GoalArea(Area):
    def draw(self, scheme):
        super().draw()
        pygame.draw.rect(self.screen, scheme['on'], [self.origin[0], self.origin[1], self.dx, self.dy], 3)

    def identity(self):
        return 'GoalArea'

class Wall(Area):
    def draw(self, scheme):
        super().draw()
        pygame.draw.rect(self.screen, scheme['outline'], [self.origin[0], self.origin[1], self.dx, self.dy])