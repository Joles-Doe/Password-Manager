from cryptography.fernet import Fernet # cryptography is not in python's default packages, so 'pip install cryptography' is needed
import hashlib
import pygame # pygame is not in python's default packages, so 'pip install pygame' is needed
import os
import sys
# Imports ^
sourcedirectory = os.path.dirname(os.path.abspath(__file__)) # Notes the directory of the program
# [ITEM]path = os.path.join(sourcedirectory, 'Data/[REST OF PATH]')

pygame.init() # Initiates pygame

swidth, sheight = 740, 740
screen = pygame.display.set_mode((swidth, sheight)) #width, height

pygame.display.set_caption('Password Manager')

iconpath = os.path.join(sourcedirectory, 'Data/Images/lock_icon.png')
icon = pygame.image.load(iconpath).convert_alpha()
pygame.display.set_icon(icon)
# Pygame screen configuration ^

def create_message(message, x, y, fontstyle=None):
    if fontstyle is None:
        fontstyle = pygame.font.SysFont(None, 50) # Defaults to a size 70 font
    messageid = fontstyle.render(message, True, (255, 255, 255))
    message_rectid = messageid.get_rect(center = (x, y)) # Message container
    screen.blit(messageid, message_rectid)
    pygame.display.flip()
    return message_rectid


def first_time(sourcedirectory):
    keypath = os.path.join(sourcedirectory, 'Data/Key/masterkey')
    try:
        with open(keypath, 'rb') as f:
            KEY = f.read()
        return False
    except FileNotFoundError:
        return True

def first_time_SETUP(sourcedirectory):
    def menu_message(text):
        menu.fill((0, 0, 0))
        screen.blit(menu, (0,0))
        create_message('Please enter your master password', 370, 130)
        create_message(f'{text}', 370, 240)
        create_message('NOTE: This password cannot be changed', 370, 370)
        create_message('DO NOT LOSE IT', 370, 410)
    menu = pygame.Surface((screen.get_size()))
    menu.fill((0, 0, 0))
    screen.blit(menu, (0,0))
    text = ''
    menu_message(text)
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        menu_message(text)
                    else:
                        text += event.unicode
                        menu_message(text)
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

new_user = first_time(sourcedirectory)
if new_user == True:
    first_time_SETUP(sourcedirectory)