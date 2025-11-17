import pygame 
from os.path import join 
from os import walk

# Window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1440, 720 
TILE_SIZE = 64

# Font settings
FONT_PATH = join('fonts', 'QuinqueFive.ttf')

# Background settings
MENU_BACKGROUND_PATH = join('images', 'ui', 'menu_background.png')

# Loading screen settings
LOADING_ANIMATION_PATH = join('images', 'ui', 'loading')
LOADING_DURATION = 3000  # 3 seconds in milliseconds

# Audio settings
AUDIO_SHOOT = join('audio', 'shoot.mp3')
AUDIO_IMPACT = join('audio', 'impact.mp3')
AUDIO_PLAYER_DEATH = join('audio', 'player_death.mp3')
AUDIO_PLAYER_REVIVE = join('audio', 'player_revive.mp3')
AUDIO_BUTTON_CLICK = join('audio', 'button_click.mp3')  # Also used for pause
AUDIO_MENU_MUSIC = join('audio', 'menu_music.mp3')
AUDIO_GAME_MUSIC = join('audio', 'game_music.mp3')

# Player settings
PLAYER_SPEED = 500

# Enemy settings
ENEMY_SPEED = 200
ENEMY_SPAWN_RATE = 300  # milliseconds between enemy spawns

# Gun/Bullet settings
BULLET_SPEED = 1200
GUN_COOLDOWN = 100  # milliseconds between shots
BULLET_LIFETIME = 1000  # milliseconds before bullet disappears

# Health settings
PLAYER_MAX_LIVES = 4
INVULNERABILITY_DURATION = 1000  # milliseconds of invulnerability after getting hit
DEATH_EFFECT_RADIUS = 200  # radius to kill enemies when player gets hit