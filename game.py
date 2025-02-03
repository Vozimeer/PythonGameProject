import pygame
import random
import time
import math
import sys

from constants import WIDTH, HEIGHT, FPS, WHITE, EXPLOSION_COLOR, BACKGROUND_COLOR, BORDER_COLOR, PLAYER_SIZE, \
    HUNTER_SIZE, FONT_SIZE, \
    PUSH_DISTANCE, PLAYER_BASE_SPEED, MAX_SPEED_MULTIPLIER, INERTIA_DECAY, PUSH_FACTOR, LEVEL_DURATION, LEVELS_COUNT, \
    HIGHSCORE_FILE, MIN_HUNTER_DISTANCE, BORDER_SIZE, FAN_SIZE, LEVEL_SETTINGS

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pictures/ping2.png")  # Загружаем пингвина
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = [0, 0]

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        distance = math.hypot(dx, dy)

        if 0 < distance < PUSH_DISTANCE:
            speed_multiplier = (1 - distance / PUSH_DISTANCE) * MAX_SPEED_MULTIPLIER + 1
            speed = PLAYER_BASE_SPEED * speed_multiplier
            self.speed[0] += -dx / distance * speed * PUSH_FACTOR
            self.speed[1] += -dy / distance * speed * PUSH_FACTOR

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        self.speed[0] *= INERTIA_DECAY
        self.speed[1] *= INERTIA_DECAY

        self.rect.clamp_ip(pygame.Rect(BORDER_SIZE, BORDER_SIZE, WIDTH - 2 * BORDER_SIZE, HEIGHT - 2 * BORDER_SIZE))

        if self.rect.left == BORDER_SIZE or self.rect.right == WIDTH - BORDER_SIZE:
            self.speed[0] = 0
        if self.rect.top == BORDER_SIZE or self.rect.bottom == HEIGHT - BORDER_SIZE:
            self.speed[1] = 0


class Target(pygame.sprite.Sprite):
    def __init__(self, size, speed, moves=True):
        super().__init__()
        self.image = pygame.image.load("pictures/fish.png")  # Загружаем рыбу
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = [random.choice([-1, 1]) * speed, random.choice([-1, 1]) * speed]
        self.moves = moves

    def reset_position(self):
        self.rect.x = random.randint(BORDER_SIZE, WIDTH - self.rect.width - BORDER_SIZE)
        self.rect.y = random.randint(BORDER_SIZE, HEIGHT - self.rect.height - BORDER_SIZE)

    def update(self):
        if self.moves:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]

            if self.rect.left < BORDER_SIZE or self.rect.right > WIDTH - BORDER_SIZE:
                self.speed[0] *= -1
            if self.rect.top < BORDER_SIZE or self.rect.bottom > HEIGHT - BORDER_SIZE:
                self.speed[1] *= -1


class Hunter(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("pictures/hunter.png")  # Загружаем охотника
        self.image = pygame.transform.scale(self.image, (HUNTER_SIZE, HUNTER_SIZE))
        self.rect = self.image.get_rect()
        self.speed = speed

    def reset_position(self, player):
        while True:
            self.rect.x = random.randint(BORDER_SIZE, WIDTH - HUNTER_SIZE - BORDER_SIZE)
            self.rect.y = random.randint(BORDER_SIZE, HEIGHT - HUNTER_SIZE - BORDER_SIZE)
            if math.hypot(self.rect.centerx - player.rect.centerx,
                          self.rect.centery - player.rect.centery) >= MIN_HUNTER_DISTANCE:
                break

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.rect.x += dx / distance * self.speed
            self.rect.y += dy / distance * self.speed


class Animation(pygame.sprite.Sprite):
    def __init__(self, center, target_size):
        super().__init__()
        self.frames = [pygame.Surface((target_size, target_size)) for _ in range(6)]
        for i, frame in enumerate(self.frames):
            frame.fill(WHITE)
            pygame.draw.circle(frame, EXPLOSION_COLOR, (target_size // 2, target_size // 2),
                               (target_size // 2) * (i + 1) / 6)
            frame.set_colorkey(WHITE)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center)
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 3:
            self.frame_timer = 0
            if self.frames:
                self.image = self.frames.pop(0)
            else:
                self.kill()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пингвийский Дрифт")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)


def load_best_score():
    try:
        with open(HIGHSCORE_FILE, "r") as file:
            return int(file.readline().strip())
    except (FileNotFoundError, ValueError):
        return 0


def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=(x, y)))


def display_screen(lines, wait_for_key=True):
    screen.fill(BACKGROUND_COLOR)
    for i, line in enumerate(lines):
        draw_text(line, WIDTH // 2, HEIGHT // (len(lines) + 1) * (i + 1))
    pygame.display.flip()
    if wait_for_key:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
    else:
        time.sleep(1)


def game(level_num):
    settings = LEVEL_SETTINGS[level_num]
    player = Player()
    target = Target(settings["target_size"], settings["target_speed"], settings["target_moves"])
    all_sprites = pygame.sprite.Group(player, target)

    cursor_image = pygame.image.load("pictures/fan2.png")  # Меняем курсор на вентилятор
    cursor_image = pygame.transform.scale(cursor_image, (FAN_SIZE, FAN_SIZE))

    background = pygame.image.load("pictures/fon.jpg")  # Загружаем фон 
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    hunter = None
    if settings["hunter_enabled"]:
        hunter = Hunter(settings["hunter_speed"])
        hunter.reset_position(player)
        all_sprites.add(hunter)

    animations = pygame.sprite.Group()
    score = 0
    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()
        target.update()
        if hunter:
            hunter.update(player)

        if pygame.sprite.collide_rect(player, target):
            score += settings["score_multiplier"]
            animations.add(Animation(target.rect.center, settings["target_size"]))
            target.reset_position()

        if hunter and pygame.sprite.collide_rect(player, hunter):
            running = False
            score = 0

        if time.time() - start_time >= LEVEL_DURATION:
            running = False

        # Отображаем фон
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, BORDER_COLOR, (0, 0, BORDER_SIZE, HEIGHT))
        pygame.draw.rect(screen, BORDER_COLOR, (WIDTH - BORDER_SIZE, 0, BORDER_SIZE, HEIGHT))
        pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, BORDER_SIZE))
        pygame.draw.rect(screen, BORDER_COLOR, (0, HEIGHT - BORDER_SIZE, WIDTH, BORDER_SIZE))

        all_sprites.draw(screen)
        animations.update()
        animations.draw(screen)
        draw_text(f"Счёт: {score}", 70, 30)
        draw_text(f"Время: {int(max(0, LEVEL_DURATION - (time.time() - start_time)))}", WIDTH - 70, 30)
        draw_text(f"Уровень: {level_num}", WIDTH // 2, 30)

        pygame.mouse.set_visible(False)  # Скрываем дефолтный курсор
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_image, (
            mouse_x - cursor_image.get_width() // 2, mouse_y - cursor_image.get_height() // 2))  # показываем вентилятор

        pygame.display.flip()
        clock.tick(FPS)

    return score, hunter and pygame.sprite.collide_rect(player, hunter)


display_screen(["Пингвийский Дрифт", "Нажмите любую кнопку, чтобы начать"])

total_score = 0
for level in range(1, LEVELS_COUNT + 1):
    display_screen([f"Уровень {level}"], wait_for_key=False)
    level_score, caught_by_hunter = game(level)
    if caught_by_hunter:
        total_score = 0
        break
    total_score += level_score

best_score = load_best_score()
if total_score > best_score:
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(total_score) + "\n")
    text_lines = ["Игра окончена", f"Ваш счёт: {total_score}", "Новый рекорд!",
                  "Нажмите любую кнопку, чтобы продолжить"]
else:
    text_lines = ["Игра окончена", f"Ваш счёт: {total_score}", f"Лучший счет: {best_score}",
                  "Нажмите любую кнопку, чтобы продолжить"]
display_screen(text_lines)

pygame.quit()
