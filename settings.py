from pygame.locals import *

# Generic
GAME_TITLE = 'Moon Patrol'
GAME_WIDTH = 1000
GAME_HEIGHT = 500
FPS = 60
SCROLL_SPEED = 2
PLAYER_HEALTH = 10
PLAYER_VEL_X = 7
PLAYER_VEL_Y = 9
PLAYER_START_POS_X = 20
PLAYER_START_POS_Y = 315

# Sprites
CAR_WIDTH = 90
CAR_HEIGHT = 55
UFO1_WIDTH = 50
UFO1_HEIGHT = 50
UFO2_WIDTH = 45
UFO2_HEIGHT = 45
SPIKES_WIDTH = 60
SPIKES_HEIGHT = 180
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 60

# Assets
CAR_SPRITE = 'assets/car.png'
UFO1_SPRITE = 'assets/ufo1.png'
UFO2_SPRITE = 'assets/ufo2.png'
SPIKES_SPRITE = 'assets/spikes.png'
BLOCK_SPRITE = 'assets/block.png'
CITY_BG = 'assets/city_bg.png'
GAME_LOGO = 'assets/moon-patrol-logo.png'
UP_ARROW = 'assets/up-arrow.png'
DOWN_ARROW = 'assets/down-arrow.png'
LEFT_ARROW = 'assets/left-arrow.png'
RIGHT_ARROW = 'assets/right-arrow.png'
SPACE_BAR = 'assets/space-bar.png'

#Music
BG_MUSIC='assets/bgmusic.wav'
BULLET_SOUND = 'assets/laser.wav'

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN=(165,42,42)
BLUE=(100, 149, 237)
PURPLE=(186, 52, 235)
GREEN2 = (52,235,171)

# Events
EVENT_OBSTACLE = USEREVENT + 1
EVENT_UFO_1 = USEREVENT + 2
EVENT_UFO_2 = USEREVENT + 3

# Debug
DEBUG_HITBOXES = False
