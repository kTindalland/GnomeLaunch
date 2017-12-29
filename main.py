# Gnome Launch
# Main runtime file

from subroutines import *
from variables import *

def main():
    settings = importSettings('Settings.csv')
    colours, defaultScheme = parseSettings(settings)
    scheme = colours[defaultScheme]

    screen, clock = setupPygame(defaultSize(), 'Gnome Launch')

    start_menu(screen, clock, scheme)

def start_menu(screen, clock, scheme):
    pygame.display.set_caption("Gnome Launch - Start Menu")

    buttons = {
        'Tutorials' : None
    }

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        screen.fill(scheme["background"])
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
