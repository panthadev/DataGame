import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, image, boss):

        super().__init__() # initializes Sprite class

        self.screen = screen
        
        self.image = pygame.image.load(image)
        self.mask = pygame.mask.from_surface(self.image) # creates a bitmap from the image
        self.rect = self.mask.get_rect()

        self.boss = boss

        self.stats = {"heatlh": 1, "atk": 1, "spatk": 1, "spd": 2}
        self.colliding = {"state": False, "object": None}

        self.walk_right = ["assets/player/player_walk/player_walk" + str(0) + ".png",
                                "assets/player/player_walk/player_walk" + str(1) + ".png",
                                "assets/player/player_walk/player_walk" + str(2) + ".png",
                                "assets/player/player_walk/player_walk" + str(3) + ".png",
                                "assets/player/player_walk/player_walk" + str(4) + ".png",
                                "assets/player/player_walk/player_walk" + str(5) + ".png"]
        self.frame = 0
        self.frame_counter = 0
        self.frame_buffer = 9 # how many frames it takes to get to next part of animation


    def movement(self):     
        
        keys = pygame.key.get_pressed()
      
      # checks a,d keys to maove player by self.stats["spd"]
        if keys[pygame.K_d]: 
           
            if (self.frame == 5): 
                self.frame = 0 # resets to first frame of animation
            self.rect =  self.rect.move(self.stats["spd"], 0) # updates the player rect ie moves player
            if(self.frame_counter % self.frame_buffer == 0): # every frame_buffer number of frames do :
                self.frame = self.frame + 1 # moves to next frame of animation
            self.image = pygame.image.load(self.walk_right[self.frame])
         
        if keys[pygame.K_a]: 

            # needs to play animation
            self.rect =  self.rect.move(-self.stats["spd"], 0) # updates the player rect ie moves player
            
        
       

    def collisions(self):

        
        
        
        if(pygame.sprite.collide_mask(self, self.boss)):
            self.colliding["state"] = True
            self.colliding["object"] = self.boss

        else:
            self.colliding["state"] = False
            self.colliding["object"] = None

        print(self.colliding["state"])
        print(self.colliding["object"])
            
    

 

    def update(self):

        self.frame_counter = self.frame_counter + 1 # counts number of frames that have occurred in total

        self.movement()
        self.collisions()
       
       
        self.screen.blit(self.image, self.rect)
      
        

       
    
            
            
        
        
    




