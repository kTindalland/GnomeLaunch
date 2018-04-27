# Gnome Launch
# Subroutines

import csv, pygame, math
import sqlite3 as sql
from textbox import Textbox

def importRawSettings(filename='settings.csv'):
    # Read and return raw settings data from the settings file.
    try:
        file = open(filename, 'r')

    except:
        print("An error has occured in importRawSettings") # This is to aid with future maintenance
        return False

    else:
        reader = csv.reader(file)
        settings = []
        for row in reader:
            settings.append(row)

        file.close()
        return settings


def hexcodeToRGB(hexcode): # for reading in a hexcode
    RGBCol = []
    for i in range(0, 5, 2):
        RGBCol.append(int(hexcode[i:i+2], 16))
    return RGBCol

def RGBToHexcode(*args): # for writing to database
    hexcode = ''
    for col in args:
        newSection = hex(col)[2:]
        if len(newSection) < 2:
            newSection = '0' + newSection
        hexcode += newSection
    return hexcode

def parseSettings(settings): # This takes in raw settings and then spits out formatted settings
    for line in settings:
        if line[0] == 'colour schemes':
            colSettings = settings[settings.index(line):settings.index(line)+int(line[1])+1]
            colourPackage = parseColourSchemes(colSettings)

    return colourPackage


def parseColourSchemes(colSettings):
    schemes = {}
    titles = ['background', 'outline', 'on', 'off', 'text'] # All titles of colours
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

    coords = generateMainBlockCoords([700, 500], ['NasalizationRg-Regular', 50, 'GNOME LAUNCH'], [3, 180, 50]) # First number in final arg is how many buttons you have, this may be an issue for future maintenance
    buttonNames = ['Tutorials', 'Level Designer', 'Load Level'] # The names in here are what buttons get generated
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

        # If Level designer clicked
        if buttons['Level Designer'].state:
            levelDesigner(font)
            buttons['Level Designer'].state = False

        # If load button clicked
        if buttons['Load Level'].state:
            loadScreen(font, scheme)
            buttons['Load Level'].state = False


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

def drawTitle(screen, scheme, position, fontName, size, title): # Mainly used for main menu
    font = pygame.font.SysFont(fontName, size, False, True)
    renderedTitle = font.render(title, True, scheme['text'])
    screen.blit(renderedTitle, position)

def generateButtons(screen, font, coords, names, dimensions): # Called in main menu
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

    # Setup settings and change caption
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

def drawText(screen, scheme, font, theString, coords): # General draw text function
    text = font.render(theString, True, scheme['text'])
    screen.blit(text, coords)

def changeColPackage(newScheme, oldColourPackage):
    oldColourPackage[1] = newScheme
    return newScheme, oldColourPackage

def writeSettings(colourPackage): # Write settings back into file
    colSchemeLines = writeColSchemes(colourPackage) # Outsource col schemes to seperate function
    with open('settings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for line in colSchemeLines:
            writer.writerow(line)

def writeColSchemes(colourPackage): # Format the settings back to a usable format
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
    # This is the dictionary that holds all the level objects.
    levelEntities = {
        'Gravity Well' : [],
        'Player Area'  : None,
        'Goal Area'    : None,
        'Wall'         : [],
    }
    done = False
    screensize = [950, 550]
    # Sets up a new screen because it needs a new screensize.
    screen, clock = startupPygame('', screensize)

    backButton = Button(screen, font, [550,5], [125, 40])
    button1 = Button(screen, font, [25, 5], [125, 40])
    button2 = Button(screen, font, [200, 5], [125, 40])
    saveButton = Button(screen, font, [375, 5], [125, 40])

    Y = 45 # Y displacement for toolbox
    names = ['Player Area', 'Gravity Well', 'Goal Area', 'Wall'] # However many names are in the list is how many are generated
    toolboxCoords = [[725, Y+((50+30)*i)] for i in range(len(names))]
    toolboxButtons = createToolboxButtons(screen, font, toolboxCoords, names, [200, 50]) # Creates buttons for the right hand toolbar

    testPlayer = Player(screen, 1, [100, 100], [0.45, -0.1], [0, 50, 700, 550]) # Purely for testing
    testWell = Well(screen, font, [250, 200], 10, 1000000000000)
    drawTest = False # If false then the two test objects are not drawn

    ts = LabelToggleSwitch(screen, font, [725,550-50-25], [200, 50], 0) # Draw / Select swtich

    pygame.display.set_caption('Gnome Launch - Level Designer')
    rawSettings = importRawSettings('settings.csv') # Import settings again
    colourPackage = parseSettings(rawSettings)
    defaultColourScheme = colourPackage[1]
    scheme = colourPackage[0][defaultColourScheme]

    while not done:
        screen, clock = startupPygame('Gnome Launch - Level Designer', screensize)
        for e in pygame.event.get():
            ts.detect(e) # Toggle switch detect
            if backButton.detect(e):
                done = True
            if saveButton.detect(e): # If save button clicked
                saveScreen(font, scheme, levelEntities)
                saveButton.state = False

            for key, value in toolboxButtons.items(): # Toolbox buttons detect
                if value.detect(e):
                    for keyB, valueB in toolboxButtons.items(): # Set all states to false
                        valueB.state = False
                    value.state = True # Set clicked button's state to true

            if e.type == pygame.QUIT:
                pygame.quit()

            mpos = pygame.mouse.get_pos()
            if 0 <= mpos[0] <= 700 and 50 <= mpos[1] <= 550:  # If in game space - validation
                if not ts.state and e.type == pygame.MOUSEBUTTONDOWN: # If drawing
                    for key, value in toolboxButtons.items():
                        if value.state:
                            if key == 'Gravity Well': # If Gravity Well selected
                                temp = Well(screen, font, mpos, 10, 10**12)
                                levelEntities[key].append(temp)
                            if key == 'Player Area': # If player area selected
                                levelEntities = checkAreas(key, screen, PlayerArea, levelEntities)
                            if key == 'Goal Area': # If goal area selected
                                levelEntities = checkAreas(key, screen, GoalArea, levelEntities)
                            if key == 'Wall': # If wall selected
                                if not Wall.isDrawing:
                                    mpos = pygame.mouse.get_pos()
                                    levelEntities[key].append(Wall(screen, mpos))
                                    Wall.isDrawing = True
                                else:
                                    mpos = pygame.mouse.get_pos()
                                    levelEntities[key][-1] = Wall(screen, levelEntities[key][-1].origin, mpos)
                                    Wall.isDrawing = False
                else: # If selecting
                    for i in levelEntities['Gravity Well']:
                        i.detect(e)
                    for i in levelEntities['Wall']:
                        i.detect(e)
                    if levelEntities['Player Area'] != None:
                        levelEntities['Player Area'].detect(e)
                    if levelEntities['Goal Area'] != None:
                        levelEntities['Goal Area'].detect(e)



        screen.fill(scheme['background'])
        backButton.draw(scheme, 'Back')
        button1.draw(scheme, 'Button1')
        button2.draw(scheme, 'Button2')
        saveButton.draw(scheme, 'Save')
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

        selected = False

        if len(levelEntities['Gravity Well']) > 0:
            for i in levelEntities['Gravity Well']:
                if i.TBD:
                    index = levelEntities['Gravity Well'].index(i)
                    del levelEntities['Gravity Well'][index]
                    continue
                if not i.selected:
                    i.draw(scheme, None)
                    continue
                selected = i

        # Drawing and deletion of player area
        if levelEntities['Player Area'] != None:
            levelEntities['Player Area'].draw(scheme)
            if levelEntities['Player Area'].TBD:
                levelEntities['Player Area'] = None

        # Drawing and deletion of goal area
        if levelEntities['Goal Area'] != None:
            levelEntities['Goal Area'].draw(scheme)
            if levelEntities['Goal Area'].TBD:
                levelEntities['Goal Area'] = None

        # Drawing and deletion of walls.
        if len(levelEntities['Wall']) > 0:
            for i in levelEntities['Wall']:
                if i.TBD:
                    index = levelEntities['Wall'].index(i)
                    del levelEntities['Wall'][index]
                    continue
                i.draw(scheme)

        if selected != False: # Making sure selectd is drawn last
            if selected.identity() == 'Well':
                selected.draw(scheme, None)


        pygame.display.flip()
        clock.tick(60)


def drawGuideLines(screen, scheme): # Drawing lines for level designer
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


def createToolboxButtons(screen, font, coords, names, dimensions): # Generates  buttons depending on how many names its given
    buttons = {}
    for index, name in enumerate(names):
        buttons[name] = Button(screen, font, coords[index], dimensions)
        if not index:
            buttons[name].state = True
    return buttons


def checkAreas(key, screen, selectedClass, levelEntities): # Checking for goal area and spawn area
    if not selectedClass.isDrawing:
        mpos = pygame.mouse.get_pos()
        levelEntities[key] = selectedClass(screen, mpos)
        selectedClass.isDrawing = True
    else:
        mpos = pygame.mouse.get_pos()
        levelEntities[key] = selectedClass(screen, levelEntities[key].origin, mpos)
        selectedClass.isDrawing = False
    return levelEntities


def exportLevel(levelName, levelEntities, folderName=None): # this will create the database with all the level data in
    if folderName == None:
        path = levelName + '.db'
    else:
        path = "\\".join(__file__.split("\\")[:-1])
        path += "\\" + folderName + "\\" + levelName
        print(path)
    conn = sql.connect(path)
    cursor = conn.cursor()

    # Execute commands
    cursor.execute("DROP TABLE IF EXISTS gravwells;")
    cursor.execute("DROP TABLE IF EXISTS areas;")
    cursor.execute("CREATE TABLE IF NOT EXISTS gravwells (id INTEGER PRIMARY KEY, x NOT_NULL INTEGER, y NOT_NULL INTEGER, size INTEGER, mass REAL);")
    cursor.execute("CREATE TABLE IF NOT EXISTS areas (id INTEGER PRIMARY KEY, iden TEXT, x1 INTEGER, y1 INTEGER, x2 INTEGER, y2 INTEGER);")

    for well in levelEntities['Gravity Well']:
        cursor.execute("INSERT INTO gravwells (x, y, size, mass) VALUES ({}, {}, {}, {});".format(well.position[0], well.position[1], well.size, float(well.mass)))

    def addArea(area):
        if area != None:
            cursor.execute("INSERT INTO areas (iden, x1, y1, x2, y2) VALUES ({}, {}, {}, {}, {});".format(
                "'"+area.identity()+"'", area.origin[0], area.origin[1], area.origin[0]+area.dx, area.origin[1]+area.dy))
        else:
            cursor.execute("INSERT INTO areas (iden) VALUES (NULL);")

    addArea(levelEntities['Player Area'])
    addArea(levelEntities['Goal Area'])

    for wall in levelEntities['Wall']:
        addArea(wall)

    conn.commit()
    conn.close()

def saveScreen(font, scheme, levelEntities):
    done = False
    screensize = [700, 500]
    screen, clock = startupPygame('Gnome Launch - Save', screensize)

    textbox = Textbox([screen, 0, font], [10, 10], [200, 50], 'Level Name')
    saveButton = Button(screen, font, [220, 15], [100, 40])
    backButton = Button(screen, font, [330, 15], [100, 40])

    while not done:
        for e in pygame.event.get():
            textbox.detect(e)
            if saveButton.detect(e):
                exportLevel(textbox.return_input(), levelEntities)
                done = True
            if backButton.detect(e):
                done = True
            if e.type == pygame.QUIT:
                pygame.quit()

        screen.fill(scheme['background'])
        textbox.draw(scheme)

        saveButton.draw(scheme, 'Save')
        backButton.draw(scheme, 'Back')

        pygame.display.flip()
        clock.tick(60)


def importLevel(screen, font, dbname='default'):
    path = dbname + '.db'
    conn = sql.connect(path)
    cursor = conn.cursor()

    # Execute commands
    cursor.execute("SELECT * FROM gravwells;")
    gravwells = cursor.fetchall()

    cursor.execute("SELECT * FROM areas WHERE iden IS 'PlayerArea'")
    playerArea = cursor.fetchall()
    # Check there is a player area
    if len(playerArea) > 0:
        playerArea = playerArea[0]
    else:
        playerArea = [None, None]

    cursor.execute("SELECT  * FROM areas WHERE iden IS 'GoalArea'")
    goalArea = cursor.fetchall()
    # Check there is a goal area
    if len(goalArea) > 0:
        goalArea = goalArea[0]
    else:
        goalArea = [None, None]

    cursor.execute("SELECT * FROM areas WHERE iden IS 'WallArea'")
    walls = cursor.fetchall()

    conn.commit()
    conn.close()

    levelEntities = {
        'Gravity Well' : [],
        'Player Area'  : None,
        'Goal Area'    : None,
        'Wall'         : [],
    }

    # Format the level entities

    for well in gravwells:
        temp = Well(screen, font, [well[1], well[2]], well[3], well[4])
        levelEntities['Gravity Well'].append(temp)

    if playerArea[1] != None:
        levelEntities['Player Area'] = PlayerArea(screen, [playerArea[2], playerArea[3]], [playerArea[4], playerArea[5]])

    if goalArea[1] != None:
        levelEntities['Goal Area'] = GoalArea(screen, [goalArea[2], goalArea[3]], [goalArea[4], goalArea[5]])

    for wall in walls:
        temp = Wall(screen, [wall[2], wall[3]], [wall[4], wall[5]])
        levelEntities['Wall'].append(temp)

    return levelEntities


def loadScreen(font, scheme):

    done = False
    done2 = False
    screensize = [700, 550]
    screen, clock = startupPygame('Gnome Launch - Load', screensize)

    textbox =  Textbox([screen, 0, font], [10, 10], [200, 50], 'Level Name')
    loadButton = Button(screen, font, [220, 15], [100, 40])
    backButton = Button(screen, font, [330, 15], [100, 40])

    while not done: # First loop - getting filename
        for e in pygame.event.get():
            textbox.detect(e)
            loadButton.detect(e)
            backButton.detect(e)
            if e.type == pygame.QUIT:
                pygame.quit()

        screen.fill(scheme['background'])

        textbox.draw(scheme)
        loadButton.draw(scheme, 'Load')
        backButton.draw(scheme, 'Back')

        if backButton.state:
            done = True
            done2 = True
            backButton.state = False

        if loadButton.state:
            done = True

        pygame.display.flip()
        clock.tick(60)


    # Second loop - actual game.
    levelEntities = importLevel(screen, font, textbox.return_input())

    backButton = Button(screen, font, [590, 5], [100, 40])
    spawnPlayerButton = Button(screen, font, [380, 5], [200, 40])
    player = None

    title = font.render(textbox.return_input(), True, scheme['text'])
    titleHeight = title.get_height()

    while not done2: # Second loop, plays level
        for e in pygame.event.get():
            if backButton.detect(e):
                backButton.state = False
                done2 = True
            spawnPlayerButton.detect(e)
            if e.type == pygame.QUIT:
                pygame.quit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if levelEntities['Player Area'].detect(e):
                    spawner = PlayerSpawner(screen, pygame.mouse.get_pos())
                    PlayerSpawner.isDrawing = True
            if e.type == pygame.MOUSEBUTTONUP and PlayerSpawner.isDrawing:
                spawner.addSecondCoord(pygame.mouse.get_pos())
                player, playerSpeed = spawner.spawn()
                PlayerSpawner.isDrawing = False


        screen.fill(scheme['background'])

        backButton.draw(scheme, 'Menu')
        spawnPlayerButton.draw(scheme, 'Spawn Player')

        screen.blit(title, [10, 25-(titleHeight//2)])

        pygame.draw.line(screen, scheme['outline'], [0,50], [700, 50], 3)
        pygame.draw.rect(screen, scheme['outline'], [0,0,700,550], 3)

        # Draw wells
        for well in levelEntities['Gravity Well']: # Will need to add more logic when player introduced.
            well.draw(scheme, player)

        # Draw areas
        if levelEntities['Player Area'] != None:
            levelEntities['Player Area'].draw(scheme)
        if levelEntities['Goal Area'] != None:
            levelEntities['Goal Area'].draw(scheme)

        # Draw walls
        for wall in levelEntities['Wall']:
            wall.draw(scheme)
            if player != None:
                wall.playerDetect(player)

        # Draw player
        if player != None:
            player.draw(scheme)

        # If spawning player
        if PlayerSpawner.isDrawing:
            mpos = pygame.mouse.get_pos()
            pygame.draw.line(screen, scheme['outline'], spawner.startCoords, mpos, 2)

        # Goal area detection.
        if player != None and levelEntities['Goal Area'] != None:
            if levelEntities['Goal Area'].playerDetect(player.coords):
                done2 = True



        pygame.display.flip()
        clock.tick(60)



class Button():
    def __init__(self, screen, font, position, dimensions):
        self.screen, self.font, self.position, self.dimensions = screen, font, position, dimensions
        self.state = False

        def rect(mousepos): # For rectangular button
            if self.position[0] <= mousepos[0] <= (self.position[0] + self.dimensions[0]):
                if self.position[1] <= mousepos[1] <= (self.position[1] + self.dimensions[1]):
                    return True
            return False

        def circ(mousepos): # For circular button
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

    def detect(self, e): # Detect if clicked
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

class PlayerSpawner(): # Aids in spawning a player object
    isDrawing = False # if true then the mouse is being held down
    def __init__(self, screen, startcoords):
        self.screen = screen
        self.startCoords = startcoords

    def addSecondCoord(self, coord):
        self.secondCoord = coord
        self.getHyp()

    def getHyp(self): # get length between points
        self.dx = self.startCoords[0] - self.secondCoord[0]
        self.dy = self.startCoords[1] - self.secondCoord[1]

        self.hyp = math.sqrt(self.dy**2 + self.dx**2)

    def spawn(self): # When the mouse is released
        return Player(self.screen, 1, self.startCoords, [self.dx//30, self.dy//30], [0,50,700,550]), self.hyp


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
        # Making sure vector is in correct direction
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
    def __init__(self, screen, font, position, size, mass):
        self.screen, self.position, self.mass = screen, position, mass
        self.size = size
        self.font = font
        self.selected = False
        self.defaults = [mass, size]
        self.TBD = False # To Be Deleted

        self.font.set_underline(True)
        title = self.font.render('Gravity Well', True, (0,0,0))
        self.font.set_underline(False)
        massTag = self.font.render('Mass:', True, (0,0,0))
        sizeTag = self.font.render('Size:', True, (0,0,0))
        massWidth, sizeWidth = massTag.get_width(), sizeTag.get_width()
        self.longTag = max(massWidth, sizeWidth)

        width = -(270 + self.longTag)
        height = -(180 + title.get_height())
        self.startcoords = [self.position[0] + width, self.position[1] + height]

        # Check if there's space
        if self.position[0] + width < 0:  # if not enough space to left
            width *= -1  # set right
            self.startcoords[0] = self.position[0]
        if self.position[1] + height < 50:  # if not enough space up
            height *= -1  # set down
            self.startcoords[1] = self.position[1]

        self.__width = width
        self.__height = height
        startcoords = self.startcoords

        self.__massBox = Textbox([self.screen, 0, self.font],
                                 [startcoords[0] + 40 + self.longTag, startcoords[1] + 20 + title.get_height()], [200, 50],
                                 str(self.mass))
        self.__sizeBox = Textbox([self.screen, 0, self.font],
                                 [startcoords[0] + 40 + self.longTag, startcoords[1] + 100 + title.get_height()], [200, 50],
                                 str(self.size))

        self.delBox = Button(self.screen, self.font, [self.startcoords[0]+abs(self.__width)-80, self.startcoords[1]+10], [70, 30])

    def draw(self, scheme, player): # Draws the well
        pygame.draw.circle(self.screen, scheme['text'], self.position, self.size)
        if player != None: # If there is a player object assigned to this well
            self.calc(player)
        if self.selected:
            self.drawSelectBox(scheme)
        if self.delBox.state:
            self.TBD = True

    def detect(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()

            dx, dy = mpos[0] - self.position[0], mpos[1] - self.position[1]
            if dx**2 + dy**2 <= self.size**2: # If in the well
                self.selected = True
            elif self.selected and self.between([self.position[0], self.position[0] + self.__width], # If selected and in the selection box
                                                mpos[0]) and self.between(
                [self.position[1], self.position[1] + self.__height], mpos[1]):
                self.selected = True

            else: # The user has clicked off of the selection box
                try:
                    self.mass = int(self.__massBox.return_input()) # Try assign the input value to mass
                except:
                    self.mass = self.defaults[0] # If invalid then set to default
                try:
                    self.size = int(self.__sizeBox.return_input()) # Try assign the input value to size
                except:
                    self.size = self.defaults[1] # If invalid then set to default
                self.selected = False
        if self.__massBox != False and self.selected: # If the textboxes exist and the well is selected, detect for the textboxes
            self.__massBox.detect(e)
            self.__sizeBox.detect(e)
            self.delBox.detect(e) # And detect for the deletion button



    def between(self, limits, num):
        if min(limits) <= num <= max(limits):
            return True


    def drawSelectBox(self, scheme):
        self.font.set_underline(True)
        title = self.font.render('Gravity Well', True, scheme['text']) # Render underlined title
        self.font.set_underline(False)
        massTag = self.font.render('Mass:', True, scheme['text']) # Render tags
        sizeTag = self.font.render('Size:', True, scheme['text'])

        pygame.draw.rect(self.screen, scheme['background'], [self.position[0], self.position[1], self.__width, self.__height]) # Draw the blank box
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0], self.position[1], self.__width, self.__height], 3)
        self.__massBox.draw(scheme) # Draw the textboxes
        self.__sizeBox.draw(scheme)
        self.delBox.draw(scheme, 'Del')

        titleWidth, massHeight, sizeHeight = title.get_width(), massTag.get_height(), sizeTag.get_height()

        self.screen.blit(title, [((270+self.longTag)//2)-(titleWidth//2)+self.startcoords[0], self.startcoords[1]+10]) # Blit all the text
        self.screen.blit(massTag, [self.startcoords[0]+10, 20 + title.get_height() + (25-(massHeight//2)) + self.startcoords[1]])
        self.screen.blit(sizeTag, [self.startcoords[0]+10, 100 + title.get_height() + (25-(sizeHeight//2)) + self.startcoords[1]])



    def calc(self, player): # Calculate the change in vectors
        dx = abs(self.position[0] - player.coords[0])
        dy = abs(self.position[1] - player.coords[1])
        theta = math.atan(dy/dx)

        G = 6.67 * (10**-11) # Universal gravitational constant
        r = math.sqrt((dx**2)+(dy**2)) # Distance between the objects
        if r < self.size:
            r = self.size

        g = (-G*self.mass)/(r**2) # Gravitational field strength at where the player is
        Fx = g*math.cos(theta) # Force in the x direction
        Fy = g * math.sin(theta) # Force in the y direction

        ax = abs(Fx / player.mass) # Acceleration in the x direction
        ay = abs(Fy / player.mass) # Acceleration in the y direction

        # Check where player is in relation to well
        # Is player below
        if player.coords[1] > self.position[1]:
            ay *= -1
        # Is player to the right
        if player.coords[0] > self.position[0]:
            ax *= -1

        player.vComps[0] += ax # Change the players vectors by the acceleration
        player.vComps[1] += ay

    def identity(self):
        return 'Well'



class ToggleSwitch():
    def __init__(self, screen, font, position, dimensions, default):
        self.screen, self.font, self.position, self.dimensions, self.state = screen, font, position, dimensions, default
        self.blockWidth = self.dimensions[0] * 0.4 # How wide the moving block is
        self.blockEnds = [0, self.dimensions[0] * 0.6] # X coords at either side
        self.goal = self.blockEnds[self.state] # Where it should be
        self.blockX = self.goal # Where it is
        self.speed = 7 # How many pixels it travels in a tick


    def draw(self, scheme):
        pygame.draw.rect(self.screen, scheme['on'], [self.position[0]+ self.blockX, self.position[1], self.blockWidth, self.dimensions[1]])
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0] + self.blockX, self.position[1], self.blockWidth, self.dimensions[1]], 3)
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]], 3)
        self.move()


    def detect(self, e): # If it has been clicked
        if e.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if self.position[0] <= mpos[0] <= (self.position[0]+self.dimensions[0]):
                if self.position[1] <= mpos[1] <= (self.position[1] + self.dimensions[1]):
                    if self.state:
                        self.state = 0
                    else:
                        self.state = 1
                    self.goal = self.blockEnds[self.state] # Change which side it should be at


    def move(self):
        if self.goal != self.blockX:
            temp = self.goal - self.blockX
            change = temp // abs(temp)
            change *= self.speed
            # Need to validate coords.
            self.blockX += change
            # Coord validation
            if self.blockX < self.blockEnds[0]:
                self.blockX = self.blockEnds[0]
            if self.blockX > self.blockEnds[1]:
                self.blockX = self.blockEnds[1]

    def identity(self):
        return 'ToggleSwitch'

class LabelToggleSwitch(ToggleSwitch):
    # Same as toggle switch but has labels above the left and right sides
    # The side which is selected will be highlighted in the on colour
    # while the side which isn't will be highlighted in the off colour
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

class Area(): # Parent class
    isDrawing = False # If true then the user will be on the second click
    def __init__(self, screen, cornerOne, cornerTwo=None):
        self.screen = screen
        self.origin = cornerOne
        self.drawAtMouse = False
        self.TBD = False
        if cornerTwo != None: # Does not need to initialise with a second corner
            self.dx, self.dy = cornerTwo[0] - cornerOne[0], cornerTwo[1] - cornerOne[1]
        else:
            self.drawAtMouse = True # If does not have second corner, second corner is mouse pos

    def draw(self):
        # handling when there isn't a second corner
        if self.drawAtMouse:
            cornerTwo = pygame.mouse.get_pos()
            self.dx, self.dy = cornerTwo[0] - self.origin[0], cornerTwo[1] - self.origin[1]

    def detect(self, e):
        # detect if clicked, if has then mark instance for deletion
        if e.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if Well.between(self, [self.origin[0], self.origin[0]+self.dx], mpos[0]) and Well.between(self, [self.origin[1], self.origin[1]+self.dy], mpos[1]):
                self.TBD = True
                return True
        return False



    def identity(self):
        return 'Area'

class PlayerArea(Area):
    def draw(self, scheme):
        super().draw() # Special draw - needs different colour than other areas
        pygame.draw.rect(self.screen, scheme['off'], [self.origin[0], self.origin[1], self.dx, self.dy], 3)

    def identity(self):
        return 'PlayerArea'

class GoalArea(Area):
    def draw(self, scheme):
        super().draw() # Special draw - needs different colour than other areas
        pygame.draw.rect(self.screen, scheme['on'], [self.origin[0], self.origin[1], self.dx, self.dy], 3)

    def playerDetect(self, coords):
        if Well.between(self, [self.origin[0], self.origin[0] + self.dx], coords[0]) and Well.between(self,
                        [self.origin[1], self.origin[1] + self.dy],coords[1]):
            return True
        return False

    def identity(self):
        return 'GoalArea'

class Wall(Area):
    def draw(self, scheme):
        super().draw() # Special draw - needs different colour than other areas
        pygame.draw.rect(self.screen, scheme['outline'], [self.origin[0], self.origin[1], self.dx, self.dy])

    def playerDetect(self, player):
        def isCloserTo(num, bound1, bound2):
            if abs(bound1 - num) < abs(bound2 - num):
                return True
            return False
        coords = player.coords
        if Well.between(self, [self.origin[0], self.origin[0] + self.dx], coords[0]) and Well.between(self,
                        [self.origin[1],self.origin[1] + self.dy],coords[1]):
            # Get boundaries
            xBoundaries = [min(self.origin[0], self.origin[0] + self.dx), max(self.origin[0], self.origin[0] + self.dx)]
            yBoundaries = [min(self.origin[1], self.origin[1] + self.dx), max(self.origin[1], self.origin[1] + self.dx)]

            # Step 1 - Convert coords
            wallCoords = [[0,0], [0, yBoundaries[1]-yBoundaries[0]], [xBoundaries[1] - xBoundaries[0], yBoundaries[1]-yBoundaries[0]], [xBoundaries[1] - xBoundaries[0], 0]] # From bottom left, clockwise
            prevCoord = [coords[0] - player.vComps[0], coords[1] - player.vComps[1]]
            point1 = [prevCoord[0] - xBoundaries[0], yBoundaries[1] - prevCoord[1]]
            point2 = [coords[0] - xBoundaries[0], yBoundaries[1] - coords[1]]

            # Step 2 - y=mx+c
            m = (point1[1] - point2[1]) / (point1[0] - point2[0])
            eq = [m, (m*point1[0]) + point1[1]] # [m, c]

            # Step 3 - Simultaneous equations
            hitX = False
            hitY = False
            # Hits top
            y = yBoundaries[1]-yBoundaries[0]
            if eq[0] == 0:
                eq[0] = 1/999999999999
            print(eq[0])
            x = (y - eq[1]) / eq[0]
            if 0 <= x <= (xBoundaries[1] - xBoundaries[0]):
                hitY = True

            # Hit bottom
            y = 0
            x = (y - eq[1]) / eq[0]
            if 0 <= x <= (xBoundaries[1] - xBoundaries[0]):
                hitY = True

            # Hit left
            x = 0
            y = (eq[0]*x) + eq[1]
            print(eq[1])
            print(y)
            if 0 <= y <= (yBoundaries[1] - yBoundaries[0]):
                hitX = True

            # Hit right
            x = xBoundaries[1] - xBoundaries[0]
            y = (eq[0] * x) + eq[1]
            if 0 <= y <= (yBoundaries[1] - yBoundaries[0]):
                hitX = True

            if hitX:
                player.vComps[0] *= -1
            if hitY:
                player.vComps[1] *= -1

    def identity(self):
        return 'WallArea'

