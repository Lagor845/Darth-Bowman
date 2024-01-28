import pygame
from Asset_classes import *
import socket
from threading import Thread

class Host_menu():
    def __init__(self,frame_rate, character_name, name, character_dictionary) -> None:
        self.color = Colors()
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.connected_list = {}
        self.character_name = character_name
        self.name = name
        self.character_dictionary = character_dictionary
        self.player_num_list = [[1,False],[2,False],[3,False],[4,False]]
        self.current_page = True


    def accept(self):
        """Connected_list is formatted like connected_list[Ip Address] = [conn,[character_name,name],player num]"""
        while True:
            # Accept new players
            # First check if server has enough room
            conn,addr = self.server.accept()
            player_num = len(self.connected_list) + 1
            spot = False
            for num in self.player_num_list:
                if num[1] == False:
                    spot = True
                    player_num , num[1] = num[0] , True
                    break
            if spot == False:
                conn.send("Too full".encode("utf-8"))
            else:
                conn.send("Accepted".encode("utf-8"))

                # Recv player details formatted as character,name
                msg = conn.recv(2048).decode("utf-8")

                # Send player num formated as 0x0001,num
                conn.send(f"0x0001,{player_num}".encode("utf-8"))

                # Sends all current players to new player
                temp = ""
                for person in self.connected_list:
                    if temp != "":
                        temp + "\n"
                    temp = temp + f"{person[1][0]},{person[1][1]},{person[2]}"
                if temp == "":
                    temp = "None"
                conn.send(f"{temp}".encode("utf-8"))

                for person in self.connected_list:
                    string = f"0x0004,{msg.split(',')[0]},{msg.split(',')[1]},{player_num}"
                    person[0].send(string.encode("utf-8"))

                # Save new player to the connected list
                self.connected_list[addr[0]] = [conn]
                self.connected_list[addr[0]].append(msg.split(","))
                self.connected_list[addr[0]].append(player_num)

                # Start recv thread
                Thread(target=self.Recv,args=(conn,addr[0])).start()

        
    def Recv(self,conn,ip):
        while self.current_page:
            try:
                msg = conn.recv(2048).decode("utf-8")

                # Checks if player decided to quit
                if msg == "Quit":
                    player_num = self.connected_list[2]
                    self.connected_list.pop(ip)
                    for person in self.connected_list:
                        person[0].send(f"0x0005,{player_num}".encode())

                else:
                    new_msg = msg.split(",")

                    # Checks if player wants to switch characters then sends new character to everybody else on the self.connected list
                    if new_msg[0] == "0x0003":
                        self.connected_list[ip][1][0] = new_msg[1]

                        for person in self.connected_list:
                            if person[0] != conn:
                                person[0].send(f"0x0003,{new_msg[1]}".encode("utf-8"))

            except:
                try:
                    self.player_num_list[self.connected_list[ip][2]-1] = False
                    self.connected_list.pop(ip)
                except:
                    raise ValueError("Recv function in Host_menu.py experienced a critical error")

    def Run(self,screen):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostbyname(socket.gethostname()),56656))
        self.server.listen(3)
        Thread(target=self.accept).start()
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.background = Background("Images/Backgrounds/Background Image.jpeg",(0,0))

        pygame.mouse.set_visible(True)

        character_spots = [(self.width/8 , self.height/3) , (self.width/4 , self.height/3) , (self.width/2 + self.width/4,self.height/3) , (self.width/2 + (self.width/2 - self.width/8) , self.height/3)]
        name_spots = [(self.width/8 , self.height/4) , (self.width/4 , self.height/4) , (self.width/2 + self.width/4,self.height/4) , (self.width/2 + (self.width/2 - self.width/8) , self.height/4)]

        running = True
        while running:
            self.screen.fill(self.color.black)
            self.screen.blit(self.background.image,self.background.rect)

            Text(self.screen,50,self.color.white,self.width/2,self.height/10,f"Your Ip is {socket.gethostbyname(socket.gethostname())}")
            start_button = Button(self.screen,70,self.color.white,self.width/2-30,self.height/1.2,200,100 + round(self.height*0.2),"Start",self.color.red)
            back_button = Button(self.screen,50,self.color.white,self.width/10,self.height/10,100,100,"Back",self.color.red)

            img = pygame.image.load(Character_creator(self.character_dictionary[self.character_name]).Create().walk_animation_down[0]).convert_alpha()
            value_to_mult = self.screen.get_width() / img.get_width() / 12
            img = pygame.transform.scale(img,(img.get_width() * value_to_mult,img.get_height() * value_to_mult))
            self.screen.blit(img,character_spots[0])
            Text(self.screen,50,self.color.white,name_spots[1][0],name_spots[1][1],self.name)

            for person in self.connected_list:
                character = Character_creator(self.character_dictionary[self.connected_list[person][1][0]]).Create().walk_animation_down[0]
                img = pygame.image.load(character).convert_alpha()
                value_to_mult = self.screen.get_width() / img.get_width() / 12
                img = pygame.transform.scale(img,(img.get_width() * value_to_mult,img.get_height() * value_to_mult))
                self.screen.blit(img,character_spots[self.connected_list[person][2]-1])

                Text(self.screen,50,self.color.white,name_spots[self.connected_list[person][2]-1][0],name_spots[self.connected_list[person][2]-1][1],self.connected_list[person][1][1])

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        location = "Main menu"
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if start_button.rect.collidepoint(event.pos):
                        self.save_current_players()
                        for connection in self.connected_list:
                            connection[0].send("911_x0x".encode("uft-8"))
                        location = "game_load"
                        running = False
                        Sound("Audio/Sounds/Select.wav")

                    if back_button.rect.collidepoint(event.pos): 
                        location = "Main menu"
                        self.server.close()
                        running = False
                        Sound("Audio/Sounds/Select.wav")

            self.clock.tick(self.frame_rate)
            pygame.display.flip()
        
        self.current_page = False
        return location


    def save_current_players(self):
        ips = list(self.connected_list.keys())
        temp = ""
        for ip in ips:
            character_name = self.connected_list[ip][1][0]
            name = self.connected_list[ip][1][1]
            player_num = self.connected_list[ip][2]
            temp = temp + f"{ip},{character_name},{name},{player_num}\n"
        with open("Text Files/joined.current","w") as file:
            file = file.write(temp)