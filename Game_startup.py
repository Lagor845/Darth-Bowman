import pygame
from pygame import mixer
import time
from pyvidplayer2 import Video
from Asset_classes import *

class Game_startup():
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        mixer.init()

        self.hosting = False
        self.color = Colors()
        self.game_started = False
        self.starting_video = Video("Video/Star Wars.mp4")

        # All clocks
        self.starting_time = time.time()
        self.last_clock = time.time()
        self.clock = pygame.time.Clock()
        self.game_failed = False
        self.menu_screen = pygame.display.set_mode(self.starting_video.current_size, pygame.FULLSCREEN,pygame.RESIZABLE)
        pygame.display.set_caption("Nerd Wars")
        self.X = self.menu_screen.get_width() / 2
        self.Y = self.menu_screen.get_height() / 2

        # Settings

        self.frame_rate = 60
        self.title_growth_modifier = 1 / (self.frame_rate * 0.8)
        self.size = 60

    def Run(self):
        video_started = True
        video_stopped = False

        while self.starting_video.active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if video_started == True:
                            try:
                                self.starting_video.close()
                                video_stopped = True
                            except:
                                pass
                    
            pygame.mouse.set_visible(False)

            fps = self.clock.get_fps()

            self.menu_screen.fill(self.color.black)

            if time.time() - self.starting_time <= 5:
                self.Presented_by_screen(self.size)
            
            elif time.time() - self.starting_time <= 95:

                if self.starting_video.draw(self.menu_screen, (0, 0), force_draw=True) or video_stopped != True:
                    video_started = True

            else:
                self.starting_video.close()
            
            self.clock.tick(self.frame_rate)

            pygame.display.flip()
        
        return "Main menu"
    
    def Presented_by_screen(self,size):
        if size <= 200:
            new_clock = time.time()
            time_since = new_clock - self.last_clock
            size = round((time_since * self.title_growth_modifier + 1) * size)
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render("Paden O'Neal Presents", True, self.color.white, self.color.black)
        textRect = text.get_rect()
        textRect.center = (self.X, self.Y)
        self.menu_screen.blit(text, textRect)

    
    def quit(self):
        pygame.quit()
        quit()