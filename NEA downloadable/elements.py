import pygame

pygame.init()

COLOR_ACTIVE = pygame.Color('maroon')
COLOR_PASSIVE = pygame.Color('gray')

FONT = pygame.font.SysFont('Calluna', 32)

class Element:  # This class acts as a parent class
    def __init__(self, x, y, w, h, text=''):  # This is all the parameters it takes in
        self.x = x  # x coordinate element starts at
        self.y = y  # y coordinate element starts at
        self.w = w  # width of the element
        self.h = h  # height of the element
        self.text = text  # text in button/prompt of input box
        self.rect = pygame.Rect(x, y, w, h)  # creates a rectangle with the data above
        self.active = False  # if self.active is true, the button/input box has been clicked

    def draw(self, screen):  # this function is empty as it will be overridden in both child classes
        pass

    def handle_event(self, event): # This function draws the element on the board
        if event.type == pygame.MOUSEBUTTONDOWN:  # if event is a mouse click
            if self.rect.collidepoint(event.pos):  # if position of mouse click is within the rectagle, active is true
                self.active = True
            else:  # else, active remains false
                self.active = False

class Button(Element):  # The button class inherits the element class as shown
    def __init__(self, x, y, w, h, text=''):
        super().__init__(x, y, w, h, text)  # All these parameters are handeled by the parent class.
        self.COLOR_TEXT = (0, 0, 0)  # color of the text: Black
        self.txt_surface = FONT.render(text, True, self.COLOR_TEXT)

        if self.txt_surface.get_width() > w:
            # If the length of the text is greater than the user entered width of the button, the width increases to ensure that text is inside button
            self.rect = pygame.Rect(x, y, self.txt_surface.get_width() + 10, h)
        else:
            self.rect = pygame.Rect(x, y, w, h)

        self.COLOR_BUTTON = pygame.Color('burlywood1')  # this is the color of the button: beige

    def draw(self, screen):  # this needs to be overridden as it is unique to buttons
        pygame.draw.rect(screen, self.COLOR_BUTTON, self.rect)
        screen.blit(self.txt_surface, (self.rect.x +5, self.rect.y + 5))  # diplay text in the middle of button

    #  Button class inherits the handle event function from the parent class

class InputBox(Element):  # The InputBox class inherits the element class as shown

    def __init__(self, x, y, w, h, text, textType = 'text'):  # The textType parameter is not handeled by the parent class.
        super().__init__(x, y, w, h, text)  # All these parameters are handeled by the parent class.
        self.OGw = w  # Original width
        self.color = COLOR_PASSIVE  # color passive is the color of the input box when no clicked on
        self.userInput = ''  # what the user will type, This is a stack structure
        self.txt_surface = FONT.render(self.userInput, True, self.color)
        self.textType = textType  # type of text: text/password/integer
        self.text_surface = FONT.render(self.text, True, (0,0,0))

    def handle_event(self, event):  # The handle_event function is overridden as an input box works in a different way as it has to handle key presses.
        if event.type == pygame.MOUSEBUTTONDOWN:  # if event is a mouse click
            if self.rect.collidepoint(event.pos):  # if mouse click position is inside rectangle(input box)
                self.active = True  # cilcked
            else:
                self.active = False

            if self.active:
                self.color = COLOR_ACTIVE  # if input box is active, change the color of the box to indicate that it has been clicked on
            else:
                self.color = COLOR_PASSIVE

        if event.type == pygame.KEYDOWN:  # if user clicks a button on keyboard:
            if self.active:  # and if the input box has been clicked on

                if event.key == pygame.K_BACKSPACE:  # if keypress is a backspace
                    self.userInput = self.userInput[:-1]  # remove last letter of userInput, this is a stack structure as FILO

                elif self.textType.lower() == 'int':  # if text type is an integer, only allow numbers 1-9 on the input box
                    if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        self.userInput += event.unicode  # add number to user input

                else:  # if text type is a string, add the character to user input
                    self.userInput += event.unicode

                if self.textType.lower() == 'password':  # if the type is password, replace all the characters to display with *
                    self.txt_surface = FONT.render('*' * len(self.userInput), True, self.color)

                else:
                    self.txt_surface = FONT.render(self.userInput, True, self.color)


    def update(self, screen):  # This fucntion does not exist in the parent class
        # Resize the box if the text is too long.
        screen.fill((255, 255, 255), (self.x - self.text_surface.get_width() - 5, self.y, self.w + self.text_surface.get_width()+10, self.h))
        width = max(self.OGw, self.txt_surface.get_width() + 10)  # pick between whichever is greater: the original width or the width of the text
        self.w = width
        self.rect.w = width

    def draw(self, screen):  # This function is overridden as I will need to add a prompt before the input box
        screen.blit(self.text_surface, (self.rect.x - self.text_surface.get_width() - 5, self.rect.y + 5))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 2)