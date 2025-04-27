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
        self.stats = {"heatlh": 1, "atk": 1, "spatk": 1, "spd": 2}
        self.colliding = {"state": False, "object": None}  
        self.dodge = {"is_dodging": False, "direction": None, 
                      "start_pos": None, "end_pos": None,
                      "start_time": None, "end_time": None}
        self.block = {"is_blocking": False}
       

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
        
        
        self.frame = 0
        self.frame_counter = 0
        self.frame_buffer = 9 # how many frames it takes to get to next part of animation

        

    def controls(self):     
        
        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_d]: # walk right

            if (self.frame == 5): 
                self.frame = 0 # resets to first frame of animation
            self.rect =  self.rect.move(self.stats["spd"], 0) # updates the player rect ie moves player
            if(self.frame_counter % self.frame_buffer == 0): # every frame_buffer number of frames do :
                self.frame = self.frame + 1 # moves to next frame of animation
            self.image = pygame.image.load(self.walk_right[self.frame])
        
        elif keys[pygame.K_a]: # walk left

            # needs to play animation
            self.rect =  self.rect.move(-self.stats["spd"], 0) # updates the player rect ie moves player
        

        elif keys[pygame.K_SPACE]:  # dodge
           
           self.dodge["is_dodging"] = True
           self.dodge["direction"] = 1

        elif self.dodge["is_dodging"]:
            
            if(self.frame > 5):
                self.dodge["is_dodging"] = False # ends animation and invincibility eye frames
                self.dodge["direction"] = None # resets direction

            if(self.frame_counter % self.frame_buffer == 0): # enough fps frames elapsed -> next frame of animation
                self.image = pygame.image.load(self.dodge_animation[self.frame])
                self.rect =  self.rect.move(self.stats["spd"] * 10, 0)
                self.frame = self.frame + 1


        elif keys[pygame.K_s]: # block
           
            print("blocking is " + str(self.block["is_blocking"]))

            if(self.frame >= 3):
                self.frame = 3 # keeps blocking animation at final frame while pressing down
                self.block["is_blocking"] = True # only blocking when animation is fully completed

            if(self.frame_counter % self.frame_buffer == 0): # every frame_buffer number of frames do :
                self.image = pygame.image.load(self.block_animation[self.frame])
                self.frame = self.frame + 1 # moves to next frame of animation

        
        else: # resets frames, self.image, and action statuses

            self.image = pygame.image.load("assets\player\player_idle.png")
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

        self.frame_counter = self.frame_counter + 1 # counts number of frames that have occurred in total

        self.controls()
        self.collisions()

       
       
        self.screen.blit(self.image, self.rect)
      
        

       
    
            
            
        
        
    




