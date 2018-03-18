import time, pygame
class Textbox():
    def __init__(self, lcl_info, lcl_coords, lcl_dimentions, lcl_starttext='', lcl_ispassword=False):
        self.__screen, self.font     = lcl_info[0],       lcl_info[2]
        self.__x,      self.__y      = lcl_coords[0],     lcl_coords[1]
        self.__width,  self.__height = lcl_dimentions[0], lcl_dimentions[1]
        self.starttext               = lcl_starttext
        self.selected                = False
        self.text                    = ''
        self.__caps                  = False
        self.cursor                  = 0
        self.starttime               = int(time.time())
        self.password                = lcl_ispassword

    def reset_time(self):
        self.starttime = int(time.time())

    def check_length(self, lcl_string):
        text = self.font.render(lcl_string, True, (0,0,0))
        if text.get_width() > self.__width - 10:
            return True
        else:
            return False

    def insert_string(self, lcl_string, lcl_insert, lcl_index):
            strng = lcl_string[:lcl_index] + lcl_insert + lcl_string[lcl_index:]
            if self.check_length(strng):
                return self.text
            else:
                self.cursor += 1
                return strng

    def cutdown_string(self, lcl_string):
        length = self.font.render(lcl_string, True, (0,0,0)).get_width()
        if length > self.__width - 10:
            return self.cutdown_string(lcl_string[:-1])
        else:
            return lcl_string

    def backspace(self, lcl_string, lcl_index):
        if self.cursor <= 0:
            self.cursor = 0
            return self.text
        self.cursor -= 1
        return lcl_string[:lcl_index-1] + lcl_string[lcl_index:]

    def draw(self, scheme):
        self.starttextcol = scheme['off']
        bordercol     = scheme['outline']
        backgroundcol = scheme['background']

        # Draw box
        pygame.draw.rect(self.__screen, backgroundcol, (self.__x, self.__y, self.__width, self.__height))
        pygame.draw.rect(self.__screen, bordercol, (self.__x, self.__y, self.__width, self.__height),3)

        # Draw text
        if len(self.text) > 0:
            if self.password:
                text = self.font.render('*'*len(self.text), True, scheme['text'])
            else:
                text = self.font.render(self.text, True, scheme['text'])
            isText = True
        elif len(self.starttext) > 0:
            text = self.font.render(self.cutdown_string(self.starttext), True, self.starttextcol)
            isText = True
        else:
            isText = False

        if isText:
            textx      = self.__x + 5
            textheight = text.get_height()
            texty      = ((self.__height - textheight) // 2) + self.__y

            self.__screen.blit(text, [textx, texty])
            self.draw_cursor(scheme=scheme)

    def detect(self, lcl_event):
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        nums = [["0",")"],["1","!"],["2","\""],["3","£"],["4","$"],["5","%"],
               ["6","^"],["7","&"],["8","*"],["9","("]]

        if lcl_event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            if self.__x <= m_pos[0] <= (self.__x + self.__width) and self.__y <= m_pos[1] <= (self.__y + self.__height):
                self.selected = True
            else:
                self.selected = False

        if self.selected:
            if lcl_event.type == pygame.KEYDOWN:
                #print(lcl_event.key)
                if lcl_event.key == 304 or lcl_event.key == 303: # Shift
                    self.__caps = True
                elif lcl_event.key >= 97 and lcl_event.key <= 122: # A - Z
                    self.add_key(alphabet[lcl_event.key - 97].upper(),alphabet[lcl_event.key - 97])
                elif lcl_event.key >= 48 and lcl_event.key <= 57: # 0 - 9
                    self.add_key(nums[lcl_event.key - 48][1],nums[lcl_event.key - 48][0])
                elif lcl_event.key == 32: # Space bar
                    self.text = self.insert_string(self.text, " ", self.cursor)
                elif lcl_event.key == 8: # Backspace
                    self.text = self.backspace(self.text,self.cursor)
                elif lcl_event.key == 59: # ; - :
                    self.add_key(":",";")
                elif lcl_event.key == 275: # Right arrow key
                    self.cursor += 1
                    if self.cursor > len(self.text):
                        self.cursor = len(self.text)
                    self.reset_time()
                elif lcl_event.key == 276: # Left arrow key
                    self.cursor -= 1
                    if self.cursor < 0:
                        self.cursor = 0
                    self.reset_time()
                elif lcl_event.key == 47: # / - ?
                    self.add_key("?","/")
                elif lcl_event.key == 46: # . - >
                    self.add_key(">",".")
                elif lcl_event.key == 44: # , - <
                    self.add_key("<",",")
                elif lcl_event.key == 45:
                    self.add_key("_","-")
                elif lcl_event.key == 61:
                    self.add_key("+","=")
                elif lcl_event.key == 60:
                    self.add_key("|","\\")
            elif lcl_event.type == pygame.KEYUP:
                if lcl_event.key == 304 or lcl_event.key == 303:
                    self.__caps = False

    def add_key(self,ifcaps,norm):
        if self.__caps:
            self.text = self.insert_string(self.text, ifcaps, self.cursor)
        else:
            self.text = self.insert_string(self.text, norm, self.cursor)

    def draw_cursor(self, scheme):
        current_time = int(time.time())
        delta_time   = current_time - self.starttime
        if delta_time % 2 == 0 and self.selected:
            if self.password:
                render = self.font.render('*'*len(self.text[:self.cursor]),True, scheme['text'])
            else:
                render = self.font.render(self.text[:self.cursor],True,scheme['text'])
            x_offset = render.get_width() + 5 + self.__x
            height   = render.get_height()
            y_offset = ((self.__height - height) // 2) + self.__y
            pygame.draw.line(self.__screen, scheme['text'],[x_offset,y_offset],[x_offset, y_offset+height],3)

    def return_input(self):
        return self.text