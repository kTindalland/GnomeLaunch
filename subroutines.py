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
        pygame.display.set_caption('Gnome Launch - Main Menu')

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

        pygame.display.flip()
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

    print(type(colourPackage[0].keys()))

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

# Instead of displaying text it draws a picture
class PicButton(Button):
    def assignDrawFunc(self, func):
        self.drawFunc = func

    def draw(self, scheme):
        self.rectDraw(scheme, '')
        self.drawFunc(self.screen, scheme, self.position, self.dimensions)
