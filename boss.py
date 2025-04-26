import pygame

class Boss(pygame.sprite.Sprite):

    def __init__(self, screen, image, x, y):

        super().__init__() # initializes Sprite class
        
        self.screen = screen

        self.image = pygame.image.load(image)
        self.mask = pygame.mask.from_surface(self.image) # creates a bitmap from the image
        self.rect = self.mask.get_rect(center=(x,y))



    def check_collide(self):

        print("")
    

        

    def update(self):

        self.screen.blit(self.image, self.rect)
    
    


        




