from Game_startup import Game_startup
from Main_menu import Main_menu
from Multiplayer_menu import Multiplyer_menu
from Singleplayer_menu import Singleplayer_menu
from Host_menu import Host_menu
from Join_menu import Join_menu
from Asset_classes import *
import pygame

# Game Settings
with open("Text Files/settings.config","r") as file:
    all_settings = []
    file_contents = file.read()
    settings = file_contents.split("\n")
    for setting in settings:
        all_settings.append(setting.strip().split("="))
    frame_rate = int(all_settings[0][1])
    name = all_settings[1][1]
    character = all_settings[2][1].replace(" ","")

character_dictionary = {}
files = os.scandir("Text Files/Character files/")
for file in files:
    with open(f"Text Files/Character files/{file.name}","r") as document:
        name = document.read().split("\n")[1].replace(" ","")
    character_dictionary[name] = file.name

game_areas = {
    "Game Startup" : Game_startup(),
    "Main menu" : Main_menu(frame_rate),
    "Singleplayer menu" : Singleplayer_menu(frame_rate),
    "Multiplayer menu" : Multiplyer_menu(frame_rate),
    "Host menu" : Host_menu(frame_rate,character,name,character_dictionary),
    "Join menu" : Join_menu(frame_rate,character,name)
}

game_areas["Game Startup"].Run()

def Menus():
    Music().Start_star_wars_music(5)
    location = "Main menu"
    pygame.display.quit()
    pygame.display.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN,pygame.HWSURFACE | pygame.DOUBLEBUF)
    while True:
        if location == "Local game":
            pass

        elif location == "Multiplayer game":
            pass

        else:
            location = game_areas[location].Run(screen)

Menus()