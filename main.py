# Gnome Launch
# Main runtime file

from subroutines import *
from variables import *

def start_menu():
    def generate_front(screen, *args):
        # Takes in a list of lists of name and actions
        title_font = pygame.font.SysFont('nasalization', 50, False, True)
        title = title_font.render('Gnome Launch!', True, scheme['text'])
        title_height, title_width, title_buffer = title.get_height(), title.get_width(), 30
        width, height, buffer = 200, 80, 10
        screenWidth, screenHeight = defaultSize()
        amount = len(args)
        title_startx = (screenWidth // 2) - (title_width // 2)
        startx = (screenWidth // 2) - (width // 2)
        totalButtonHeight = (amount * height) + ((amount-1) * buffer) + (title_height + title_buffer)
        starty = (screenHeight // 2) - (totalButtonHeight // 2)
        title_package = [title, title_startx, starty]

        # Create dictionary and add the buttons
        buttons = {}
        for index, info in enumerate(args):
            name, action = info
            relY = starty + (index * (height+buffer)) + (title_height + title_buffer)
            buttons[name] = Button(screen, font, [startx, relY], [width, height], action)
        return buttons, title_package

    def draw_title(screen, package):
        title, x, y = package
        screen.blit(title, [x,y])

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


    settingsButton = PicButton(screen, font, [defaultSize()[0] - 60, 10], [50, 50], settings_screen)
    settingsButton.assignDrawFunc(drawGear)

    ay = Spaceship(screen, [30, 30], [0,0], 'saucer')

    # Start menu main loop
    while True:
        buttons, title_package = generate_front(screen, ('Tutorial', emptyFunc), ('Designer', emptyFunc),
                                                ('Load', emptyFunc))
        for e in pygame.event.get():
            detect_buttons(e)
            settingsButton.detect(e)
            if e.type == pygame.QUIT:
                pygame.quit()

        pygame.display.set_caption("Gnome Launch - Start Menu")
        screen.fill(scheme["background"])
        draw_buttons()
        settingsButton.draw(scheme)
        draw_title(screen, title_package)
        draw_creds(screen)
        ay.draw(scheme)

        pygame.display.flip()
        clock.tick(60)

def settings_screen():
    global current_scheme, scheme, settings, colours
    def finish():
        return True

    def write_settings():
        new_settings = []
        def colour_schemes(new_settings):
            new_settings.append(['colour schemes', str(len(colours)), current_scheme])
            order = ['background', 'outline', 'on', 'off', 'text']
            for key, diff_schemes in colours.items():
                cur_scheme = [key]
                for val in order:
                    for i in diff_schemes[val]:
                        cur_scheme.append(str(i))
                new_settings.append(cur_scheme)
            return new_settings
        new_settings = colour_schemes(new_settings)
        with open('settings.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in new_settings:
                writer.writerow(row)
            file.close()

        return new_settings

    done = False
    backButton = Button(screen, font, [defaultSize()[0] - 110, defaultSize()[1] - 50], [100, 40], finish)
    col_schemes = ColourSchemes(screen, font, colours, current_scheme, [10, 10])

    # Settings main loop
    while not done:
        for e in pygame.event.get():
            done = backButton.detect(e)
            scheme, current_scheme = col_schemes.detect(e)
            col_schemes.current = current_scheme
            if e.type == pygame.QUIT:
                pygame.quit()

        pygame.display.set_caption("Gnome Launch - Settings")
        screen.fill(scheme['background'])
        backButton.draw(scheme, 'Back')
        col_schemes.draw(scheme)
        pygame.display.flip()
        clock.tick(60)

    settings = write_settings()


# Main
settings = importSettings('settings.csv')
colours, defaultScheme = parseSettings(settings)
current_scheme = defaultScheme
scheme = colours[current_scheme]

screen, clock = setupPygame(defaultSize(), 'Gnome Launch')

start_menu()
