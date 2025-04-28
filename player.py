import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, image, boss):

        super().__init__() # initializes Sprite class

        self.screen = screen
        
        self.image = pygame.image.load(image)
        self.mask = pygame.mask.from_surface(self.image) # creates a bitmap from the image
        self.rect = self.mask.get_rect()

        self.boss = boss

        # for data collection
        self.stats = {"heatlh": 1, "atk": 1, "spatk": 1, "spd": 2, "dodge_range": 10}
        self.colliding = {"state": False, "object": None}  
        self.dodge = {"is_dodging": False, "direction": None, 
                      "start_pos": None, "end_pos": None,
                      "start_time": None, "end_time": None}
        self.block = {"is_blocking": False}
        self.attack = {"is_attacking": False}

        self.direction = 1 # right: 1, left: -1
        
       

        # player assets
        self.walk_right = ["assets/player/player_walk/player_walk" + str(0) + ".png",
                                "assets/player/player_walk/player_walk" + str(1) + ".png",
                                "assets/player/player_walk/player_walk" + str(2) + ".png",
                                "assets/player/player_walk/player_walk" + str(3) + ".png",
                                "assets/player/player_walk/player_walk" + str(4) + ".png",
                                "assets/player/player_walk/player_walk" + str(5) + ".png"]
       
        self.dodge_animation = ["assets/player/player_dodge/player_dodge" + str(0) + ".png",
                                "assets/player/player_dodge/player_dodge" + str(1) + ".png",
                                "assets/player/player_dodge/player_dodge" + str(2) + ".png",
                                "assets/player/player_dodge/player_dodge" + str(3) + ".png",
                                "assets/player/player_dodge/player_dodge" + str(4) + ".png",
                                "assets/player/player_dodge/player_dodge" + str(5) + ".png"]
        
        self.block_animation = ["assets\player\player_block\player_block"  + str(0)  + ".png",
                                "assets\player\player_block\player_block"  + str(1)  + ".png",
                                "assets\player\player_block\player_block"  + str(2)  + ".png",
                                "assets\player\player_block\player_block"  + str(3)  + ".png"]
        
        self.atk_animation = ["assets\player\player_attack\player_attack" + str(0) + ".png",
                              "assets\player\player_attack\player_attack" + str(1) + ".png",
                              "assets\player\player_attack\player_attack" + str(2) + ".png",
                              "assets\player\player_attack\player_attack" + str(3) + ".png",
                              "assets\player\player_attack\player_attack" + str(4) + ".png",
                              "assets\player\player_attack\player_attack" + str(5) + ".png"]
        
        # for animations
        self.frame = 0
        self.frame_counter = 0
        self.frame_buffer = 7 # how many frames it takes to get to next part of animation

        self.busy = {"busy": False, "action": None}

        

    def controls(self):     
        
        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_d]: # walk right
            self.direction = 1 # facing right

            if self.frame >= 5: 
                self.frame = 0 # resets to first frame of animation
            self.rect =  self.rect.move( self.direction * self.stats["spd"], 0) # moves player speed * direction
            if self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
                self.frame += 1 # moves to next frame of animation
            self.image = pygame.image.load(self.walk_right[self.frame])
        
        elif keys[pygame.K_a]: # walk left
            self.direction = -1 # facing left
            
            if self.frame >= 5: 
                self.frame = 0 # resets to first frame of animation
            self.rect =  self.rect.move(self.direction * self.stats["spd"], 0) # moves player speed * direction
            if self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
                self.frame += 1 # moves to next frame of animation
            self.image = pygame.transform.flip(pygame.image.load(self.walk_right[self.frame]), True, False) # flips walk_right animation horizontally


        elif keys[pygame.K_SPACE]:  # dodge
           
           self.dodge["is_dodging"] = True
           self.dodge["direction"] = 1
           
        elif self.dodge["is_dodging"]:
            
            if self.frame > 5:
                self.dodge["is_dodging"] = False # ends animation and invincibility eye frames
                self.dodge["direction"] = None # resets direction
                
            if self.frame_counter % self.frame_buffer == 0: # enough fps frames elapsed -> next frame of animation
                if self.direction == 1:
                    self.image = pygame.image.load(self.dodge_animation[self.frame])
                else:
                    self.image = pygame.transform.flip(pygame.image.load(self.dodge_animation[self.frame]), True, False) # flips dodging to the right animation horizontally
                self.rect =  self.rect.move(self.direction * self.stats["spd"] * self.stats["dodge_range"], 0) # moves player speed * direction * dodge_range
                self.frame += 1


        elif keys[pygame.K_s]: # block
           
            print("blocking is " + str(self.block["is_blocking"]))

            if self.frame >= 3:
                self.frame = 3 # keeps blocking animation at final frame while pressing down
                self.block["is_blocking"] = True # only blocking when animation is fully completed

            if self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
                if self.direction == 1:
                    self.image = pygame.image.load(self.block_animation[self.frame])
                else:
                    self.image = pygame.transform.flip(pygame.image.load(self.block_animation[self.frame]), True, False) # flips block_animation horizontally
                self.frame += 1 # moves to next frame of animation
        

        elif keys[pygame.K_f]: # attack

            self.attack["is_attacking"] = True

        elif self.attack["is_attacking"]:

            if self.frame > 5:
                self.attack["is_attacking"] = False # ends animation and resets attacking state
            elif self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
                if self.direction == 1:
                    self.image = pygame.image.load(self.atk_animation[self.frame])
                else:
                    self.image = pygame.transform.flip(pygame.image.load(self.atk_animation[self.frame]), True, False) # flips atk_animation horizontally
                self.frame += 1  # moves to next frame of animation

        
        else: # resets frames, self.image, and action statuses
            if self.direction == 1:
                self.image = pygame.image.load("assets\player\player_idle.png")
            else:
                self.image = pygame.transform.flip(pygame.image.load("assets\player\player_idle.png"), True, False)

            self.frame = 0
            self.frame_counter = 0

            self.dodge["is_dodging"] = False
            self.dodge["direction"] = None

            self.block["is_blocking"] = False



    def collisions(self):

        if(pygame.sprite.collide_mask(self, self.boss) and self.dodge["is_dodging"] == False): # if colliding + not dodging
            self.colliding["state"] = True
            self.colliding["object"] = self.boss

        else:
            self.colliding["state"] = False
            self.colliding["object"] = None

        print(self.colliding["state"])
        print(self.colliding["object"])
            
    

 

    def update(self):

        self.frame_counter += 1 # counts number of frames that have occurred in total

        self.controls()
        self.collisions()

       
       
        self.screen.blit(self.image, self.rect)
      
        

       
    
            
            
        
        
    




