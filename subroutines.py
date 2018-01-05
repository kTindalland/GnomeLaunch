# Gnome Launch
# Subroutines file

# Importing variables
from variables import *

# Exception to be raised when something goes wrong in parsing settings
class SettingsError(Exception):
    def __init__(self, message):
        self.message = message

# Import settings from file
def importSettings(filename='settings.csv'):
    try:
        file = open(filename, 'r')
    except:
        print('An error occured in importSettings.')
        return False
    else:
        reader = csv.reader(file)
        settings = []
        for row in reader:
            settings.append(row)
        file.close()
        return settings

# Convert settings list into usable variables
def parseSettings(settings):
    colours = {}
    try:
        for row in settings:
            # Colour scheme checks
            if row[0] == 'colour schemes':

                amount = int(row[1])
                # If more than 5 colour schemes present.
                if amount > 5:
                    raise SettingsError('Too many colour schemes.')
                currentSettingRow = settings.index(row)
                # For each scheme
                # Set reserved names
                usedNames = ['colour schemes']
                for schemeNum in range(1, amount+1):
                    scheme = settings[currentSettingRow+schemeNum]
                    # Checking for valid name.
                    if scheme[0] in usedNames:
                        raise SettingsError('Name already used or reserved. Infringing name: \"{}\".'.format(scheme[0]))
                    # Create scheme dict
                    schemeDict = {}
                    titles = ['background', 'outline', 'on', 'off', 'text']
                    # Create background etc key, value pairs
                    for i in range(1, len(scheme), 3):
                        schemeDict[titles[(i-1)//3]] = (int(scheme[i]), int(scheme[i+1]), int(scheme[i+2]))

                    # Add scheme dict to colours dict
                    colours[scheme[0]] = schemeDict
                defaultScheme = row[2]
        return colours, defaultScheme
    except SettingsError as e:
        print(e.message)
    except:
        print('An unexpected Error occured.')
        if input('Print error message? (y/n) >> ').lower() == 'y':
            e = sys.exc_info()
            print(e)
    return False

# Return current default screensize
defaultSize = lambda: [screenx, screeny]

# Null function for testing purposes
emptyFunc = lambda: None

# Create pygame objects
def setupPygame(screensize=defaultSize(), caption='Gnome Launch'):
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return [screen, clock]

# returns selected colour schemes
def changeScheme(schemes, key=False):
    if type(key) is not str or key not in schemes.keys():
        print('Invalid scheme!')
        return False
    else:
        return schemes[key]

def buttonChangeScheme(arg):
    schemes, key = arg
    if type(key) is not str or key not in schemes.keys():
        print('Invalid scheme!')
        return False
    else:
        return schemes[key], key

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

# Classes for buttons
class Button():
    def __init__(self, screen, font, position, dimensions, action=emptyFunc):
        self.screen, self.font, self.position, self.dimensions, self.action = screen, font, position, dimensions, action

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

    def detect(self, e, arg=None):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.equation(pygame.mouse.get_pos()):
                if arg == None:
                    return self.action()
                return self.action(arg)

    def rectDraw(self, scheme, label):
        # Draw rectangles
        pygame.draw.rect(self.screen, scheme['off'], [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]])
        pygame.draw.rect(self.screen, scheme['outline'], [self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]], 3)

        # Draw label
        if label != '' and type(label) is str:
            text = self.font.render(label, True, scheme['text'])
            width, height = text.get_width() // 2, text.get_height() // 2
            self.screen.blit(text, [self.position[0]+(self.dimensions[0]//2)-width, self.position[1]+(self.dimensions[1]//2)-height])

    def circDraw(self, scheme, label):
        # Draw rectangles
        pygame.draw.circle(self.screen, scheme['off'], self.position, self.dimensions)
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

# Draws the colour scheme part of settings
class ColourSchemes():
    def __init__(self, screen, font, colours, current, position):
        self.screen, self.font, self.colours, self.current, self.position = screen, font, colours, current, position

    def draw(self, scheme):
        title = self.font.render('Colour Scheme:', True, scheme['text'])
        title_width, title_height, buffer = title.get_width(), title.get_height(), 10

        self.buttons = []
        for i in enumerate(self.colours):
            relPos = [self.position[0] + title_width + (buffer * (i[0]+1)) + (100 * i[0]), self.position[1] + (title_height // 2) - 20]
            self.buttons.append(Button(self.screen, self.font, relPos, [100, 40], buttonChangeScheme))

        self.screen.blit(title, self.position)
        self.tags = sorted(self.colours)
        for index, tag in enumerate(self.tags):
            self.buttons[index].draw(scheme, tag)

    def detect(self, e):
        for index, button in enumerate(self.buttons):
            output = button.detect(e, [self.colours, self.tags[index]])
            if output != None:
                return output
        return self.colours[self.current], self.current

class Spaceship():
    def __init__(self, screen, position, components, skin='saucer'):
        self.screen, self.position, self.components, self.skin = screen, position, components, skin
    def draw(self, scheme):
        if self.skin == 'saucer':
            pygame.draw.ellipse(self.screen, scheme['off'], [self.position[0]-25, self.position[1]-20, 50, 20])