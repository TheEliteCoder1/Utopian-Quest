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
        "descriptor":"Block",
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
        "descriptor":"Block",
        "animation":None,
        "size":(35, 35)
    },
    5:{
        "image":"assets/levelObjects/light_brick.png",
        "descriptor":"Block",
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
        "descriptor":"Enemy",
        "animation":None,
        "size":(35, 35)
    },
    9:{
        "image":"assets/levelObjects/coinGold.png",
        "descriptor":"Currency",
        "animation":None,
        "size":(35, 35)
    },
    10:{
        "image":"assets/levelObjects/bee.png",
        "descriptor":"Enemy",
        "animation":None,
        "size":(35, 35)
    },
    11:{
        "image":"assets/levelObjects/gemBlue.png",
        "descriptor":"Currency",
        "animation":None,
        "size":(35, 35)
    },
    12:{
        "image":"assets/levelObjects/shieldGold.png",
        "descriptor":"Healer",
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
        "descriptor":"Goal",
        "animation":None,
        "size":(35, 35)
    },
    15:{
        "image":"assets/levelObjects/bomb.png",
        "descriptor":"Explodable",
        "animation":None,
        "size":(35, 35)
    },
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