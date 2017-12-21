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
        return colours
    except SettingsError as e:
        print(e.message)
    except:
        print('An unexpected Error occured.')
        if input('Print error message? (y/n) >> ').lower() == 'y':
            e = sys.exc_info()
            print(e)
    return False