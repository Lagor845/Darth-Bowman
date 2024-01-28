import pygame
from Asset_classes import *

class Multiplyer_menu():
    def __init__(self,frame_rate) -> None:
        self.frame_rate = frame_rate
        self.color = Colors()
        self.clock = pygame.time.Clock()

    def Run(self,screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        running = True
        self.background = Background("Images/Backgrounds/Background Image.jpeg",(0,0))
        while running:
            self.screen.fill(self.color.black)
            self.screen.blit(self.background.image,self.background.rect)
            mouse = pygame.mouse.get_pos()
            pygame.mouse.set_visible(True)
            join_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2-50,round(self.width*0.3),round(self.height*0.2),"Join",self.color.red)
            host_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2+150,round(self.width*0.3),round(self.height*0.2),"Host",self.color.red)
            back_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2+350,round(self.width*0.3),round(self.height*0.2),"Back",self.color.red)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        location = "Main Menu"
                        running = False

                    if event.key == pygame.K_SPACE:
                        pass

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if join_button.rect.collidepoint(event.pos):
                        location = "Join menu"
                        Sound("Audio/Sounds/Select.wav")
                        running = False

                    if host_button.rect.collidepoint(event.pos):
                        location = "Host menu"
                        Sound("Audio/Sounds/Select.wav")
                        running = False

                    if back_button.rect.collidepoint(event.pos):
                        location = "Main menu"
                        Sound("Audio/Sounds/Select.wav")
                        running = False

            self.clock.tick(self.frame_rate)
            pygame.display.flip()
        
        return location