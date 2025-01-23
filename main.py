import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

# Розміри екрану
screen = pygame.display.set_mode((800, 600))  # Встановлюємо розміри екрану 800x600
pygame.display.set_caption("Проста гра на Pygame")

background = pygame.image.load("icon/background.jpg")
background = pygame.transform.scale(background, (800, 600))

# Завантажуємо звукові ефекти
pygame.mixer.music.load("sound/music.mp3")  # Фоновий звук
pygame.mixer.music.play(-1, 0.0)  # Зациклюємо фон, параметр -1 означає нескінченне повторення

shoot_sound = pygame.mixer.Sound("sound/shoot_sound.wav")  # Звук вистрілу
hit_sound = pygame.mixer.Sound("sound/hit_sound.wav")    # Звук попадання
game_over_sound = pygame.mixer.Sound("sound/game_over.wav")  # Звук завершення гри

# Завантажуємо зображення для сердечок
heart_image = pygame.image.load("icon/heart.png")  # Завантажуємо зображення для серця
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Змінюємо розмір

# Клас для гравця
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icon/space.png")  # Завантажуємо зображення гравця
        self.image = pygame.transform.scale(self.image, (50, 50))  # Змінюємо розмір
        self.rect = self.image.get_rect()  # Отримуємо прямокутник для спрайта
        self.rect.centerx = screen.get_width() // 2
        self.rect.bottom = screen.get_height() - 10  # Розташовуємо гравця біля нижньої частини екрану
        self.health = 3  # Початкове здоров'я (3 сердечка)

    def update(self, keys):
        # Оновлення позиції гравця в залежності від натискання клавіш
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += 5

# Клас для ворогів
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("icon/enemy.png")  # Завантажуємо зображення ворога
        self.image = pygame.transform.scale(self.image, (50, 50))  # Змінюємо розмір
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_shot_time = 0  # Час останнього вистрілу

    def update(self, direction):
        # Рух ворога по осі X
        self.rect.x += direction

        # Випадковий шанс на постріл
        if random.random() < 0.01:  # 1% шанс на постріл кожну кадр
            if pygame.time.get_ticks() - self.last_shot_time > 2000:  # Вистрілює не частіше, ніж раз на секунду
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                enemy_bullet_group.add(bullet)
                self.last_shot_time = pygame.time.get_ticks()

# Клас для великого боса
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("icon/boss.png")  # Завантажуємо зображення боса
        self.image = pygame.transform.scale(self.image, (100, 100))  # Змінюємо розмір
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_width() // 2
        self.rect.top = 50  # Розташовуємо боса в верхній частині екрану
        self.health = 100  # Більше здоров'я для боса

    def update(self):
        # Бос рухається тільки вліво і вправо
        self.rect.x += 2
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.rect.x -= 2  # Стоп на межах екрану

# Клас для снарядів гравця
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))  # Збільшений розмір снаряду
        self.image.fill((255, 255, 0))  # Жовтий колір
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y  # Розташовуємо на позиції гравця
        self.direction = -1  # Напрямок вгору (від'ємне значення по осі Y)

    def update(self):
        # Рух снаряду вгору
        self.rect.y += self.direction * 5  # Снаряд рухається вгору
        if self.rect.bottom < 0:  # Якщо снаряд вийшов за верхній край екрану
            self.kill()  # Видаляємо снаряд

# Клас для снарядів ворогів
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Встановлюємо розміри снаряду
        self.image.fill((255, 0, 0))  # Червоний колір
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        # Рух снаряду вниз
        self.rect.y += 3
        if self.rect.top > 600:  # Якщо снаряд вийшов за нижню межу екрану, видаляємо його
            self.kill()

# Функція для генерації ворогів в 5 рядах по 10 ворогів
def generate_enemies(level):
    enemies = pygame.sprite.Group()
    spacing_x = 70  # Відстань між ворогами по горизонталі
    spacing_y = 70  # Відстань між ворогами по вертикалі
    max_columns = 10  # Кількість ворогів по горизонталі
    max_rows = 5  # Кількість ворогів по вертикалі

    # Кількість ворогів залежить від рівня
    if level >= 10:
        max_rows = 1  # На 10-му рівні кількість ворогів зменшується до одного ряду
    for row in range(max_rows):
        for col in range(max_columns):
            x = col * spacing_x + 50  # Відстань між ворогами по горизонталі
            y = row * spacing_y + 50  # Відстань між ворогами по вертикалі
            enemy = Enemy(x, y)
            enemies.add(enemy)
    return enemies

# Ініціалізація гравця та групи ворогів
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = generate_enemies(1)  # Створення початкових ворогів
bullet_group = pygame.sprite.Group()  # Група для снарядів
enemy_bullet_group = pygame.sprite.Group()  # Група для снарядів ворогів

# Кольори
WHITE = (255, 255, 255)

# Створення шрифту для рахунку
font = pygame.font.SysFont("Arial", 30)

# Головний цикл гри
clock = pygame.time.Clock()
score = 0
level = 1  # Початковий рівень
direction = 1
enemy_speed = 2

# Створення боса на 10-му рівні
boss = None

while True:
    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Якщо натиснута клавіша "Пробіл" (стрільба)
                bullet_left = Bullet(player.rect.centerx - 10, player.rect.top)  # Снаряд вліво
                bullet_right = Bullet(player.rect.centerx + 10, player.rect.top)  # Снаряд вправо
                bullet_group.add(bullet_left, bullet_right)
                shoot_sound.play()  # Відтворюємо звук вистрілу

    # Отримання натискання клавіш
    keys = pygame.key.get_pressed()

    # Оновлення позиції гравця
    player_group.update(keys)

    # Оновлення ворогів або боса
    if level < 10:
        for enemy in enemy_group:
            enemy.update(direction)
        # Перевірка на досягнення правого або лівого краю екрану
        for enemy in enemy_group:
            if enemy.rect.right >= 800 or enemy.rect.left <= 0:
                direction *= -1
                break
    elif boss:
        boss.update()

    # Оновлення снарядів
    bullet_group.update()
    enemy_bullet_group.update()

    # Перевірка на зіткнення між снарядами гравця і снарядами ворогів
    for bullet in bullet_group:
        for enemy_bullet in enemy_bullet_group:
            if pygame.sprite.collide_rect(bullet, enemy_bullet):
                bullet.kill()  # Видаляємо снаряд гравця
                enemy_bullet.kill()  # Видаляємо снаряд ворога

    # Перевірка на зіткнення з ворогами
    for bullet in bullet_group:
        if level < 10:  # Для рівнів менше 10
            enemies_hit = pygame.sprite.spritecollide(bullet, enemy_group, True)  # Знищуємо ворогів при зіткненні
            if enemies_hit:
                bullet.kill()  # Видаляємо снаряд після зіткнення
                score += 1  # Збільшуємо рахунок
                hit_sound.play()  # Відтворюємо звук попадання
        elif boss:  # Якщо босс
            if pygame.sprite.collide_rect(bullet, boss):  # Якщо снаряд потрапляє в боса
                bullet.kill()  # Видаляємо снаряд після зіткнення
                boss.health -= 10  # Зменшуємо здоров'я боса
                hit_sound.play()  # Відтворюємо звук попадання
                if boss.health <= 0:  # Якщо босс вбитий
                    boss.kill()  # Видаляємо боса
                    score += 50  # Додаємо бонусні очки
                    level += 1  # Переходимо на наступний рівень
                    enemy_group = generate_enemies(level)  # Створюємо нових ворогів для наступного рівня
                    if level >= 10:  # Створення боса на 10-му рівні
                        boss = Boss()

    # Якщо всі вороги знищені на рівні (для звичайних рівнів, не для боса)
    if level < 10 and len(enemy_group) == 0:
        level += 1  # Переходимо на наступний рівень
        enemy_group = generate_enemies(level)  # Генеруємо нових ворогів

    # Перевірка на зіткнення між снарядами ворогів і гравцем
    for enemy_bullet in enemy_bullet_group:
        if pygame.sprite.collide_rect(enemy_bullet, player):
            enemy_bullet.kill()  # Видаляємо снаряд ворога
            player.health -= 1  # Забираємо життя гравця
            hit_sound.play()  # Звук попадання
            if player.health <= 0:  # Якщо у гравця закінчилося здоров'я
                game_over_sound.play()  # Відтворюємо звук завершення гри
                pygame.time.wait(1000)  # Затримка перед завершенням гри
                pygame.quit()  # Виходимо з гри
                sys.exit()  # Завершуємо програму

    # Малюємо фон
    screen.blit(background, (0, 0))

    # Малюємо групи спрайтів
    player_group.draw(screen)
    enemy_group.draw(screen)
    bullet_group.draw(screen)
    enemy_bullet_group.draw(screen)

    # Малюємо рівень та рахунок
    level_text = font.render(f"Level: {level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (10, 40))

    # Малюємо здоров'я гравця
    for i in range(player.health):
        screen.blit(heart_image, (760 - (i * 40), 10))

    # Оновлення екрану
    pygame.display.update()

    # Затримка для контролю FPS
    clock.tick(60)
