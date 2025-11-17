from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from menu import Menu

from random import randint, choice
from os import listdir

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game states: 'menu', 'playing', 'paused', 'game_over'
        self.game_state = 'menu'
        self.previous_state = None  # Track previous state for settings
        
        # Menu
        self.menu = Menu(self.display_surface)
        
        # Load images and audio first
        self.load_images()
        self.load_audio()
        
        # Loading screen
        self.loading_frames = []
        self.load_loading_animation()
        self.loading_start_time = 0
        self.loading_target_state = None
        
        # Game variables (initialized in setup)
        self.all_sprites = None
        self.collision_sprites = None
        self.bullet_sprites = None
        self.enemy_sprites = None
        self.player = None
        self.gun = None

    def load_audio(self):
        # Sound effects
        try:
            self.shoot_sound = pygame.mixer.Sound(AUDIO_SHOOT)
            self.shoot_sound.set_volume(0.2)
        except:
            print("Warning: shoot.wav not found")
            self.shoot_sound = None
            
        try:
            self.impact_sound = pygame.mixer.Sound(AUDIO_IMPACT)
            self.impact_sound.set_volume(0.3)
        except:
            print("Warning: impact.ogg not found")
            self.impact_sound = None
            
        try:
            self.player_death_sound = pygame.mixer.Sound(AUDIO_PLAYER_DEATH)
            self.player_death_sound.set_volume(0.4)
        except:
            print("Warning: player_death.wav not found")
            self.player_death_sound = None
            
        try:
            self.player_revive_sound = pygame.mixer.Sound(AUDIO_PLAYER_REVIVE)
            self.player_revive_sound.set_volume(0.3)
        except:
            print("Warning: player_revive.wav not found")
            self.player_revive_sound = None
            
        try:
            self.button_click_sound = pygame.mixer.Sound(AUDIO_BUTTON_CLICK)
            self.button_click_sound.set_volume(0.3)
        except:
            print("Warning: button_click.wav not found")
            self.button_click_sound = None
        
        # Background music
        try:
            self.menu_music = pygame.mixer.Sound(AUDIO_MENU_MUSIC)
            self.menu_music.set_volume(0.3)
        except:
            print("Warning: menu_music.wav not found")
            self.menu_music = None
            
        try:
            self.game_music = pygame.mixer.Sound(AUDIO_GAME_MUSIC)
            self.game_music.set_volume(0.3)
        except:
            print("Warning: game_music.wav not found")
            self.game_music = None
        
        self.current_music = None

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        
        # Load heart images for health display
        try:
            # Load full heart
            heart_files = [f for f in listdir(join('images', 'ui', 'heart')) if f.endswith('.png')]
            if len(heart_files) >= 2:
                # Assuming first is full, second is empty (or sort them)
                heart_files.sort()
                self.heart_full_surf = pygame.image.load(join('images', 'ui', 'heart', heart_files[0])).convert_alpha()
                self.heart_empty_surf = pygame.image.load(join('images', 'ui', 'heart', heart_files[1])).convert_alpha()
                # Scale them
                self.heart_full_surf = pygame.transform.scale(self.heart_full_surf, (40, 40))
                self.heart_empty_surf = pygame.transform.scale(self.heart_empty_surf, (40, 40))
            else:
                raise Exception("Need 2 heart images")
        except Exception as e:
            print(f"Warning: Could not load heart images: {e}")
            # Create fallback hearts if images not found
            # Full heart
            self.heart_full_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.heart_full_surf, (220, 20, 60), (15, 15), 12)
            pygame.draw.circle(self.heart_full_surf, (220, 20, 60), (25, 15), 12)
            pygame.draw.polygon(self.heart_full_surf, (220, 20, 60), [(8, 18), (20, 35), (32, 18)])
            # Empty heart
            self.heart_empty_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.heart_empty_surf, (100, 100, 100), (15, 15), 12, 2)
            pygame.draw.circle(self.heart_empty_surf, (100, 100, 100), (25, 15), 12, 2)
            pygame.draw.polygon(self.heart_empty_surf, (100, 100, 100), [(8, 18), (20, 35), (32, 18)], 2)
        
        # Load death effect frames
        self.death_effect_frames = []
        try:
            death_effect_path = join('images', 'ui', 'death')
            death_files = sorted([f for f in listdir(death_effect_path) if f.endswith('.png')])
            for file in death_files:
                surf = pygame.image.load(join(death_effect_path, file)).convert_alpha()
                # Scale to a reasonable size for the effect
                surf = pygame.transform.scale(surf, (128, 128))
                self.death_effect_frames.append(surf)
            print(f"Loaded {len(self.death_effect_frames)} death effect frames")
        except Exception as e:
            print(f"Warning: Death effect images not found: {e}")

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
    
    def load_loading_animation(self):
        """Load loading animation frames"""
        try:
            loading_files = sorted([f for f in listdir(LOADING_ANIMATION_PATH) if f.endswith('.png')])
            for file in loading_files:
                surf = pygame.image.load(join(LOADING_ANIMATION_PATH, file)).convert_alpha()
                # Scale to reasonable size (e.g., 128x128)
                surf = pygame.transform.scale(surf, (128, 128))
                self.loading_frames.append(surf)
            print(f"Loaded {len(self.loading_frames)} loading animation frames")
        except Exception as e:
            print(f"Warning: Loading animation not found: {e}")
            # Create a simple spinning circle as fallback
            for i in range(8):
                surf = pygame.Surface((128, 128), pygame.SRCALPHA)
                angle = i * 45
                pygame.draw.arc(surf, 'white', (20, 20, 88, 88), 0, 3.14 * angle / 180, 10)
                self.loading_frames.append(surf)

    def setup_game(self):
        """Initialize/reset the game"""
        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0 
        self.gun_cooldown = GUN_COOLDOWN

        # enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, ENEMY_SPAWN_RATE)
        self.spawn_positions = []
        
        # Player health
        self.player_lives = PLAYER_MAX_LIVES
        self.invulnerable = False
        self.hit_time = 0
        self.invulnerability_duration = INVULNERABILITY_DURATION
        
        # Death effect
        self.death_effects = []  # List to store active death effects
        
        # Score
        self.score = 0
        
        # Load map and entities
        self.setup()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            if self.shoot_sound:
                self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    if self.impact_sound:
                        self.impact_sound.play()
                    for sprite in collision_sprites:
                        # Check if enemy is not already in death animation
                        if sprite.death_time == 0:
                            self.score += 1
                            print(f"Enemy killed! Score: {self.score}")  # Debug print
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if not self.invulnerable and pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.player_lives -= 1
            self.hit_time = pygame.time.get_ticks()
            self.invulnerable = True
            
            # Play death sound when losing a heart
            if self.player_death_sound:
                self.player_death_sound.play()
            
            # Create death effect at player's position
            self.create_death_effect(self.player.rect.center)
            
            # Kill all enemies within a certain radius
            self.kill_nearby_enemies(self.player.rect.center)
            
            if self.player_lives <= 0:
                self.game_state = 'game_over'
                # Stop enemy spawning
                pygame.time.set_timer(self.enemy_event, 0)
                # Stop game music
                self.stop_music()
    
    def invulnerability_timer(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.invulnerable = False
    
    def create_death_effect(self, pos):
        """Create a death effect animation at the given position"""
        if self.death_effect_frames:
            effect = {
                'pos': pos,
                'frame_index': 0,
                'start_time': pygame.time.get_ticks(),
                'frame_duration': 50  # milliseconds per frame
            }
            self.death_effects.append(effect)
    
    def kill_nearby_enemies(self, pos, radius=None):
        """Kill all enemies within radius of pos"""
        if radius is None:
            radius = DEATH_EFFECT_RADIUS
        for enemy in self.enemy_sprites:
            distance = pygame.math.Vector2(enemy.rect.center).distance_to(pos)
            if distance <= radius:
                # Check if enemy is not already in death animation
                if enemy.death_time == 0:
                    self.score += 1
                    print(f"Enemy killed by death effect! Score: {self.score}")  # Debug print
                enemy.destroy()
    
    def update_death_effects(self):
        """Update and draw death effect animations"""
        current_time = pygame.time.get_ticks()
        effects_to_remove = []
        
        for effect in self.death_effects:
            # Calculate which frame to show
            elapsed = current_time - effect['start_time']
            frame_index = int(elapsed / effect['frame_duration'])
            
            if frame_index >= len(self.death_effect_frames):
                # Animation finished
                effects_to_remove.append(effect)
            else:
                # Draw the current frame
                frame = self.death_effect_frames[frame_index]
                # Center the effect on the position
                rect = frame.get_rect(center=effect['pos'])
                # Apply camera offset
                self.display_surface.blit(frame, rect.topleft + self.all_sprites.offset)
        
        # Remove finished effects
        for effect in effects_to_remove:
            self.death_effects.remove(effect)

    def draw_health(self):
        """Draw hearts in the top left corner - full and empty"""
        for i in range(PLAYER_MAX_LIVES):
            x = 20 + i * 50  # 50 pixels apart
            y = 20
            # Draw full heart if player has this life, empty heart otherwise
            if i < self.player_lives:
                self.display_surface.blit(self.heart_full_surf, (x, y))
            else:
                self.display_surface.blit(self.heart_empty_surf, (x, y))
    
    def draw_score(self):
        """Draw score in the top left corner below hearts"""
        font = pygame.font.Font(FONT_PATH, 48)
        score_text = font.render(f'Score: {self.score}', True, 'white')
        score_rect = score_text.get_rect(topleft=(20, 80))  # Below the hearts
        
        # Draw shadow
        shadow_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(topleft=(22, 82))
        self.display_surface.blit(shadow_text, shadow_rect)
        self.display_surface.blit(score_text, score_rect)
    
    def play_music(self, music):
        """Play background music, stopping current music if playing"""
        if self.current_music == music:
            # Just update volume if already playing
            if music:
                music.set_volume(self.menu.music_volume)
            return
        
        self.stop_music()
        
        if music:
            music.set_volume(self.menu.music_volume)
            music.play(loops=-1)
            self.current_music = music
    
    def update_sfx_volumes(self):
        """Update all sound effect volumes"""
        volume = self.menu.sfx_volume
        if self.shoot_sound:
            self.shoot_sound.set_volume(0.2 * volume)
        if self.impact_sound:
            self.impact_sound.set_volume(0.3 * volume)
        if self.player_death_sound:
            self.player_death_sound.set_volume(0.4 * volume)
        if self.player_revive_sound:
            self.player_revive_sound.set_volume(0.3 * volume)
        if self.button_click_sound:
            self.button_click_sound.set_volume(0.3 * volume)
    
    def stop_music(self):
        """Stop currently playing music"""
        if self.current_music:
            self.current_music.stop()
            self.current_music = None
    
    def start_loading(self, target_state):
        """Start loading screen transition"""
        self.game_state = 'loading'
        self.loading_start_time = pygame.time.get_ticks()
        self.loading_target_state = target_state
    
    def draw_loading_screen(self):
        """Draw the loading screen with animated icon"""
        self.display_surface.fill((20, 20, 30))
        
        if self.loading_frames:
            # Calculate which frame to show (loop through frames)
            elapsed = pygame.time.get_ticks() - self.loading_start_time
            frame_duration = 100  # 100ms per frame
            frame_index = (elapsed // frame_duration) % len(self.loading_frames)
            
            # Draw loading animation in center
            frame = self.loading_frames[frame_index]
            frame_rect = frame.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.display_surface.blit(frame, frame_rect)
        
        # Draw "Loading..." text
        font = pygame.font.Font(FONT_PATH, 64)
        loading_text = font.render('Loading...', True, 'white')
        text_rect = loading_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        
        # Text shadow
        shadow_text = font.render('Loading...', True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 83))
        self.display_surface.blit(shadow_text, shadow_rect)
        self.display_surface.blit(loading_text, text_rect)

    def handle_menu(self):
        """Handle main menu state"""
        # Play menu music
        self.play_music(self.menu_music)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_main_menu_click(pygame.mouse.get_pos(), True)
                if action == 'start':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.start_loading('playing')
                elif action == 'settings':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.previous_state = 'menu'
                    self.game_state = 'settings'
                elif action == 'exit':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.running = False
        
        self.menu.draw_main_menu()

    def handle_game_over(self):
        """Handle game over state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_game_over_click(pygame.mouse.get_pos(), True)
                if action == 'play_again':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    if self.player_revive_sound:
                        self.player_revive_sound.play()
                    self.start_loading('playing')
                elif action == 'main_menu':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.start_loading('menu')
        
        # Draw the last game frame in background
        self.display_surface.fill('black')
        if self.all_sprites and self.player:
            self.all_sprites.draw(self.player.rect.center)
        
        # Draw game over overlay
        self.menu.draw_game_over(self.score)
    
    def handle_loading(self):
        """Handle loading screen state"""
        # Check if events happened (to prevent freezing)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Draw loading screen
        self.draw_loading_screen()
        
        # Check if loading time has elapsed
        elapsed = pygame.time.get_ticks() - self.loading_start_time
        if elapsed >= LOADING_DURATION:
            # Transition to target state
            if self.loading_target_state == 'playing':
                self.game_state = 'playing'
                self.setup_game()
                self.play_music(self.game_music)
            elif self.loading_target_state == 'menu':
                self.game_state = 'menu'
                self.play_music(self.menu_music)
            
            self.loading_target_state = None
    
    def handle_settings(self):
        """Handle settings menu state"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_settings_click(mouse_pos, True)
                if action == 'back':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    # Return to previous state
                    self.game_state = self.previous_state if self.previous_state else 'menu'
                    self.previous_state = None
        
        # Handle slider dragging
        self.menu.handle_settings_slider(mouse_pos, mouse_pressed)
        
        # Update volumes in real-time
        self.update_sfx_volumes()
        if self.current_music:
            self.current_music.set_volume(self.menu.music_volume)
        
        # Draw appropriate background based on where we came from
        if self.previous_state == 'paused':
            # Draw game in background
            self.display_surface.fill('black')
            if self.all_sprites and self.player:
                self.all_sprites.draw(self.player.rect.center)
                self.draw_health()
                self.draw_score()
            self.menu.draw_settings_menu(from_pause=True)
        else:
            # Draw menu background
            self.menu.draw_settings_menu(from_pause=False)
    
    def handle_paused(self):
        """Handle paused state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.game_state = 'playing'
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_pause_menu_click(pygame.mouse.get_pos(), True)
                if action == 'resume':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.game_state = 'playing'
                elif action == 'settings':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.previous_state = 'paused'
                    self.game_state = 'settings'
                elif action == 'restart':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    if self.player_revive_sound:
                        self.player_revive_sound.play()
                    self.game_state = 'playing'
                    self.setup_game()
                elif action == 'main_menu':
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.start_loading('menu')
        
        # Draw the game in background
        self.display_surface.fill('black')
        if self.all_sprites and self.player:
            self.all_sprites.draw(self.player.rect.center)
            self.draw_health()
            self.draw_score()
        
        # Draw pause menu overlay
        self.menu.draw_pause_menu()

    def handle_playing(self, dt):
        """Handle playing state"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.game_state = 'paused'
            if event.type == self.enemy_event:
                Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), 
                      (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

        # update 
        self.gun_timer()
        self.invulnerability_timer()
        self.input()
        self.all_sprites.update(dt)
        self.bullet_collision()
        self.player_collision()

        # draw
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        self.update_death_effects()  # Draw death effects on top of game
        self.draw_health()  # Draw hearts last so they're always on top
        self.draw_score()  # Draw score in top right

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            if self.game_state == 'menu':
                self.handle_menu()
            elif self.game_state == 'playing':
                self.handle_playing(dt)
            elif self.game_state == 'paused':
                self.handle_paused()
            elif self.game_state == 'game_over':
                self.handle_game_over()
            elif self.game_state == 'loading':
                self.handle_loading()
            elif self.game_state == 'settings':
                self.handle_settings()
            
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()