import pygame
from pygame import mixer
import os

class Music():
    def Start_star_wars_music(self,volume):
        mixer.music.load("Audio/Music/Star Wars.mp3")
        mixer.music.set_volume(volume)
        mixer.music.play()
        return True

    def Stop_star_wars_music(self):
        mixer.music.stop()
        return False

class Sound():
    def __init__(self,sound_loc) -> None:
        sound = mixer.Sound(sound_loc)
        mixer.Sound.play(sound)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        infoObject = pygame.display.Info()
        self.image = pygame.transform.scale(self.image, (infoObject.current_w, infoObject.current_h))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Button():
    def __init__(self,screen,font_size,text_color,locx,locy,width,height,text,background = None) -> None:
        self.text = text
        self.text_class = Text(screen,font_size,text_color,locx,locy,text)
        self.rect = self.text_class.textRect
        if Background == None:
            pygame.draw.rect(screen,background,self.rect)
        

class Text():
    def __init__(self,screen,font_size,text_color,locx,locy,text) -> None:
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render(text, True, text_color)
        self.textRect = text.get_rect()
        self.textRect.center = (locx, locy)
        screen.blit(text, self.textRect)

class Colors():
    def __init__(self) -> None:
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.black = (0,0,0)
        self.red = (255,0,0)

class Character(pygame.sprite.Sprite):
    def __init__(self, name, emote_animation, hurt_animation,walk_animation_down,walk_animation_up,walk_animation_horizontal,Emote_time):
        super().__init__()
        self.name = name
        self.emote_animation = emote_animation
        self.hurt_animation = hurt_animation
        self.walk_animation_down = walk_animation_down
        self.walk_animation_up = walk_animation_up
        self.walk_animation_horizontal = walk_animation_horizontal
        self.emote_time = Emote_time
        self.emote_time_between = (self.emote_time / len(emote_animation)) * 10
        self.animation_progress = 0
        self.emote_in_progress = False
        self.last_emote_frame_time = pygame.time.get_ticks()
        self.current_frame = self.walk_animation_down[0]

    def Emote(self):
        if self.emote_in_progress == True:
            if self.last_emote_frame_time >= self.emote_time_between:
                self.current_frame = self.emote_animation[self.animation_progress]
                self.animation_progress += 1

    def Walk_up(self):
        self.Erase_emote_progress()

    def Walk_down(self):
        self.Erase_emote_progress()

    def Walk_horizontal(self):
        self.Erase_emote_progress()

    def Erase_emote_progress(self):
        if self.emote_in_progress == True:
            self.emote_in_progress = False

class Character_creator():
    def __init__(self, character_map) -> object:
        self.character_map = character_map
        with open(f"Text Files/Character files/{self.character_map}","r") as file:
            file_info = file.read()
            self.file_lines = file_info.split("\n")

    def Create(self):
        After_space = True
        Emote_time = "Hello This Failed"
        info = {
            "Name" : [],
            "Emote" : [],
            "Hurt" : [],
            "Walking_down" : [],
            "Walking_up" : [],
            "Walking_horizontal" : []
        }
        for line in self.file_lines:
            if After_space == True:
                if line == "Name":
                    next = "Name"
                    After_space = False

                elif "Emote" in line:
                    Emote_time = float(line.split(",")[1].replace(" ",""))
                    next = "Emote"
                    After_space = False

                elif line == "Hurt":
                    After_space = False
                    next = "Hurt"

                elif line == "Walking_down":
                    next = "Walking_down"
                    After_space = False

                elif line == "Walking_up":
                    next = "Walking_up"
                    After_space = False

                elif line == "Walking_horizontal":
                    next = "Walking_horizontal"
                    After_space = False

            elif line == "":
                After_space = True
            
            else:
                info[next].append(line)

        name = info["Name"]
        emote_animation = info["Emote"]
        hurt_animation = info["Hurt"]
        walk_animation_down = info["Walking_down"]
        walk_animation_up = info["Walking_up"]
        walk_animation_horizontal = info["Walking_horizontal"]

        character = Character(name, emote_animation, hurt_animation,walk_animation_down,walk_animation_up,walk_animation_horizontal,Emote_time)
        return character