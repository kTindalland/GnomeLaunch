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
                defaultScheme = settings[currentSettingRow+1][0]
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

def drawGear(screen, scheme, position, dimensions):
    # Assumes the button is square
    # Assign vars
    centre = [int(position[0]+(dimensions[0]//2)), int(position[1]+(dimensions[1]//2))] # Centre of the button
    gearRad = int(dimensions[0] * 0.4)
    outerRad = int(dimensions[0] * 0.6) // 2
    innerRad = int(dimensions[0] * 0.3) // 2
    cornerRad = int(dimensions[0] * 0.1)
    rectWidth = math.sqrt((cornerRad**2)*2)
    topLeft, topRight = [centre[0] - gearRad, centre[1] - gearRad], [centre[0] + gearRad, centre[1] - gearRad]
    bottomLeft, bottomRight = [centre[0] - gearRad, centre[1] + gearRad], [centre[0] + gearRad, centre[1] + gearRad]

    # Draw outer circle
    pygame.draw.circle(screen, scheme['text'], centre, outerRad)

    # Draw straight rects
    # Vertical
    pygame.draw.rect(screen, scheme['text'], [centre[0] - rectWidth//2, centre[1] - gearRad, rectWidth, gearRad * 2])
    # Horizontal
    pygame.draw.rect(screen, scheme['text'], [centre[0] - gearRad, centre[1] - rectWidth//2, gearRad * 2, rectWidth])

    # Draw polygons
    pygame.draw.polygon(screen, scheme['text'],
        [topRight, [topRight[0], topRight[1] + cornerRad], [bottomLeft[0] + cornerRad, bottomLeft[1]],
        bottomLeft, [bottomLeft[0], bottomLeft[1] - cornerRad],[topRight[0] - cornerRad, topRight[1]]])
    pygame.draw.polygon(screen, scheme['text'],
        [topLeft, [topLeft[0], topLeft[1] + cornerRad], [bottomRight[0] - cornerRad, bottomRight[1]],
         bottomRight, [bottomRight[0], bottomRight[1] - cornerRad], [topLeft[0] + cornerRad, topLeft[1]]])
    """pygame.draw.polygon(screen, scheme['text'],
                        [[topRight[0], topRight[1] + cornerRad], [bottomLeft[0] + cornerRad, bottomLeft[1]],
                         [bottomLeft[0], bottomLeft[1] - cornerRad],
                         [topRight[0] - cornerRad, topRight[1]]])
    pygame.draw.polygon(screen, scheme['text'],
                        [[topLeft[0], topLeft[1] + cornerRad], [bottomRight[0] - cornerRad, bottomRight[1]],
                        [bottomRight[0], bottomRight[1] - cornerRad],
                         [topLeft[0] + cornerRad, topLeft[1]]])"""

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

    def detect(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if self.equation(pygame.mouse.get_pos()):
                self.action()

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

class PicButton(Button):
    def assignDrawFunc(self, func):
        self.drawFunc = func

    def draw(self, scheme):
        self.rectDraw(scheme, '')
        self.drawFunc(self.screen, scheme, self.position, self.dimensions)