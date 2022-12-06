from cryptography.fernet import Fernet # cryptography is not in python's default packages, so 'pip install cryptography' is needed
import hashlib
import pygame # pygame is not in python's default packages, so 'pip install pygame' is needed
import os
import sys
# Imports ^
global sourcedirectory
sourcedirectory = os.path.dirname(os.path.abspath(__file__)) # Notes the directory of the program
# [ITEM]path = os.path.join(sourcedirectory, 'Data/[REST OF PATH]')

pygame.init() # Initiates pygame

swidth, sheight = 740, 740
screen = pygame.display.set_mode((swidth, sheight)) #width, height
pygame.scrap.init() ### Scrap can only be initiatlised after the display set mode command has been done
pygame.key.set_repeat(500, 50)

pygame.display.set_caption('Password Manager')

iconpath = os.path.join(sourcedirectory, 'Data/Images/lock_icon.png')
icon = pygame.image.load(iconpath).convert_alpha()
pygame.display.set_icon(icon)
# Pygame screen configuration ^

def create_message(message, x, y, fontstyle=None):
    if fontstyle is None:
        fontstyle = pygame.font.SysFont(None, 50) # Defaults to a size 50 font
    color = (255, 255, 255)
    messageid = fontstyle.render(message, True, color)
    message_rectid = messageid.get_rect(center = (x, y)) # Message container
    screen.blit(messageid, message_rectid)
    pygame.display.flip()
    return message_rectid

def create_message_topleft(message, x, y, fontstyle=None):
    if fontstyle is None:
        fontstyle = pygame.font.SysFont(None, 50) # Defaults to a size 50 font
    color = (255, 255, 255)
    messageid = fontstyle.render(message, True, color)
    message_rectid = messageid.get_rect(topleft = (x, y)) # Message container
    screen.blit(messageid, message_rectid)
    pygame.display.flip()
    return message_rectid

def first_time(sourcedirectory): # Checks to see if a key already exists
    keypath = os.path.join(sourcedirectory, 'Data/Key/masterkey')
    try:
        with open(keypath, 'rb') as f:
            KEY = f.read()
        return False
    except FileNotFoundError:
        return True


def first_time_SETUP(sourcedirectory):
    def change_input(text):
        textrect = pygame.Rect((0, 200), (740, 100))
        pygame.draw.rect(screen, (0, 0, 0), textrect)
        create_message(f'{text}', 370, 240)

    def menu_message(text):
        menu.fill((0, 0, 0))
        screen.blit(menu, (0,0))
        create_message('Please enter your master password', 370, 130)
        create_message(f'{text}', 370, 240)
        create_message('NOTE: This password cannot be changed', 370, 370)
        create_message('DO NOT LOSE IT', 370, 410)

    def last_chance():
        menu_message(text)
        create_message('Do you want to make this your password?', 370, 480)
        message_rectYES = create_message('YES', 310, 560)
        message_rectNO = create_message('NO', 430, 560)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos() # mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if message_rectYES.collidepoint(mouse[0], mouse[1]):
                            return True
                        elif message_rectNO.collidepoint(mouse[0], mouse[1]):
                            return False

    def add_masterpassword(text):
        keypath = os.path.join(sourcedirectory, 'Data/Key/masterkey')
        salt = os.urandom(32)
        KEY = hashlib.pbkdf2_hmac(
            'sha256', # Define the algorithm
            text.encode('utf-8'), # Converts the given password to bytes
            salt, # Add thyme
            100000
            )
        SaltPassword = salt + KEY
        with open(keypath, 'wb') as f:
            f.write(SaltPassword)

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
                        change_input(text)
                    elif event.key == pygame.K_RETURN:
                        create_password = last_chance()
                        if create_password == True:
                            add_masterpassword(text)
                            return
                        else:
                            change_input(text)
                    else:
                        text += event.unicode
                        change_input(text)
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


def LOGIN(sourcedirectory):
    def encrypt_text(text, salt):
        KEY = hashlib.pbkdf2_hmac(
            'sha256', # Define the algorithm
            text.encode('utf-8'), # Converts the given password to bytes
            salt, # Add thyme
            100000
            )
        return KEY

    def change_input(text, textrect):
        pygame.draw.rect(screen, (0, 0, 0), textrect)
        create_message(f'{text}', 370, 240)

    keypath = os.path.join(sourcedirectory, 'Data/Key/masterkey')
    with open(keypath, 'rb') as f:
        salt_key = f.read()
        salt = salt_key[:32] # 32 is specified because that is the length of the salt
        stored_key = salt_key[32:]
    
    menu = pygame.Surface((screen.get_size()))
    menu.fill((0, 0, 0))
    screen.blit(menu, (0,0))
    text = ''
    create_message('Please enter your master password', 370, 130)
    textrect = pygame.Rect((0, 200), (740, 200))

    print('password = TEST_123999!!!#')
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        change_input(text, textrect)
                    elif event.key == pygame.K_RETURN:
                        created_key = encrypt_text(text, salt)
                        if created_key == stored_key:
                            return text
                        else:
                            create_message('That password is incorrect, try again', 370, 300)
                    else:
                        text += event.unicode
                        change_input(text, textrect)
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()





def MAIN(sourcedirectory):
    def drawcontent(surface, topvalue, nameslist):
        color = (73,73,73)

        # iconpath = os.path.join(sourcedirectory, 'Data/Images/lock_icon.png')
        # icon = pygame.image.load(iconpath).convert_alpha()
        editpath = os.path.join(sourcedirectory, 'Data/Images/edit_icon.png')
        editicon = pygame.image.load(editpath).convert_alpha()
        viewpath = os.path.join(sourcedirectory, 'Data/Images/view_icon.png')
        viewicon = pygame.image.load(viewpath).convert_alpha()
        deletepath = os.path.join(sourcedirectory, 'Data/Images/delete_icon.png')
        deleteicon = pygame.image.load(deletepath).convert_alpha()
        # logopath = os.path.join(sourcedirectory, 'Data/Images/logo.png')
        # logo = pygame.image.load(logopath).convert_alpha()

        # for x in range(len(nameslist)):
        #     text = nameslist[x]
        #     drawrectangle(menu, 15, (((x+1)*115)+35), 640, 100, text)
        entityrects = []
        editrects = []
        viewrects = []
        deleterects = []
        for x in range(5):
            text = nameslist[x + topvalue]
            rect, editiconrect, viewiconrect, deleteiconrect = drawrectangle(surface, 15, (((x+1)*115)+35), 640, 100, text, color, editicon, viewicon, deleteicon)
            entityrects.append((rect, x + topvalue))
            editrects.append((editiconrect, x + topvalue))
            viewrects.append((viewiconrect, x + topvalue))
            deleterects.append((deleteiconrect, x + topvalue))
           
        # surfacehitbox = surface.get_rect()
        # surface.fill((16, 16, 16)) # outline colour
        # surface.fill((90, 90, 90), surfacehitbox.inflate(-10, -10)) # fill colour
        newboxsurface = pygame.Surface((262, 70))
        newboxhitbox = newboxsurface.get_rect()
        newboxsurface.fill((16, 16, 16))
        newboxsurface.fill((90, 90, 90), newboxhitbox.inflate(-10, -10))
        surface.blit(newboxsurface, (440, 34))

        screen.blit(surface, (0,0))
        newbox = create_message_topleft('New Entry', 450, 44, fontstyle = pygame.font.SysFont(None, 70)) # <rect(50, 44, 242, 50)>
        create_message_topleft('Zenyth Inc.', 50, 44, fontstyle = pygame.font.SysFont(None, 70))
        pygame.display.flip()
        return entityrects, editrects, viewrects, deleterects, newbox.inflate(20, 20)


    def drawrectangle(surface, left, top, width, height, text, color, editicon, viewicon, deleteicon):
        if color is None:
            color = (100, 100, 100)

        #### IMPORTANT!!!!! only 5 rectangles can be on the screen at once!!! remember this!! ####
        rectanglerect = pygame.Rect(left, top, width, height)
        rectcentre = rectanglerect.topleft
        rectcentrestatic = list(rectcentre)
        rectcentrestatic[0] += 40
        rectcentrestatic[1] += 35
        pygame.draw.rect(surface, color, rectanglerect)
        fontstyle = pygame.font.SysFont(None, 50) # Defaults to a size 50 font
        fontcolor = (220,220,220)
        messageid = fontstyle.render(text, True, fontcolor)
        surface.blit(messageid, rectcentrestatic)

        editicon = pygame.transform.scale(editicon, (75, 75))
        editrect = editicon.get_rect()
        editrect = editrect.move((410, top + 10))
        surface.blit(editicon, editrect)

        viewicon = pygame.transform.scale(viewicon, (85, 85))
        viewrect = viewicon.get_rect()
        viewrect = viewrect.move((480, top + 5))
        surface.blit(viewicon, viewrect)

        deleteicon = pygame.transform.scale(deleteicon, (75, 75))
        deleterect = deleteicon.get_rect()
        deleterect = deleterect.move((570, top + 10))
        surface.blit(deleteicon, deleterect)

        screen.blit(surface, (0,0))
        pygame.display.flip()
        return rectanglerect, editrect, viewrect, deleterect

    def importvalues(sourcedirectory):
        listpath = os.path.join(sourcedirectory, 'Data/List/names.txt')
        with open(listpath, 'r') as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
        return lines

    def view_entity(account_name):
        fontstyletitle = pygame.font.SysFont(None, 80)
        fontstylebody = pygame.font.SysFont(None, 50)
        entitypath = os.path.join(sourcedirectory, f'Data/Passwords/{account_name}')
        with open(entitypath, 'r') as f:
            lines = f.readlines()
            filelines = [line.rstrip() for line in lines]
            usernamerect = create_message_topleft(filelines[0], 90, 340, fontstylebody) ########## CHANGE HERE TO DECRYPT FOR READING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##########
            usernamerectstatic = list(usernamerect.topright)
            passwordrect = create_message_topleft(filelines[1], 90, 520, fontstylebody)
            passwordrectstatic = list(passwordrect.topright)

        surface = pygame.Surface((650, 565))
        surfaceinvisiblerect = pygame.Rect(45, 150, 650, 565) 
        clippath = os.path.join(sourcedirectory, 'Data/Images/clipboard_icon.png')
        clipboardicon = pygame.image.load(clippath).convert_alpha()
        exitpath = os.path.join(sourcedirectory, 'Data/Images/exit_icon.png')
        exiticon = pygame.image.load(exitpath).convert_alpha()

        surfacehitbox = surface.get_rect()
        surface.fill((16, 16, 16)) # outline colour
        surface.fill((90, 90, 90), surfacehitbox.inflate(-10, -10)) # fill colour

        exiticon = pygame.transform.scale(exiticon, (75, 75))
        exitrect = exiticon.get_rect()
        exitrect = exitrect.move((555, 20))
        surface.blit(exiticon, exitrect)

        clipboardicon = pygame.transform.scale(clipboardicon, (60, 60))
        clipboardrectusername = clipboardicon.get_rect()
        clipboardrectusername = clipboardrectusername.move((usernamerectstatic[0] - 45), (usernamerectstatic[1] - 165))
        surface.blit(clipboardicon, clipboardrectusername)
        clipboardrectpassword = clipboardicon.get_rect()
        clipboardrectpassword = clipboardrectpassword.move((passwordrectstatic[0] - 45), (passwordrectstatic[1] - 165))
        surface.blit(clipboardicon, clipboardrectpassword)


        screen.blit(surface, (45, 150)) ######IMPORTANT!!! SINCE SURFACE IS NOT BLITTED AT (0,0), ALL COLLIDEPOINTS MUST BE OFFSETTED BY -45, -150######
        create_message(account_name, 370, 200, fontstyletitle)
        create_message_topleft('Username', 80, 280, fontstylebody)
        usernamerect = create_message_topleft(filelines[0], 90, 340, fontstylebody)
        create_message_topleft('Password', 80, 460, fontstylebody)
        passwordrect = create_message_topleft(filelines[1], 90, 520, fontstylebody)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not surfaceinvisiblerect.collidepoint((mousepos[0]), (mousepos[1])):
                        return
                    if pygame.mouse.get_pressed()[0]:
                        if exitrect.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            return
                        if clipboardrectusername.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            pygame.scrap.put(pygame.SCRAP_TEXT, filelines[0].encode('utf-8'))
                        if clipboardrectpassword.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            pygame.scrap.put(pygame.SCRAP_TEXT, filelines[1].encode('utf-8'))

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


    def edit_entity(account_name):
        def change_file(entitypath, filelines, linechange, textrect):
            def change_text(text, drawover, textrectstatic):
                pygame.draw.rect(screen, (90, 90, 90), drawover)
                create_message_topleft(text, textrectstatic[0], textrectstatic[1], fontstyle = pygame.font.SysFont(None, 50))
            textrectstatic = [textrect[0], textrect[1], textrect[2], textrect[3]]
            drawover = pygame.Rect(textrectstatic[0], textrectstatic[1], 600, textrectstatic[3])
            text = filelines[linechange]
            active = True
            addedtext = create_message('Press enter to save', 370, 690, fontstylebody)
            while active == True:
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                                change_text(text, drawover, textrectstatic)
                            elif event.key == pygame.K_RETURN:
                                active = False
                            else:
                                text += event.unicode
                                change_text(text, drawover, textrectstatic)
                    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            filelines[linechange] = text
            #edit text file
            with open(entitypath, 'wb') as f:
                f.write((filelines[0] + '\n' + filelines[1]).encode('utf-8'))  ########## CHANGE HERE ASWELL FOR ENCRYPTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##########
            pygame.draw.rect(screen, (90, 90, 90), addedtext)
            pygame.display.flip()
            return filelines

        fontstyletitle = pygame.font.SysFont(None, 80)
        fontstylebody = pygame.font.SysFont(None, 50)
        entitypath = os.path.join(sourcedirectory, f'Data/Passwords/{account_name}')
        with open(entitypath, 'r') as f:
            lines = f.readlines()
            filelines = [line.rstrip() for line in lines]
            usernamerect = create_message_topleft(filelines[0], 90, 340, fontstylebody)
            usernamerectstatic = list(usernamerect.topright)
            passwordrect = create_message_topleft(filelines[1], 90, 520, fontstylebody)
            passwordrectstatic = list(passwordrect.topright)   ########## CHANGE HERE TO DECRYPT FOR READING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##########
        
        surface = pygame.Surface((650, 565))
        surfaceinvisiblerect = pygame.Rect(45, 150, 650, 565) 
        exitpath = os.path.join(sourcedirectory, 'Data/Images/exit_icon.png')
        exiticon = pygame.image.load(exitpath).convert_alpha()

        surfacehitbox = surface.get_rect()
        surface.fill((16, 16, 16)) # outline colour
        surface.fill((90, 90, 90), surfacehitbox.inflate(-10, -10)) # fill colour

        exiticon = pygame.transform.scale(exiticon, (75, 75))
        exitrect = exiticon.get_rect()
        exitrect = exitrect.move((555, 20))
        surface.blit(exiticon, exitrect)

        screen.blit(surface, (45, 150))
        create_message(account_name, 370, 200, fontstyletitle)
        create_message_topleft('Username', 80, 280, fontstylebody)
        usernamerect = create_message_topleft(filelines[0], 90, 340, fontstylebody)
        create_message_topleft('Password', 80, 460, fontstylebody)
        passwordrect = create_message_topleft(filelines[1], 90, 520, fontstylebody)
        create_message('Click on text to edit it', 370, 660, fontstylebody)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not surfaceinvisiblerect.collidepoint((mousepos[0]), (mousepos[1])):
                        return
                    if pygame.mouse.get_pressed()[0]:
                        if exitrect.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            return
                        if usernamerect.collidepoint(mousepos[0], mousepos[1]):
                            filelines = change_file(entitypath, filelines, 0, usernamerect)
                        if passwordrect.collidepoint(mousepos[0], mousepos[1]):
                            filelines = change_file(entitypath, filelines, 1, passwordrect)
                            edit_entity(account_name)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def addnew_entity():
        def addto_files(enteredlist, listpath, entitypath):

            with open(entitypath, 'wb') as f:
                f.write((enteredlist[1] + '\n' + enteredlist[2]).encode('utf-8'))
            with open(listpath, 'ab') as f:
                f.write(('\n' + enteredlist[0]).encode('utf-8'))
        def change_text(text, changequestion):
            if changequestion == True:
                changerect = pygame.Rect(50, 260, 640, 210)
                text = ''
            else:
                changerect = pygame.Rect(50, 350, 640, 100)
            pygame.draw.rect(screen, (90, 90, 90), changerect)
            create_message(f'{text}', 375, 370)
            pygame.display.flip()
            return text
        fontstyletitle = pygame.font.SysFont(None, 80)
        fontstylebody = pygame.font.SysFont(None, 50)
        surface = pygame.Surface((650, 565))
        surfaceinvisiblerect = pygame.Rect(45, 150, 650, 565) 
        exitpath = os.path.join(sourcedirectory, 'Data/Images/exit_icon.png')
        exiticon = pygame.image.load(exitpath).convert_alpha()

        surfacehitbox = surface.get_rect()
        surface.fill((16, 16, 16)) # outline colour
        surface.fill((90, 90, 90), surfacehitbox.inflate(-10, -10)) # fill colour

        exiticon = pygame.transform.scale(exiticon, (75, 75))
        exitrect = exiticon.get_rect()
        exitrect = exitrect.move((555, 20))
        surface.blit(exiticon, exitrect)

        screen.blit(surface, (45, 150))
        create_message('Add new', 370, 200, fontstyletitle)
        addedtext = create_message('Press enter to save', 370, 690, fontstylebody)
        pygame.display.flip()

        enteredlist = []
        thetriplelist = ['name', 'username', 'password']
        choose = 0
        text = ''

        create_message(f'Please enter the {thetriplelist[choose]}', 375, 290)
        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        text = change_text(text, changequestion=False)
                    elif event.key == pygame.K_RETURN:
                        if choose == 2:
                            enteredlist.append(text)
                            print(enteredlist)
                            addto_files(enteredlist, listpath = os.path.join(sourcedirectory, 'Data/List/names.txt'), entitypath = os.path.join(sourcedirectory, f'Data/Passwords/{enteredlist[0]}'))
                            return
                        else:
                            choose += 1
                            enteredlist.append(text)
                            text = change_text(text, changequestion=True)
                            create_message(f'Please enter the {thetriplelist[choose]}', 375, 290)
                            pygame.display.flip()

                    else:
                        text += event.unicode
                        text = change_text(text, changequestion=False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not surfaceinvisiblerect.collidepoint((mousepos[0]), (mousepos[1])):
                        return
                    if pygame.mouse.get_pressed()[0]:
                        if exitrect.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    def delete_entity(account_name):
        surface = pygame.Surface((650, 350))
        surfaceinvisiblerect = pygame.Rect(45, 150, 650, 350)
        exitpath = os.path.join(sourcedirectory, 'Data/Images/exit_icon.png')
        exiticon = pygame.image.load(exitpath).convert_alpha()
        fontstyletitle = pygame.font.SysFont(None, 80)
        fontstylebody = pygame.font.SysFont(None, 50) 

        listpath = os.path.join(sourcedirectory, 'Data/List/names.txt')
        entitypath = os.path.join(sourcedirectory, f'Data/Passwords/{account_name}')

        surfacehitbox = surface.get_rect()
        surface.fill((16, 16, 16)) # outline colour
        surface.fill((90, 90, 90), surfacehitbox.inflate(-10, -10)) # fill colour

        exiticon = pygame.transform.scale(exiticon, (75, 75))
        exitrect = exiticon.get_rect()
        exitrect = exitrect.move((555, 20))
        surface.blit(exiticon, exitrect)

        screen.blit(surface, (45, 150))
        create_message('Delete', 370, 200, fontstyletitle)
        create_message('Are you sure you want to', 370, 260, fontstylebody)
        create_message('delete this entry?', 370, 300, fontstylebody)
        yesbutton = create_message('YES', 150, 400, fontstylebody)
        nobutton = create_message('NO', 580, 400, fontstylebody)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                mousepos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not surfaceinvisiblerect.collidepoint((mousepos[0]), (mousepos[1])):
                        return
                    if pygame.mouse.get_pressed()[0]:
                        if exitrect.collidepoint((mousepos[0] - 45), (mousepos[1] - 150)):
                            return
                        if nobutton.collidepoint((mousepos[0]), (mousepos[1])):
                            return
                        if yesbutton.collidepoint((mousepos[0]), (mousepos[1])):
                            with open(listpath, 'r+') as f:
                                accounts = f.read().split('\n')
                                f.seek(0)
                                f.truncate()
                                accounts = [account for account in accounts if account and account != account_name] # ¯\_(ツ)_/¯ thanks meic
                                f.write('\n'.join(accounts))
                            os.remove(entitypath) #bye bye
                            return

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    menu = pygame.Surface((screen.get_size()))
    menu.fill((30, 30, 30))
    header = pygame.Rect(0, 0, 740, 135)
    pygame.draw.rect(menu, (47, 47, 47), header)
    screen.blit(menu, (0,0))
    pygame.display.flip()

    toprectangle = 0
    nameslist = importvalues(sourcedirectory)
    # for x in range(len(nameslist)):
    #     text = nameslist[x]
    #     drawrectangle(menu, 15, (((x+1)*115)+35), 640, 100, text)

    entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
    while True:
        for event in pygame.event.get():
            mousepos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if newhitbox.collidepoint(mousepos[0], mousepos[1]):
                            addnew_entity()
                            nameslist = importvalues(sourcedirectory)
                            entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
                        for rect, x in edithitboxes:
                            if rect.collidepoint(mousepos[0], mousepos[1]):
                                edit_entity(nameslist[x])
                                entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
                        for rect, x in viewhitboxes:
                            if rect.collidepoint(mousepos[0], mousepos[1]):
                                view_entity(nameslist[x])
                                entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
                        for rect, x in deletehitboxes:
                            if rect.collidepoint(mousepos[0], mousepos[1]):
                                delete_entity(nameslist[x])
                                nameslist = importvalues(sourcedirectory)
                                if toprectangle == 0:
                                    pass
                                else:
                                    toprectangle -= 1
                                entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    if toprectangle == 0:
                        pass
                    else:
                        toprectangle -= 1
                elif event.y == -1:
                    if toprectangle > ((len(nameslist)) - 6):
                        pass
                    else:
                        toprectangle += 1
                entityhitboxes, edithitboxes, viewhitboxes, deletehitboxes, newhitbox = drawcontent(menu, toprectangle, nameslist)
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         if toprectangle == 0:
            #             pass
            #         else:
            #             toprectangle -= 1
            #     if event.key == pygame.K_DOWN:
            #         if toprectangle > ((len(nameslist)) - 6): #if scrollwheel doesnt work uncomment this section :)
            #             pass
            #         else:
            #             toprectangle += 1
            #     entityhitboxes, edithitboxes, viewhitboxes, newhitbox, deletehitbox = drawcontent(menu, toprectangle, nameslist)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def encryption_file(credentialsarray):
    salt = os.urandom(32) #pepper
    KEY = hashlib.pbkdf2_hmac(
        'sha256', # Define the algorithm
        raw_password.encode('utf-8'), # Converts the given password to bytes
        salt, # Add thyme
        100000
    )


new_user = first_time(sourcedirectory)
if new_user == True:
    first_time_SETUP(sourcedirectory)
else:
    global raw_password
    # raw_password = LOGIN(sourcedirectory)
MAIN(sourcedirectory)

