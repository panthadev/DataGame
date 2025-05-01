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
        self.stats = {"heatlh": 1, "atk": 1, "spatk": 1, "spd": 2, "range": 20, "cooldown": 0.25}
        self.colliding = {"state": False, "object": None}  
        self.block = {"is_blocking": False,"pos": None,  
                      "start_time": None, "end_time": None}
        self.dodge = {"is_dodging": False, "direction": None, 
                      "start_pos": None, "end_pos": None,
                      "start_time": None, "end_time": None}
        self.attack =  {"is_attacking": False, "direction": None, 
                      "start_pos": None, "end_pos": None,
                      "start_time": None, "end_time": None}
        self.direction = 1 # right: 1, left: -1
        self.busy = {"busy": False, "key": None} # stops player from interrupting attacks/dodges/blocks, key is index of the key(in pygame.keys.get_pressed()) pressed that causes "busy" == True


        # player assets
        self.idle_sprite = pygame.image.load("assets/player/idle.png")
        
        self.walk_spritesheet = pygame.image.load("assets/player/run.png")
        self.block_spritesheet = pygame.image.load("assets/player/block2.png")
        self.dodge_spritesheet = pygame.image.load("assets/player/dodge.png")
        self.attack_spritesheet = pygame.image.load("assets/player/shoot.png")
        
        self.sprite_width = 128
        self.sprite_height = 128
        
        # for animations
        self.frame = 0
        self.frame_counter = 0
        self.frame_buffer = 7 # how many frames it takes to get to next part of animation



    
    def get_sprite(self, spritesheet, frame): # returns desired section of spritesheet by creating a subsurface from full spritesheet
        return (spritesheet.subsurface(pygame.Rect(frame * self.sprite_width, 0, self.sprite_width, self.sprite_height)))



    def idle(self):
        
        if self.direction == 1:
            self.image = self.idle_sprite
        else:
            self.image = pygame.transform.flip(self.idle_sprite, True, False)


    def adjust_animation_timing(self):
        # takes in what frames to make go quicker
        # adjusts frame_buffer and corresponding logic
        pass


    def get_key_index(self, keys): # to get key that was pressed -> self.busy["key"] so that that key can continue to be pressed even if busy
        counter = 0
        for i in range(0, len(keys)):
            if keys[i] != True:
                counter += 1
            else:
                #print(counter)
                return(counter)


    def hold_or_press(self, hold = False, press = False, keys = None,action = None, helper_function = None):
        # self.busy and keys need to be adjusted depending
        # on if the move requires the player to hold the key down
        # or just press
        # use this to clean up code later
        if hold and press:
            raise ValueError("Only one argument can be True")
        elif press:
            if action["end_time"] != None: # if its not the first time since running this action takes place:
                time = float(pygame.time.get_ticks() / 1000)
                print("time - endtime: " + str(time - action["end_time"]))
                print("endtime: " + str(action["end_time"]))
                if abs(time - (action["end_time"])) > self.stats["cooldown"]: # if time since last use > cooldown:
                    self.busy["key"] = None # interacts with first if statement in control(), makes it so that once key is pressed, action occurs without interruption,  self.busy["key"] != None would indicate that the action requires key to be held
                    helper_function()
            else: # if its the first time the action takes place:
                print("first time action occurring")
                self.busy["key"] = None # interacts with first if statement in control(), makes it so that once key is pressed, action occurs without interruption,  self.busy["key"] != None would indicate that the action requires key to be held
                helper_function()

        elif hold:
            pass
        
        pass


    def walk_ctrl(self):

        if self.frame >= 7: 
            self.frame = 0 # resets to first frame of animation
        self.rect =  self.rect.move(self.direction * self.stats["spd"], 0) # moves player speed * direction
        if self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
            self.frame += 1 # moves to next frame of animation
        
        if self.direction == 1: 
            self.image = self.get_sprite(self.walk_spritesheet, self.frame)     
        else:
            self.image = pygame.transform.flip(self.get_sprite(self.walk_spritesheet, self.frame), True, False)

    def block_ctrl(self):
        self.busy["busy"] = True
        
        
        if self.frame >= 3:
                self.frame = 3 # keeps blocking animation at final frame while pressing down
                self.block["is_blocking"] = True # only blocking when animation is fully completed
        

        if self.frame_counter % self.frame_buffer == 0: # every frame_buffer number of frames do :
            if self.direction == 1:
                self.image = self.get_sprite(self.block_spritesheet, self.frame)
            else:
                self.image = pygame.transform.flip(self.get_sprite(self.block_spritesheet, self.frame), True, False) # flips block_animation horizontally
            self.frame += 1 # moves to next frame of animation


    def dodge_ctrl_helper(self): # seperate, so that one button press activates it instead of having to hold down space
        self.frame = 0 # fixes issue where walked adds frames and then dodge starts at a later grame
        
        self.dodge["is_dodging"] = True
        self.dodge["direction"] = self.direction
        self.dodge["start_pos"] = self.rect.centerx
        print("start pos is: " + str(self.dodge["start_pos"])) 
        self.dodge["start_time"] = float(pygame.time.get_ticks() / 1000)
        
        self.busy["busy"] = True

    def dodge_ctrl(self):
        if self.frame > 3:
            self.frame = 0 # resets frames so that other naimations start at 0
            
            self.dodge["is_dodging"] = False # ends animation and invincibility eye frames
            self.dodge["direction"] = None # resets direction 
            self.dodge["end_pos"] = self.rect.centerx
            print("end pos is: " + str(self.dodge["end_pos"]))
            print("distance traveled: " + str(abs(self.dodge["end_pos"] - self.dodge["start_pos"])))
            self.dodge["end_time"] = float(pygame.time.get_ticks() / 1000)
            
            self.dodge["start_pos"] = None
            self.dodge["end_pos"] = None

            self.busy["busy"] = False # resets busy status so that player can use other moves
            #print("no longer busy")

            self.idle()
        
        if self.frame_counter % self.frame_buffer == 0: # enough fps frames elapsed -> next frame of animation
            if self.direction == 1:
                self.image = self.get_sprite(self.dodge_spritesheet, self.frame)
            else:
                self.image = pygame.transform.flip(self.get_sprite(self.dodge_spritesheet, self.frame), True, False) # flips image horizontally
            self.rect =  self.rect.move(self.direction * self.stats["spd"] * self.stats["range"], 0) # moves player speed * direction * dodge_range
            self.frame += 1


    def attack_ctrl_helper(self):
        self.frame = 0 # fixes issue where walked adds frames and then dodge starts at a later grame
        
        self.attack["is_attacking"] = True
        self.attack["start_time"] = float(pygame.time.get_ticks() / 1000)
        
        self.busy["busy"] = True
        
    
    def attack_ctrl(self):

        if self.frame > 5:
            self.rect =  self.rect.move(-30 * self.direction, 0) # fixes player moving forward when attacking(cause of how the sprites are drawn)
            self.frame = 0

            self.attack["is_attacking"] = False
            self.attack["start_time"] = None
            self.attack["end_time"] = float(pygame.time.get_ticks() / 1000)

            self.busy["busy"] = False
            
            self.idle()
        if self.frame_counter % self.frame_buffer == 0:
            if self.frame == 0:
                self.rect =  self.rect.move(30 * self.direction, 0) # fixes player moving forward when attacking(cause of how the sprites are drawn)
            if self.direction == 1:
                self.image = self.get_sprite(self.attack_spritesheet, self.frame)
            else:
                self.image = pygame.transform.flip(self.get_sprite(self.attack_spritesheet, self.frame), True, False) # flips attack to the right animation horizontally
            self.frame += 1



    def controls_placeholder(self):
        keys = pygame.key.get_pressed()

        if self.busy["busy"] == True:
            keys = [0] * len(pygame.key.get_pressed()) # makes every index of possible keys pressed to false
            keys_helper = pygame.key.get_pressed() # second keys object
            if self.busy["key"]!= None: # for actions where the key needs to be held
                keys[self.busy["key"]] = keys_helper[self.busy["key"]] # original keys object's index at self.busy["key"] can now either be T or F instead of just False 
        
        if keys[pygame.K_d]:
            self.direction = 1
            self.walk_ctrl()
            
            #print("self.busy['busy'] is " + str(self.busy["busy"]))
        elif keys[pygame.K_a]: 
            self.direction = -1
            self.walk_ctrl()
            #print("self.busy['busy'] is " + str(self.busy["busy"]))
        elif keys[pygame.K_s]:
            self.busy["key"] = self.get_key_index(keys) # the s key can be pressed while busy
            self.block_ctrl()

        elif keys[pygame.K_SPACE]:
            self.hold_or_press(False, True, keys, self.dodge, self.dodge_ctrl_helper)
        elif self.dodge["is_dodging"]:
            self.dodge_ctrl()
        
        elif keys[pygame.K_f]: # attack
            self.hold_or_press(False, True, keys, self.attack, self.attack_ctrl_helper)
        elif self.attack["is_attacking"]:
            self.attack_ctrl()
        

        else: # resets frames, self.image, and action statuses
            self.idle()
           
            self.frame = 0
            self.frame_counter = 0
            #print("self.frame is " + str(self.frame))

            self.dodge["is_dodging"] = False
            self.dodge["direction"] = None

            self.block["is_blocking"] = False

            self.busy["busy"] = False
            self.busy["key"] = None
            #print("self.busy['busy'] is " + str(self.busy["busy"]))

            



    def collisions(self):

        if(pygame.sprite.collide_mask(self, self.boss) and self.dodge["is_dodging"] == False): # if colliding + not dodging
            self.colliding["state"] = True
            self.colliding["object"] = self.boss

        else:
            self.colliding["state"] = False
            self.colliding["object"] = None

        # print(self.colliding["state"])
        # print(self.colliding["object"])
            
    

 

    def update(self):

        self.frame_counter += 1 # counts number of frames that have occurred in total
        
        self.controls_placeholder()
        self.collisions()

       
       
        self.screen.blit(self.image, self.rect)
      
        

       
    
            
            
        
        
    




