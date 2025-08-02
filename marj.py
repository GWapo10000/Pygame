import tkinter as tk
from PIL import Image, ImageTk
import pygame
import sys
import os

# Global variable to store selected theme
selected_theme = "Smurf"  # Default

def run_game(theme):
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer - Finish Line")

    # Theme-based background image
    background_paths = {
        "Smurf": "img/smurf_background.png",
        "Monsters Inc": "img/monsters_background.png",
    }

    background_img = pygame.image.load(background_paths[theme])
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    # Character images
    if theme == "Smurf":
        player_img = pygame.image.load(r"C:\\xampp\\htdocs\\marj\\images\\papa smurf.png").convert_alpha()
        enemy_img = pygame.image.load(r"C:\\xampp\\htdocs\\marj\\images\\smurfette.png").convert_alpha()
    else:
        player_img = pygame.Surface((50, 50))
        player_img.fill((0, 0, 255))
        enemy_img = pygame.Surface((50, 50))
        enemy_img.fill((255, 0, 0))

    player_img = pygame.transform.scale(player_img, (50, 50))
    enemy_img = pygame.transform.scale(enemy_img, (50, 50))

    # Colors
    GREEN = (0, 200, 0)
    YELLOW = (255, 215, 0)
    RED = (200, 0, 0)

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
        screen.blit(background_img, (0, 0))

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

        # Gravity
        velocity_y += gravity
        player.y += velocity_y

        # Collision with platforms
        on_ground = False
        for plat in platforms:
            if player.colliderect(plat):
                if velocity_y > 0 and player.bottom - velocity_y <= plat.top:
                    player.bottom = plat.top
                    velocity_y = 0
                    on_ground = True

        # Enemy AI
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

        # Game Over condition
        if player.colliderect(enemy):
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, RED)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            result_message = "Game Over!"
            running = False

        # Win condition
        if player.colliderect(finish_line):
            font = pygame.font.SysFont(None, 72)
            text = font.render("You Win!", True, (0, 150, 0))
            screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            result_message = "You Win!"
            running = False

        # Draw game objects
        for plat in platforms:
            pygame.draw.rect(screen, GREEN, plat)
        pygame.draw.rect(screen, YELLOW, finish_line)
        screen.blit(player_img, (player.x, player.y))
        screen.blit(enemy_img, (enemy.x, enemy.y))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    show_try_again_screen(result_message, theme)

# ---------------------------
# Try Again Screen (Tkinter)
# ---------------------------
def show_try_again_screen(result_message, theme):
    def try_again():
        root.destroy()
        run_game(theme)

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
    global selected_theme
    root.destroy()
    run_game(selected_theme.get())

root = tk.Tk()
root.title("Platformer Menu")
root.geometry("300x250")

# Load and show menu background image
menu_bg_img = Image.open("img/smurf_background.png")
menu_bg_img = menu_bg_img.resize((300, 250))
menu_bg_photo = ImageTk.PhotoImage(menu_bg_img)

bg_label = tk.Label(root, image=menu_bg_photo)
bg_label.image = menu_bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Theme selection UI
label = tk.Label(root, text="Choose a Theme:", font=("Arial", 12), bg="white")
label.place(relx=0.5, y=30, anchor="center")

themes = ["Smurf", "Monsters Inc"]
selected_theme = tk.StringVar(value="Smurf")
theme_menu = tk.OptionMenu(root, selected_theme, *themes)
theme_menu.place(relx=0.5, y=60, anchor="center")

# Start and Exit buttons
start_button = tk.Button(root, text="Start Game", font=("Arial", 12), command=start_game)
start_button.place(relx=0.5, y=120, anchor="center")

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
exit_button.place(relx=0.5, y=160, anchor="center")

root.mainloop()