# Gnome Launch
# Main runtime file

from subroutines import *
from variables import *

def main():
    settings = importSettings('Settings.csv')
    colours, defaultScheme = parseSettings(settings)
    scheme = colours[defaultScheme]

    screen, clock = setupPygame(defaultSize(), 'Test window')
    done = False

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

        screen.fill(scheme['background'])
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
