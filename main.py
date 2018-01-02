# Gnome Launch
# Main runtime file

from subroutines import *
from variables import *

def main():
    def start_menu():
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

        def draw_creds(screen):
            font = pygame.font.SysFont("roboto", 15, True, False)
            creds = 'Created by Kai Tindall, 2018'
            text = font.render(creds, True, scheme['text'])
            height = text.get_height()
            screeny = defaultSize()[1]
            screen.blit(text, [10, screeny-height-10])

        def draw_buttons():
            for key, value in buttons.items():
                value.draw(scheme, key)

        def detect_buttons(e):
            for key, value in buttons.items():
                value.detect(e)

        buttons = generate_buttons(screen, ('Tutorial', emptyFunc), ('Designer', emptyFunc), ('Load', emptyFunc))
        settingsButton = PicButton(screen, font, [defaultSize()[0] - 60, 10], [50, 50], emptyFunc)
        settingsButton.assignDrawFunc(drawGear)

        # Start menu main loop
        while True:
            for e in pygame.event.get():
                detect_buttons(e)
                if e.type == pygame.QUIT:
                    pygame.quit()

            screen.fill(scheme["background"])
            draw_buttons()
            settingsButton.draw(scheme)
            draw_title(screen)
            draw_creds(screen)

            pygame.display.flip()
            clock.tick(60)

    # Main
    settings = importSettings('Settings.csv')
    colours, defaultScheme = parseSettings(settings)
    scheme = colours[defaultScheme]

    screen, clock = setupPygame(defaultSize(), 'Gnome Launch')

    start_menu()

if __name__ == '__main__':
    main()
