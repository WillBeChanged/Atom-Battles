#!/usr/bin/python

class Parent():
    '''Initialises everything that all child classes use'''
    def __init__(self):
        import pygame, Menus, sys
        self.pygame = pygame
        self.Menus = Menus
        self.sys = sys

        pygame.font.init()
        pygame.image.get_extended()
        pygame.display.init()

        self.original_width, self.original_height = 1500, 900
        self.width, self.height = self.original_width, self.original_height

        self.screen = self.pygame.display.set_mode((self.width, self.height))


class Run(Parent):
    '''Runs game'''
    def __init__(self):
        Parent.__init__(self)
        self.status = "MainMenu"
        self.status_change = True

        self.first_play = False

        self.menu = self.Menus.MainMenu(self.width, self.height, self.first_play)

        self.ref_dict = {
        "MainMenu":self.mainMenu,
        "Options":self.optionsMenu,
        }

        self.mouse_x, self.mouse_y = None, None

    def eventLoop(self):
        self.mouse_x, self.mouse_y = self.pygame.mouse.get_pos()[0], self.pygame.mouse.get_pos()[1]
        for event in self.pygame.event.get():
            self.keys = self.pygame.key.get_pressed()
            return event

    def mainLoop(self):
        while True:
            event = self.eventLoop()
            if self.status != "InGame":
                output = self.menuManager()
                if output == "Exit" and event and event.type == self.pygame.MOUSEBUTTONDOWN:
                    self.exit()
            self.status_change = False
            self.pygame.display.update()

    def menuManager(self):
        return self.ref_dict[self.status]()
        
    def mainMenu(self):
        self.menu.button_draw(self.screen, self.status_change)
        self.menu.button_hover(self.mouse_x, self.mouse_y)
        return self.menu.hovered_button

    def optionsMenu(self):
        pass

    def exit(self):
        self.sys.exit()

Instance = Run()
Instance.mainLoop() 
