#!/usr/bin/python 

def type_create(text, colour, size, font):
    '''Creates text that can be printed on to a screen'''
    created_font = font.SysFont(None, size)
    text = created_font.render(text, True, colour) 
    return text
