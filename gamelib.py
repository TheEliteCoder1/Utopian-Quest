import pygame, os
pygame.init()
pygame.font.init()

"""This module is a library that provides colors, fonts, assets, settings & utility functions for the game."""

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (235, 0, 0)
GREEN = (0, 235, 0)
BLUE = (10, 30, 255)

FONTS = {
    'game_info':os.path.abspath('assets/fonts/oxygene.ttf')
}

LEVEL_OBJECTS = {
    0:{
        "image":"assets/levelObjects/grass.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    1:{
        "image":"assets/levelObjects/bush.png",
        "descriptor":"Decor",
        "animation":None, 
        "size":(35, 35)
    },
    2:{
        "image":"assets/levelObjects/mushroomRed.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    3:{
        "image":"assets/levelObjects/plant.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    4:{
        "image":"assets/levelObjects/dark_brick.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    5:{
        "image":"assets/levelObjects/light_brick.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    6:{
        "image":"assets/levelObjects/fence.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    7:{
        "image":"assets/levelObjects/chain.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    8:{
        "image":"assets/levelObjects/bat.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    9:{
        "image":"assets/levelObjects/coinGold.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    10:{
        "image":"assets/levelObjects/bee.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    11:{
        "image":"assets/levelObjects/gemBlue.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    12:{
        "image":"assets/levelObjects/shieldGold.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    13:{
        "image":"assets/levelObjects/cloud3.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(45, 35)
    },
    14:{
        "image":"assets/levelObjects/keyRed.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
    15:{
        "image":"assets/levelObjects/bomb.png",
        "descriptor":"Decor",
        "animation":None,
        "size":(35, 35)
    },
}

PLAYERS = {
    "Yoro": {
        # sorted -> animation order: i.e, [...]/walking/p1_01 then [...]/walking/p1_02     
        "walking":sorted(["assets/player/p1/walking/"+f for f in os.listdir("assets/player/p1/walking") if os.path.isfile(os.path.join("assets/player/p1/walking", f))]),
        # all extras
        "extras":sorted(["assets/player/p1/extras/"+f for f in os.listdir("assets/player/p1/extras") if os.path.isfile(os.path.join("assets/plater/p1/extras", f))]),
        # individual extras
        "hurt":"assets/player/p1/extras/p1_hurt.png",
        "duck":"assets/player/p1/extras/p1_duck.png",
        "front":"assets/player/p1/extras/p1_front.png",
        "jump":"assets/player/p1/extras/p1_jump.png",
        "stand":"assets/player/p1/extras/p1_stand.png"
    },
    "Higo": {
        "walking":sorted(["assets/player/p2/walking/"+f for f in os.listdir("assets/player/p2/walking") if os.path.isfile(os.path.join("assets/player/p2/walking", f))]),
        "extras":sorted(["assets/player/p2/extras/"+f for f in os.listdir("assets/player/p2/extras") if os.path.isfile(os.path.join("assets/plater/p2/extras", f))]),
        "hurt":"assets/player/p2/extras/p2_hurt.png",
        "duck":"assets/player/p2/extras/p2_duck.png",
        "front":"assets/player/p2/extras/p2_front.png",
        "jump":"assets/player/p2/extras/p2_jump.png",
        "stand":"assets/player/p2/extras/p2_stand.png"
    },
    "Parto": {
        "walking":sorted(["assets/player/p3/walking/"+f for f in os.listdir("assets/player/p3/walking") if os.path.isfile(os.path.join("assets/player/p3/walking", f))]),
        "extras":sorted(["assets/player/p3/extras/"+f for f in os.listdir("assets/player/p3/extras") if os.path.isfile(os.path.join("assets/plater/p3/extras", f))]),
        "hurt":"assets/player/p3/extras/p3_hurt.png",
        "duck":"assets/player/p3/extras/p3_duck.png",
        "front":"assets/player/p3/extras/p3_front.png",
        "jump":"assets/player/p3/extras/p3_jump.png",
        "stand":"assets/player/p3/extras/p3_stand.png"
    }
}

def draw_text(screen: pygame.Surface, font_file: str, text: str, 
    font_size: int, color: tuple, pos: tuple, backg=None):
    """Draws text to the screen given a font file and text."""
    font = pygame.font.Font(font_file, font_size)
    if backg == None:
        t = font.render(text, True, color)
    t = font.render(text, True, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def get_usefull_constants(screen: pygame.Surface) -> dict:
    """Get usefull parts of the screen as variables returned in a dict where key is the variable name alongside it's value."""
    center_screen_x = screen.get_width() // 2
    center_screen_y = screen.get_height() // 2
    center_screen_pos = (center_screen_x, center_screen_y)
    margin_y = 50 
    bottom_y = screen.get_height()-50
    constants_dict = {
        "center_screen_x":center_screen_x, 
        "center_screen_y":center_screen_y, 
        "margin_y":margin_y,
        "center_screen_pos":center_screen_pos,
        "bottom_y":bottom_y
    }
    return constants_dict