import tkinter as tk
from PIL import Image, ImageTk
import pygame
import sys
import os

selected_theme = "Smurf"

def run_game(level, theme, character):
    pygame.init()
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption(f"Platformer - Level {level}")

    background_paths = {
        "Smurf": "img/smurf_background.png",
        "Monsters Inc": "img/monsters_background.png",
    }

    background_img = pygame.image.load(background_paths[theme])
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    YELLOW = (255, 215, 0)

    character_paths = {
        "Papa Smurf": "C:/xampp/htdocs/marj/images/papa smurf.png",
        "Smurfette": "C:/xampp/htdocs/marj/images/smurfette.png",
    }

    player_image = pygame.image.load(character_paths[character])
    player_image = pygame.transform.scale(player_image, (50, 50))

    player = pygame.Rect(100, HEIGHT - 100, 50, 50)
    velocity_y = 0
    gravity = 1
    jump_power = 15
    player_speed = 8
    on_ground = False

    enemy = pygame.Rect(WIDTH - 100, HEIGHT - 100, 50, 50)
    enemy_speed = 2

    if level == 1:
        platforms = [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
            pygame.Rect(int(WIDTH * 0.12), HEIGHT - 100, 150, 20),
            pygame.Rect(int(WIDTH * 0.35), HEIGHT - 150, 150, 20),
            pygame.Rect(int(WIDTH * 0.60), HEIGHT - 210, 150, 20),
            pygame.Rect(int(WIDTH * 0.25), HEIGHT - 280, 150, 20),
        ]
        finish_line = pygame.Rect(WIDTH - 70, HEIGHT - 70, 40, 50)

    elif level == 2:
        # Lowered platforms for better reachability
        platforms = [
            pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
            pygame.Rect(WIDTH // 4, HEIGHT - 100, 110, 20),
            pygame.Rect(WIDTH // 2, HEIGHT - 140, 110, 20),
            pygame.Rect(WIDTH // 3, HEIGHT - 200, 110, 20),
            pygame.Rect(WIDTH // 1.5, HEIGHT - 230, 100, 20),
        ]
        finish_line = pygame.Rect(int(WIDTH * 0.85), HEIGHT // 2, 40, 50)

    clock = pygame.time.Clock()
    running = True
    result_message = ""

    font_level = pygame.font.SysFont(None, 36)

    while running:
        screen.blit(background_img, (0, 0))
        level_text = font_level.render(f"Level {level}", True, WHITE)
        screen.blit(level_text, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = -jump_power
            on_ground = False

        velocity_y += gravity
        player.y += velocity_y

        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
            velocity_y = 0
            on_ground = True

        on_ground = False
        for plat in platforms:
            if player.colliderect(plat):
                if velocity_y > 0 and player.bottom - velocity_y <= plat.top:
                    player.bottom = plat.top
                    velocity_y = 0
                    on_ground = True

        if enemy.x < player.x:
            enemy.x += enemy_speed
        elif enemy.x > player.x:
            enemy.x -= enemy_speed

        enemy.y += gravity
        for plat in platforms:
            if enemy.colliderect(plat):
                if enemy.bottom - gravity <= plat.top:
                    enemy.bottom = plat.top
                    break

        if player.colliderect(enemy):
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, RED)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(2000)
            result_message = "Game Over!"
            running = False

        if player.colliderect(finish_line):
            if level == 1:
                pygame.time.wait(1000)
                run_game(2, theme, character)
                return
            else:
                font = pygame.font.SysFont(None, 72)
                text = font.render("You Win!", True, (0, 150, 0))
                screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
                pygame.display.update()
                pygame.time.wait(2000)
                result_message = "You Win!"
                running = False

        for plat in platforms:
            pygame.draw.rect(screen, GREEN, plat)
        pygame.draw.rect(screen, YELLOW, finish_line)
        screen.blit(player_image, player)
        pygame.draw.rect(screen, RED, enemy)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    show_try_again_screen(result_message, theme, character)

def show_try_again_screen(result_message, theme, character):
    def try_again():
        root.destroy()
        run_game(1, theme, character)

    def exit_game():
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.title("Game Over")
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    frame = tk.Frame(root, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(frame, text=result_message, font=("Arial", 36), bg="white")
    label.pack(pady=40)

    try_again_btn = tk.Button(frame, text="Try Again", font=("Arial", 24), command=try_again)
    try_again_btn.pack(pady=20)

    exit_btn = tk.Button(frame, text="Exit", font=("Arial", 24), command=exit_game)
    exit_btn.pack(pady=10)

    root.mainloop()

def start_game():
    global selected_theme, selected_character
    root.destroy()
    run_game(1, selected_theme.get(), selected_character.get())

# Main Menu
root = tk.Tk()
root.title("Platformer Menu")
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

menu_bg_img = Image.open("img/smurf_background.png")
menu_bg_img = menu_bg_img.resize((screen_width, screen_height))
menu_bg_photo = ImageTk.PhotoImage(menu_bg_img)

bg_label = tk.Label(root, image=menu_bg_photo)
bg_label.image = menu_bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

label_theme = tk.Label(root, text="Choose a Theme:", font=("Arial", 24), bg="white")
label_theme.place(relx=0.5, y=100, anchor="center")

themes = ["Smurf", "Monsters Inc"]
selected_theme = tk.StringVar(value="Smurf")
theme_menu = tk.OptionMenu(root, selected_theme, *themes)
theme_menu.config(font=("Arial", 18))
theme_menu.place(relx=0.5, y=150, anchor="center")

label_character = tk.Label(root, text="Choose Character:", font=("Arial", 24), bg="white")
label_character.place(relx=0.5, y=230, anchor="center")

characters = ["Papa Smurf", "Smurfette"]
selected_character = tk.StringVar(value="Papa Smurf")
character_menu = tk.OptionMenu(root, selected_character, *characters)
character_menu.config(font=("Arial", 18))
character_menu.place(relx=0.5, y=280, anchor="center")

start_button = tk.Button(root, text="Start Game", font=("Arial", 24), command=start_game)
start_button.place(relx=0.5, y=370, anchor="center")

exit_button = tk.Button(root, text="Exit", font=("Arial", 24), command=root.quit)
exit_button.place(relx=0.5, y=440, anchor="center")

root.mainloop()
