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
    file = open(filename, 'r')
    reader = csv.reader(file)
    settings = []
    for row in reader:
        settings.append(row)
    return settings

def parseSettings(settings):
    colours = {}
    for row in settings:
        # Colour scheme checks
        if row[0] == 'colour schemes':
            amount = int(row[1])
            currentSettingRow = settings.index(row)
            # For each scheme
            for schemeNum in range(1, amount+1):
                scheme = settings[currentSettingRow+schemeNum]
                # Create scheme dict
                schemeDict = {}
                titles = ['background', 'outline', 'on', 'off', 'text']
                # Create background etc key, value pairs
                for i in range(1, len(scheme), 3):
                    schemeDict[titles[(i-1)//3]] = (int(scheme[i]), int(scheme[i+1]), int(scheme[i+2]))

                # Add scheme dict to colours dict
                colours[scheme[0]] = schemeDict

    return colours