from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color='white'):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        
        # Calculate 3D effect offset
        offset = 6
        
        # Draw shadow/3D bottom layer (darker)
        shadow_color = tuple(max(0, c - 60) for c in color)
        shadow_rect = self.rect.copy()
        shadow_rect.y += offset
        pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=8)
        
        # Draw main button (top layer)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        # Draw border/outline
        border_color = tuple(max(0, c - 40) for c in color)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)
        
        # Draw text
        font = pygame.font.Font(FONT_PATH, 48)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Text shadow for readability
        shadow_text = font.render(self.text, True, (0, 0, 0))
        shadow_text_rect = shadow_text.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        surface.blit(shadow_text, shadow_text_rect)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed

class Menu:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font_large = pygame.font.Font(FONT_PATH, 96)
        self.font_medium = pygame.font.Font(FONT_PATH, 48)
        
        # Load menu background
        try:
            self.menu_background = pygame.image.load(MENU_BACKGROUND_PATH).convert()
            self.menu_background = pygame.transform.scale(self.menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            print("Warning: Menu background not found, using solid color")
            self.menu_background = None
        
        # Volume settings (0.0 to 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Main Menu Buttons
        button_width, button_height = 300, 80
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        
        self.start_button = Button(
            button_x, 320, button_width, button_height,
            'START', (34, 139, 34), (50, 205, 50)
        )
        
        self.settings_button = Button(
            button_x, 430, button_width, button_height,
            'SETTINGS', (70, 130, 180), (100, 149, 237)
        )
        
        self.exit_button = Button(
            button_x, 540, button_width, button_height,
            'EXIT', (178, 34, 34), (220, 20, 60)
        )
        
        # Game Over Buttons
        self.play_again_button = Button(
            button_x, 350, button_width, button_height,
            'PLAY AGAIN', (34, 139, 34), (50, 205, 50)
        )
        
        self.menu_button = Button(
            button_x, 460, button_width, button_height,
            'MAIN MENU', (70, 130, 180), (100, 149, 237)
        )
        
        # Pause Menu Buttons
        self.resume_button = Button(
            button_x, 250, button_width, button_height,
            'RESUME', (34, 139, 34), (50, 205, 50)
        )
        
        self.pause_settings_button = Button(
            button_x, 360, button_width, button_height,
            'SETTINGS', (70, 130, 180), (100, 149, 237)
        )
        
        self.restart_button = Button(
            button_x, 470, button_width, button_height,
            'RESTART', (218, 165, 32), (255, 215, 0)
        )
        
        self.pause_menu_button = Button(
            button_x, 580, button_width, button_height,
            'MAIN MENU', (178, 34, 34), (220, 20, 60)
        )
        
        # Settings Menu Buttons - Sliders
        slider_width, slider_height = 400, 20
        slider_x = WINDOW_WIDTH // 2 - slider_width // 2
        
        self.music_slider_rect = pygame.Rect(slider_x, 300, slider_width, slider_height)
        self.sfx_slider_rect = pygame.Rect(slider_x, 420, slider_width, slider_height)
        
        self.back_button = Button(
            button_x, 550, button_width, button_height,
            'BACK', (178, 34, 34), (220, 20, 60)
        )
        
        # Track which slider is being dragged
        self.dragging_music = False
        self.dragging_sfx = False
    
    def draw_main_menu(self):
        # Draw background or solid color
        if self.menu_background:
            self.display_surface.blit(self.menu_background, (0, 0))
        else:
            self.display_surface.fill((20, 20, 30))
        
        # Title
        title = self.font_large.render('SURVIVOR', True, 'white')
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        
        # Title shadow
        shadow = self.font_large.render('SURVIVOR', True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(WINDOW_WIDTH // 2 + 4, 204))
        self.display_surface.blit(shadow, shadow_rect)
        self.display_surface.blit(title, title_rect)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.settings_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)
        
        self.start_button.draw(self.display_surface)
        self.settings_button.draw(self.display_surface)
        self.exit_button.draw(self.display_surface)
    
    def draw_game_over(self, score=0):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        self.display_surface.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render('YOU DIED', True, (220, 20, 60))
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        
        # Shadow effect
        shadow = self.font_large.render('YOU DIED', True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(WINDOW_WIDTH // 2 + 4, 204))
        self.display_surface.blit(shadow, shadow_rect)
        self.display_surface.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font_medium.render(f'Score: {score}', True, 'white')
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.display_surface.blit(score_text, score_rect)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        self.play_again_button.check_hover(mouse_pos)
        self.menu_button.check_hover(mouse_pos)
        
        self.play_again_button.draw(self.display_surface)
        self.menu_button.draw(self.display_surface)
    
    def handle_main_menu_click(self, mouse_pos, mouse_pressed):
        if self.start_button.is_clicked(mouse_pos, mouse_pressed):
            return 'start'
        elif self.settings_button.is_clicked(mouse_pos, mouse_pressed):
            return 'settings'
        elif self.exit_button.is_clicked(mouse_pos, mouse_pressed):
            return 'exit'
        return None
    
    def handle_game_over_click(self, mouse_pos, mouse_pressed):
        if self.play_again_button.is_clicked(mouse_pos, mouse_pressed):
            return 'play_again'
        elif self.menu_button.is_clicked(mouse_pos, mouse_pressed):
            return 'main_menu'
        return None
    
    def draw_pause_menu(self):
        # Semi-transparent dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        self.display_surface.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render('PAUSED', True, 'white')
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, 130))
        
        # Shadow effect
        shadow = self.font_large.render('PAUSED', True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(WINDOW_WIDTH // 2 + 4, 134))
        self.display_surface.blit(shadow, shadow_rect)
        self.display_surface.blit(pause_text, pause_rect)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        self.resume_button.check_hover(mouse_pos)
        self.pause_settings_button.check_hover(mouse_pos)
        self.restart_button.check_hover(mouse_pos)
        self.pause_menu_button.check_hover(mouse_pos)
        
        self.resume_button.draw(self.display_surface)
        self.pause_settings_button.draw(self.display_surface)
        self.restart_button.draw(self.display_surface)
        self.pause_menu_button.draw(self.display_surface)
    
    def handle_pause_menu_click(self, mouse_pos, mouse_pressed):
        if self.resume_button.is_clicked(mouse_pos, mouse_pressed):
            return 'resume'
        elif self.pause_settings_button.is_clicked(mouse_pos, mouse_pressed):
            return 'settings'
        elif self.restart_button.is_clicked(mouse_pos, mouse_pressed):
            return 'restart'
        elif self.pause_menu_button.is_clicked(mouse_pos, mouse_pressed):
            return 'main_menu'
        return None
    
    def draw_settings_menu(self, from_pause=False):
        # Background - either overlay or solid
        if from_pause:
            # Semi-transparent overlay if coming from pause
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((20, 20, 30))
            self.display_surface.blit(overlay, (0, 0))
        else:
            # Use menu background if from main menu
            if self.menu_background:
                self.display_surface.blit(self.menu_background, (0, 0))
            else:
                self.display_surface.fill((20, 20, 30))
        
        # Title
        title = self.font_large.render('SETTINGS', True, 'white')
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        shadow = self.font_large.render('SETTINGS', True, (50, 50, 50))
        shadow_rect = shadow.get_rect(center=(WINDOW_WIDTH // 2 + 4, 124))
        self.display_surface.blit(shadow, shadow_rect)
        self.display_surface.blit(title, title_rect)
        
        # Music Volume Label and Slider
        music_label = self.font_medium.render('Music Volume', True, 'white')
        music_label_rect = music_label.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.display_surface.blit(music_label, music_label_rect)
        
        self.draw_slider(self.music_slider_rect, self.music_volume)
        
        # Music volume percentage
        music_percent = self.font_medium.render(f'{int(self.music_volume * 100)}%', True, 'white')
        music_percent_rect = music_percent.get_rect(center=(WINDOW_WIDTH // 2, 340))
        self.display_surface.blit(music_percent, music_percent_rect)
        
        # SFX Volume Label and Slider
        sfx_label = self.font_medium.render('Sound Effects', True, 'white')
        sfx_label_rect = sfx_label.get_rect(center=(WINDOW_WIDTH // 2, 370))
        self.display_surface.blit(sfx_label, sfx_label_rect)
        
        self.draw_slider(self.sfx_slider_rect, self.sfx_volume)
        
        # SFX volume percentage
        sfx_percent = self.font_medium.render(f'{int(self.sfx_volume * 100)}%', True, 'white')
        sfx_percent_rect = sfx_percent.get_rect(center=(WINDOW_WIDTH // 2, 460))
        self.display_surface.blit(sfx_percent, sfx_percent_rect)
        
        # Back button
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.display_surface)
    
    def draw_slider(self, rect, value):
        # Draw slider background (darker)
        pygame.draw.rect(self.display_surface, (60, 60, 70), rect, border_radius=10)
        
        # Draw filled portion (lighter)
        filled_width = int(rect.width * value)
        filled_rect = pygame.Rect(rect.x, rect.y, filled_width, rect.height)
        pygame.draw.rect(self.display_surface, (70, 130, 180), filled_rect, border_radius=10)
        
        # Draw handle (circle)
        handle_x = rect.x + filled_width
        handle_y = rect.centery
        pygame.draw.circle(self.display_surface, 'white', (handle_x, handle_y), 15)
        pygame.draw.circle(self.display_surface, (70, 130, 180), (handle_x, handle_y), 12)
    
    def handle_settings_slider(self, mouse_pos, mouse_pressed):
        """Handle slider dragging"""
        if mouse_pressed:
            # Check if clicking on music slider
            if self.music_slider_rect.collidepoint(mouse_pos):
                self.dragging_music = True
            # Check if clicking on sfx slider
            if self.sfx_slider_rect.collidepoint(mouse_pos):
                self.dragging_sfx = True
        else:
            self.dragging_music = False
            self.dragging_sfx = False
        
        # Update music volume if dragging
        if self.dragging_music:
            relative_x = mouse_pos[0] - self.music_slider_rect.x
            self.music_volume = max(0.0, min(1.0, relative_x / self.music_slider_rect.width))
        
        # Update sfx volume if dragging
        if self.dragging_sfx:
            relative_x = mouse_pos[0] - self.sfx_slider_rect.x
            self.sfx_volume = max(0.0, min(1.0, relative_x / self.sfx_slider_rect.width))
    
    def handle_settings_click(self, mouse_pos, mouse_pressed):
        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return 'back'
        return None