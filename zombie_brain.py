import pygame
import random


def best_score(score, best_try):
    if score > best_try:
        best_try = score
        return best_try
    return best_try

best_try = 0
score = 0
quit_game = False
while not quit_game:
    best_try = best_score(score, best_try)
    # Inizializza Pygame
    pygame.init()
    # Inizializza il mixer di pygame
    pygame.mixer.init()

    # Imposta le dimensioni della finestra
    window_width = 800
    window_height = 600

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Zombie Brains")

    # Definisci i colori
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)

    # Carica le immagini e i suoni
    zombie_head_up = pygame.image.load("assets/block_part/zombie_head_up.png")
    zombie_head_up = pygame.transform.scale(zombie_head_up, (20, 20))
    zombie_head_down = pygame.image.load("assets/block_part/zombie_head_down.png")
    zombie_head_down = pygame.transform.scale(zombie_head_down, (20, 20))
    zombie_head_left = pygame.image.load("assets/block_part/zombie_head_left.png")
    zombie_head_left = pygame.transform.scale(zombie_head_left, (20, 20))
    zombie_head_right = pygame.image.load("assets/block_part/zombie_head_right.png")
    zombie_head_right = pygame.transform.scale(zombie_head_right, (20, 20))
    brain = pygame.image.load("assets/block_part/brain.png")
    brain = pygame.transform.scale(brain, (20, 20))
    wall = pygame.image.load("assets/block_part/wall.png")
    wall = pygame.transform.scale(wall, (20, 20))
    eat_sound = pygame.mixer.Sound("assets/sounds/eating-sound-effect-36186.mp3")
    eat_sound.set_volume(0.5)
    crash_sound = pygame.mixer.Sound("assets/sounds/human-impact-on-ground-6982.mp3")
    crash_sound.set_volume(0.5)

    # Definisci le dimensioni dello zombie, del muro e del cervello
    zombie_size = 20
    brain_size = 20
    wall_size = 20

    # Inizializza il font per il punteggio e per il punteggio finale
    font_path = "assets/fonts/youmurdererbb_reg.ttf"
    font_size = 36
    font = pygame.font.Font(font_path, font_size)
    end_font = pygame.font.Font(font_path, 50)


    # Definisci la posizione iniziale dello zombie
    zombie_x = window_width // 2
    zombie_y = window_height // 2

    # Definisci il vettore di movimento iniziale
    x_change = 0
    y_change = 0

    # Crea cervello e crea muro iniziale
    brain_x = random.randrange(brain_size, window_width - brain_size, brain_size)
    brain_y = random.randrange(brain_size, window_height - brain_size, brain_size)
    wall_x = random.randrange(wall_size, window_width - wall_size, wall_size)
    wall_y = random.randrange(wall_size, window_height - wall_size, wall_size)

    # Controlla se il muro è stato generato nella stessa posizione dello zombie
    while wall_x == zombie_x and wall_x == zombie_y:
        wall_x = random.randrange(wall_size, window_width - wall_size, wall_size)
        wall_y = random.randrange(wall_size, window_height - wall_size, wall_size)

    walls = [(wall_x, wall_y)]

    # Inizializza il punteggio e la velocità e i cervelli presi
    score = 0
    speed = 8
    brain_taken = 0




    # funzione per generare il cervello
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
        score_text = font.render("Score: " + str(score) + " Best: " + str(best_try), True, green)
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
            crash_sound.play()
            game_over = True

        # Controlla le collisioni con il corpo dello zombie con il muro
        for wall_x, wall_y in walls:
            if zombie_x == wall_x and zombie_y == wall_y:
                crash_sound.play()
                game_over = True
                break

        # Controlla se lo zombie ha mangiato il cervello e genera un muro random
        if zombie_x == brain_x and zombie_y == brain_y:
            eat_sound.play()
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

            best_try = best_score(score, best_try)
        # Disegna il gioco
        draw_game()

        # Regola la velocità del gioco
        clock.tick(speed)

    # Schermata di punteggio finale
    close_game = False
    while not close_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game = True
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    close_game = True
                    quit_game = True
                elif event.key == pygame.K_r:
                    close_game = True
                    quit_game = False

        text_score = end_font.render("Final Score: " + str(score), True, (red))
        text_best_score = end_font.render("The best Score: " + str(best_try), True, (red))
        text_quit = end_font.render("Press Return to Quit", True, (red))
        text_replay = end_font.render("Or press R to Replay", True, (red))

        # Ricrea la schemata di gioco per poi metterci il punteggio
        window.fill(black)
        window.blit(brain, (brain_x, brain_y))
        for wall_x, wall_y in walls:
            window.blit(wall, (wall_x, wall_y))

        window.blit(text_score, (window_width // 2, window_height // 2))
        window.blit(text_best_score, (window_width // 2, window_height // 2 + 60))
        window.blit(text_quit, (window_width // 2, window_height // 2 + 120))
        window.blit(text_replay, (window_width // 2, window_height // 2 + 180))
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

