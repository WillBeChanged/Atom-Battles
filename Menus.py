#!/usr/bin/python

'''
This executable controls the drawing of all menu's
'''

import pygame
import Extras

class Essentials(object):
    '''Methods to be used by lower classes'''
    def initialise(self):
        '''initialise variables that will be used in both classes'''
        hovered_button = None

    def image_prep(self, button):
        '''Calculates position at which button will be placed'''
        x_pos  = (self.screen_width  * button["size"]["x"])/2
        y_space  = button["size"]["d"] * self.screen_height
        y_offset = 0.5 * (1-button["size"]["y"]) * y_space
        y_pos = y_space * button["NumRef"] + y_offset
        length = self.screen_width  - x_pos*2
        height = self.screen_height * button["size"]["y"] * button["size"]["d"]
        button_rect = pygame.Rect(x_pos, y_pos, length, height)
        return button_rect

    def typing_offset(self, image, text):
        '''Calculates the offset at which the text on the button should be placed'''
        text = Extras.type_create(text, self.generic_text_colour, self.button_placing[0][3]/3, pygame.font)
        x_offset = (image.get_rect().size[0]-(text.get_width()-400))/2
        y_offset = (image.get_rect().size[1]-(text.get_height()-100))/2
        return [x_offset, y_offset, text]

    def button_prepare(self, button, image):
        '''Prepares the button and text on button to be drawn by "button_draw"'''
        self.button_placing[button["NumRef"]] = self.image_prep(button)
        self.button_text[button["NumRef"]] = self.typing_offset(image, button["Name"])

    def button_draw(self, screen, change=False):
        '''Draws buttons onto the screen'''
        if change:
            self.button_placing = {}
            self.button_text = {}
        for num, button in self.button_dict.items():
            if button["Active"]:
                if button["Hover"]:
                    image = pygame.image.load("Images/button_selected.png")
                else:
                    image = pygame.image.load("Images/button_normal.png")
            else:
                image = pygame.image.load("Images/button_inactive.png")
            if change:
                self.button_prepare(button, image)
            button_placing_ref = self.button_placing[num]
            button_text_ref = self.button_text[num]
            image = pygame.transform.scale(image, (button_placing_ref[2], button_placing_ref[3]))
            screen.blit(image, (button_placing_ref[0], button_placing_ref[1]))
            screen.blit(button_text_ref[2], (button_placing_ref[0]+button_text_ref[0], button_placing_ref[1]+button_text_ref[1]))
        return screen

    def button_hover(self, mouse_x, mouse_y):
        '''When mouse is over a button, the sprite for that button changes to lit up in indication of this'''
        for num, button in self.button_placing.items():
            self.button_dict[num]["Hover"] = False
            if button.collidepoint(mouse_x, mouse_y):
                self.button_dict[num]["Hover"] = True
                hovered_button = self.button_dict[num]["Hover"]
            else:
                hovered_button = None

class MainMenu(Essentials):
    '''The main menu, which is displayed when the game is run'''
    def __init__(self, screen_width, screen_height, first_play=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.button_dict = {
        0: {"Name":"New Game",  "NumRef":0, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":True},
        1: {"Name":"Continue",  "NumRef":1, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":first_play},
        2: {"Name":"High Score","NumRef":2, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":True},
        3: {"Name":"Options",   "NumRef":3, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":True},
        4: {"Name":"Exit",      "NumRef":4, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":True}
        }
        self.button_placing = {}
        self.button_text = {}
        self.generic_text_colour = (0, 0, 0)


class Options(Essentials):
    '''Options menu, accessed from the main menu'''
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        options = shelve.open('Options')
        if not options:
            options = self.set_def_options()
        self.button_dict = {
        0: {"Name":"On",  "NumRef":0, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":opt_dict['Sound'][0],  "Active":True},
        1: {"Name":"Off", "NumRef":1, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":not opt_dict['Sound'][0], "Active":True},
        2: {"Name":''  ,  "NumRef":2, "size":{"x":1/2.0, "y":2/3.0, "d":1/5.0}, "Hover":False, "Active":opt_dict['Sound'][0]}
        }

    def set_def_options(self):
        opt_dict = {
        'Sound':(True, 0)}
        return opt_dict


if __name__ == "__main__":
    import sys

    pygame.font.init()
    pygame.image.get_extended()
    pygame.display.init()

    ORIGWIDTH, ORIGHEIGHT = 1500, 900
    WIDTH, HEIGHT = ORIGWIDTH, ORIGHEIGHT
    FIRST_PLAY = False
    MAINMENU = True
    OPTIONSMENU = False

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    MENU = MainMenu(WIDTH, HEIGHT, FIRST_PLAY)
    MENU.button_draw(SCREEN, True)

    while True:
        MOUSEX, MOUSEY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_f:
                    if (WIDTH, HEIGHT) == (ORIGWIDTH, ORIGHEIGHT):
                        SCREEN = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
                        WIDTH, HEIGHT = SCREEN.get_width(), SCREEN.get_height()
                        MENU = Essentials(WIDTH, HEIGHT, FIRST_PLAY)
                    else:
                        SCREEN = pygame.display.set_mode((ORIGWIDTH, ORIGHEIGHT))
                        WIDTH, HEIGHT = ORIGWIDTH, ORIGHEIGHT
                        MENU = Essentials(ORIGWIDTH, ORIGHEIGHT, FIRST_PLAY)
                    MENU.button_draw(SCREEN, True)
                elif event.key == pygame.K_n:
                    FIRST_PLAY = not FIRST_PLAY

        #if MENU.hovered_button["Name"] == "Options":
        #    OPTIONSMENU = not OPTIONSMENU
        #    MAINMENU = not MAINMENU 

        SCREEN = MENU.button_draw(SCREEN)
        MENU.button_hover(MOUSEX, MOUSEY)
        pygame.display.update()
