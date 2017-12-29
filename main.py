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

    testFunc = lambda : print('Hello world')
    b = Button(screen, font, [50,50],[100,40], testFunc)

    while not done:
        for e in pygame.event.get():
            b.detect(e)
            if e.type == pygame.QUIT:
                done = True

        screen.fill(scheme['background'])

        b.draw(scheme, 'Hello')

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
