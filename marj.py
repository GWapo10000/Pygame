import tkinter as tk
import pygame
import sys

def run_game():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer - Finish Line")

    # Colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    YELLOW = (255, 215, 0)

    # Load and scale background image
    background_img = pygame.image.load("img/smurf_background.png")  # Make sure this file exists
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Player setup
    player = pygame.Rect(100, 500, 50, 50)
    velocity_y = 0
    gravity = 1
    jump_power = 15
    player_speed = 5
    on_ground = False

    # Enemy setup
    enemy = pygame.Rect(700, 500, 50, 50)
    enemy_speed = 2

    # Platforms
    platforms = [
        pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
        pygame.Rect(100, 520, 150, 20),
        pygame.Rect(300, 460, 150, 20),
        pygame.Rect(500, 400, 150, 20),
        pygame.Rect(200, 340, 150, 20)
    ]

    # Finish line
    finish_line = pygame.Rect(WIDTH - 70, HEIGHT - 70, 40, 50)

    clock = pygame.time.Clock()
    running = True
    result_message = ""

    while running:
        screen.blit(background_img, (0, 0))  # Draw background image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = -jump_power
            on_ground = False

        # Gravity for player
        velocity_y += gravity
        player.y += velocity_y

        # Player collision with platforms
        on_ground = False
        for plat in platforms:
            if player.colliderect(plat):
                if velocity_y > 0 and player.bottom - velocity_y <= plat.top:
                    player.bottom = plat.top
                    velocity_y = 0
                    on_ground = True

        # Enemy chases player horizontally
        if enemy.x < player.x:
            enemy.x += enemy_speed
        elif enemy.x > player.x:
            enemy.x -= enemy_speed

        # Enemy gravity
        enemy.y += gravity
        for plat in platforms:
            if enemy.colliderect(plat):
                if enemy.bottom - gravity <= plat.top:
                    enemy.bottom = plat.top
                    break

        # Check collision: player & enemy = game over
        if player.colliderect(enemy):
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, RED)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            result_message = "Game Over!"
            running = False

        # Check collision: player & finish line = win
        if player.colliderect(finish_line):
            font = pygame.font.SysFont(None, 72)
            text = font.render("You Win!", True, (0, 150, 0))
            screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            result_message = "You Win!"
            running = False

        # Draw platforms
        for plat in platforms:
            pygame.draw.rect(screen, GREEN, plat)

        # Draw finish line
        pygame.draw.rect(screen, YELLOW, finish_line)

        # Draw player and enemy
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, enemy)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    show_try_again_screen(result_message)

# -------------------------------
# Show Try Again screen (Tkinter)
# -------------------------------
def show_try_again_screen(result_message):
    def try_again():
        root.destroy()
        run_game()

    def exit_game():
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.title("Game Over")
    root.geometry("300x200")

    label = tk.Label(root, text=result_message, font=("Arial", 16))
    label.pack(pady=20)

    try_again_btn = tk.Button(root, text="Try Again", font=("Arial", 12), command=try_again)
    try_again_btn.pack(pady=10)

    exit_btn = tk.Button(root, text="Exit", font=("Arial", 12), command=exit_game)
    exit_btn.pack(pady=5)

    root.mainloop()

# ---------------------
# Main Menu (Tkinter)
# ---------------------
def start_game():
    root.destroy()
    run_game()

root = tk.Tk()
root.title("Platformer Menu")
root.geometry("300x200")

label = tk.Label(root, text="Welcome to the Platformer!", font=("Arial", 14))
label.pack(pady=20)

start_button = tk.Button(root, text="Start Game", font=("Arial", 12), command=start_game)
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
exit_button.pack(pady=5)

root.mainloop()