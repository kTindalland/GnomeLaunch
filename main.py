# Gnome Launch
# Main runtime file

from subroutines import *

settings = importSettings('nvalidSettings.csv')
colours = parseSettings(settings)
print(colours)