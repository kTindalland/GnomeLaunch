# Gnome Launch
# Main runtime file

from subroutines import *
from variables import *

def main():
    settings = importSettings('Settings.csv')
    colours, defaultScheme = parseSettings(settings)
    global scheme
    scheme = colours[defaultScheme]

    screen, clock = setupPygame(defaultSize(), 'Gnome Launch')

    start_menu(screen, clock, colours)

def start_menu(screen, clock, colours):
    pygame.display.set_caption("Gnome Launch - Start Menu")

    def generate_buttons(screen, *args):
        # Takes in a list of lists of name and action

        width, height, buffer = 200, 80, 10
        screenWidth, screenHeight = defaultSize()
        amount = len(args)
        startx = (screenWidth // 2) - (width // 2)
        totalButtonHeight = (amount * height) + ((amount-1) * buffer)
        starty = (screenHeight // 2) - (totalButtonHeight // 2)

        # Create dictionary and add the buttons
        buttons = {}
        for index, info in enumerate(args):
            name, action = info
            relY = starty + (index * (height+buffer))
            buttons[name] = Button(screen, font, [startx, relY], [width, height], action)
        return buttons

    def draw_title(screen, message='Gnome Launch!'):

        title_font =  pygame.font.SysFont('nasalization',50,False,True)
        text = title_font.render(message, True, scheme['text'])


        width = text.get_width() // 2
        screenx = defaultSize()[0]

        screen.blit(text, [(screenx//2)-width,30])


    buttons = generate_buttons(screen, ('Tutorial', emptyFunc), ('Designer', emptyFunc), ('Load', emptyFunc))

    def draw_buttons():
        for key, value in buttons.items():
            value.draw(scheme, key)

    def detect_buttons(e):
        for key, value in buttons.items():
            value.detect(e)

    while True:
        for e in pygame.event.get():
            detect_buttons(e)
            if e.type == pygame.QUIT:
                pygame.quit()

        screen.fill(scheme["background"])
        draw_buttons()
        draw_title(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
