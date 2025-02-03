WIDTH, HEIGHT = 900, 700
FPS = 60
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 162, 135)
TARGET_COLOR = (255, 162, 0)
HUNTER_COLOR = (245, 0, 29)
EXPLOSION_COLOR = (255, 103, 0)
BACKGROUND_COLOR = (31, 31, 31)
BORDER_COLOR = (28, 28, 28)
PLAYER_SIZE = 100
HUNTER_SIZE = 70
FONT_SIZE = 30
PUSH_DISTANCE = 120
PLAYER_BASE_SPEED = 3
MAX_SPEED_MULTIPLIER = 2
INERTIA_DECAY = 0.95
PUSH_FACTOR = 0.1
LEVEL_DURATION = 30
LEVELS_COUNT = 3
HIGHSCORE_FILE = "highscore.txt"
MIN_HUNTER_DISTANCE = 150
BORDER_SIZE = 50
FAN_SIZE = 60
LEVEL_SETTINGS = {
    1: {"target_size": 50, "target_moves": True, "target_speed": 0, "score_multiplier": 1, "hunter_speed": 0,
        "hunter_enabled": False},
    2: {"target_size": 40, "target_moves": False, "target_speed": 0, "score_multiplier": 2, "hunter_speed": 1,
        "hunter_enabled": True},
    3: {"target_size": 40, "target_moves": True, "target_speed": 2, "score_multiplier": 3, "hunter_speed": 2,
        "hunter_enabled": True}
}
