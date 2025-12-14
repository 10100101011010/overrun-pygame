from settings import * 

class AllSprites(pygame.sprite.Group):
    def __init__(self, display_surface=None):
        super().__init__()
        self.display_surface = display_surface
        self.offset = pygame.Vector2()
    
    def set_display_surface(self, surface):
        """Update the display surface reference"""
        self.display_surface = surface
    
    def draw(self, target_pos):
        if self.display_surface is None:
            self.display_surface = pygame.display.get_surface()
            
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')] 
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')] 
        
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)