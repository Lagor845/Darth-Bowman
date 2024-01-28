import pygame
from Asset_classes import *

class Main_menu():
    def __init__(self,frame_rate) -> None:
        self.color = Colors()
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate

    def Run(self,screen):
        self.screen = screen

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.background = Background("Images/Backgrounds/Background Image.jpeg",(0,0))
        self.running = True
        while self.running:
            self.screen.fill(self.color.black)
            self.screen.blit(self.background.image,self.background.rect)
            mouse = pygame.mouse.get_pos()
            pygame.mouse.set_visible(True)
            singleplayer_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2-50,round(self.width*0.3),round(self.height*0.2),"Single",self.color.red)
            multiplayer_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2+150,round(self.width*0.3),round(self.height*0.2),"Local Multiplayer",self.color.red)
            quit_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2+350,round(self.width*0.3),round(self.height*0.2),"Quit",self.color.red)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        self.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if singleplayer_button.rect.collidepoint(event.pos):
                        location = "Singleplayer menu"
                        Sound("Audio/Sounds/Select.wav")
                        self.running = False

                    if multiplayer_button.rect.collidepoint(event.pos):
                        location = "Multiplayer menu"
                        Sound("Audio/Sounds/Select.wav")
                        self.running = False

                    if quit_button.rect.collidepoint(event.pos):
                        Sound("Audio/Sounds/Select.wav")
                        self.quit()

            self.clock.tick(self.frame_rate)
            pygame.display.flip()
        
        return location
    
    def quit(self):
        pygame.quit()
        quit()