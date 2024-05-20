import pygame
import random

# Inizializza Pygame
pygame.init()

# Imposta le dimensioni della finestra
window_width = 800
window_height = 600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Zombie Brains")

# Definisci i colori
black = (0, 0, 0)
green = (0, 255, 0)


# Carica le immagini
zombie_head_up = pygame.image.load("block_part/zombie_head_up.png")
zombie_head_up = pygame.transform.scale(zombie_head_up, (20, 20))
zombie_head_down = pygame.image.load("block_part/zombie_head_down.png")
zombie_head_down = pygame.transform.scale(zombie_head_down, (20, 20))
zombie_head_left = pygame.image.load("block_part/zombie_head_left.png")
zombie_head_left = pygame.transform.scale(zombie_head_left, (20, 20))
zombie_head_right = pygame.image.load("block_part/zombie_head_right.png")
zombie_head_right = pygame.transform.scale(zombie_head_right, (20, 20))
brain = pygame.image.load("block_part/brain.png")
brain = pygame.transform.scale(brain, (20, 20))
wall = pygame.image.load("block_part/wall.png")
wall = pygame.transform.scale(wall, (20, 20))

# Definisci le dimensioni dello zombie, del muro e del cervello
zombie_size = 20
brain_size = 20
wall_size = 20

# Definisci la posizione iniziale dello zombie
zombie_x = window_width // 2
zombie_y = window_height // 2

# Definisci il vettore di movimento iniziale
x_change = 0
y_change = 0


# Crea cervello e crea muro iniziale
brain_x = random.randrange(brain_size, window_width - brain_size, brain_size)
brain_y = random.randrange(brain_size, window_height - brain_size, brain_size)
wall_x = random.randrange(wall_size, window_height - wall_size, wall_size)
wall_y = random.randrange(wall_size, window_height - wall_size, wall_size)

walls = [(wall_x, wall_y)]

# Inizializza il punteggio e la velocità e i cervelli presi
score = 0
speed = 8
brain_taken = 0

#funzione per generare il cervello
def generate_brain_position():
    brain_x = random.randrange(brain_size, window_width - brain_size, brain_size)
    brain_y = random.randrange(brain_size, window_height - brain_size, brain_size)

    # Verificare se la posizione del cervello non collide con i muri esistenti
    while any((brain_x == wall_x and brain_y == wall_y) for wall_x, wall_y in walls):
        brain_x = random.randrange(brain_size, window_width - brain_size, brain_size)
        brain_y = random.randrange(brain_size, window_height - brain_size, brain_size)

    return brain_x, brain_y


# Funzione per disegnare il gioco
def draw_game():
    # Cancella la finestra
    window.fill(black)

    # Disegna il punteggio
    score_text = font.render("Score: " + str(score), True, green)
    window.blit(score_text, (10, 10))

    # Disegna lo zombie
    if x_change == 0 and y_change == -zombie_size:
        window.blit(zombie_head_up, (zombie_x, zombie_y))
    elif x_change == 0 and y_change == zombie_size:
        window.blit(zombie_head_down, (zombie_x, zombie_y))
    elif x_change == -zombie_size and y_change == 0:
        window.blit(zombie_head_left, (zombie_x, zombie_y))
    elif x_change == zombie_size and y_change == 0:
        window.blit(zombie_head_right, (zombie_x, zombie_y))

    # Disegna il cervello
    window.blit(brain, (brain_x, brain_y))

    # Disegna i muri
    for wall_x, wall_y in walls:
        window.blit(wall, (wall_x, wall_y))

    # Aggiorna il display
    pygame.display.update()


# Inizializza il font per il punteggio
font_path = "fonts/youmurdererbb_reg.ttf"
font_size = 36
font = pygame.font.Font(font_path, font_size)

# Inizializza il clock di Pygame
clock = pygame.time.Clock()

# Game loop
game_over = False
while not game_over:
    # Gestisci gli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                x_change = -zombie_size
                y_change = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                x_change = zombie_size
                y_change = 0
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                x_change = 0
                y_change = -zombie_size
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                x_change = 0
                y_change = zombie_size

    # Muovi zombie
    zombie_x += x_change
    zombie_y += y_change

    # Controlla le collisioni con i bordi della finestra
    if zombie_x < 0 or zombie_x >= window_width or zombie_y < 0 or zombie_y >= window_height:
        game_over = True

    # Controlla le collisioni con il corpo dello zombie con il muro
    for wall_x, wall_y in walls:
        if zombie_x == wall_x and zombie_y == wall_y:
            game_over = True
            break

    # Controlla se lo zombie ha mangiato il cervello e genera un muro random
    if zombie_x == brain_x and zombie_y == brain_y:
        wall_x = random.randrange(wall_size, window_width - wall_size, wall_size)
        wall_y = random.randrange(wall_size, window_height - wall_size, wall_size)
        brain_x, brain_y = generate_brain_position()

        walls.append((wall_x, wall_y))  # Aggiungi nuove coordinate del muro come tupla

        brain_taken += 1

        if brain_taken < 10:
            score += 5
        elif brain_taken < 20:
            score += 15
        elif brain_taken < 40:
            score += 40
        elif brain_taken > 40:
            score += 50

    # Disegna il gioco
    draw_game()

    # Regola la velocità del gioco
    clock.tick(speed)

# Quit Pygame
pygame.quit()
