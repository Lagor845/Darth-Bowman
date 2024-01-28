from Asset_classes import *
import socket
from threading import Thread

class Join_menu():
    def __init__(self,frame_rate,character,name) -> None:
        self.color = Colors()
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_ip = None
        self.character = character
        self.name = name
        self.alert_too_full = False
        self.leaving_page = True
        self.players = {

        }

    def Run(self,screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        input_rect = pygame.Rect(self.width/2,self.height/3,600,100)
        base_font = pygame.font.Font(None, 100)
        user_text = ""
        active = False
        connected = False
        self.running = True
        self.background = Background("Images/Backgrounds/Background Image.jpeg",(0,0))

        while self.running:
            self.screen.fill(self.color.black)
            self.screen.blit(self.background.image,self.background.rect)
            pygame.mouse.set_visible(True)
            if connected == True:
                Text(self.screen,50,self.color.white,self.width/2,self.height/10,"Server found")
            elif connected != True:
                start_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2 + 100,200,100 + round(self.height*0.2),"Start",self.color.red)
            back_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/2+350,100,100,"Back",self.color.red)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:

                    if active:

                        if event.key == pygame.K_BACKSPACE: 
                            # get text input from 0 to -1 i.e. end. 
                            user_text = user_text[:-1]

                        elif event.key == pygame.K_RETURN:
                            connected = self.Search(user_text)

                        else:
                            user_text += event.unicode


                    else:

                        if event.key == pygame.K_ESCAPE:
                            location = "Main menu"
                            running = False
                            if self.server_ip != None:
                                self.client.send("Quit".encode("utf-8"))

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if input_rect.collidepoint(event.pos): 
                        active = True

                    else: 
                        active = False

                    if start_button.rect.collidepoint(event.pos):
                        connected = self.Search(user_text)
                        Sound("Audio/Sounds/Select.wav")

                    if back_button.rect.collidepoint(event.pos): 
                        location = "Main menu"
                        running = False
                        Sound("Audio/Sounds/Select.wav")

            if active:

                color = self.color.blue

            else:

                color = self.color.white
            
            pygame.draw.rect(self.screen, color, input_rect)

            text_surface = base_font.render(user_text, True, self.color.black,self.color.white)
            
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            
            input_rect.w = max(500, text_surface.get_width()+10)

            self.clock.tick(self.frame_rate)

            pygame.display.flip()
        
        return location
    
    def Search(self,ip):
        # Tries to connect to server
        maybe_connected = self.client.connect_ex((ip,56656))
        print(maybe_connected)
        if maybe_connected == 0:
            # Waits to see if server has enough room
            msg = self.client.recv(2048).decode("utf-8")
            print(msg)
            if msg == "Accepted":
                self.server_ip = ip

                # Send player details formatted as character,name
                self.client.send(f"{self.character},{self.name}".encode("utf-8"))

                # Recv player num formated as 0x0001,num
                msg = self.client.recv(2048).decode("utf-8")
                if msg[0] == "0x0001":
                    self.player_num = msg[1]
                
                # Recvs all current players from server and saves them to the self.players dictionary in the following format [Player_num, character_name, name]
                msg = self.client.recv(2048).decode("utf-8")
                if msg != "None":
                    peoples_info = msg.split("\n")

                    for person in peoples_info:
                        person_info = person.split(",")
                        self.players[person_info[2]] = [person_info[3],person_info[1],person_info[2]]

                Thread(target=self.Recv).start()
                return True
            elif msg == "Too full":
                self.alert_too_full = True

        return False
    
    def Recv(self):
        while self.leaving_page:
            msg = self.client.recv(2048).decode()
            msg_parts = msg.split(",")

            # Recv new player from server formatted as 0x0004, character_name, name, player_num
            if msg_parts[0] == "0x0004":
                self.players[msg_parts[3]] = [msg_parts[1],msg_parts[2],msg_parts[3]]