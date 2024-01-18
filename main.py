import random
import sqlite3
import sys

import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox

from button import ButtonsWithImages

try:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
except sqlite3.Error:
    print("Не удалось подключиться к базе данных.")

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('9925bd28798144c.mp3')
pygame.mixer.music.play()

BACKGROUND = (255, 255, 255)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('GunFight')

new_gun = False
right_password = False
load_main_levels = False
current_email = ""
# is_logged_in - проверка авторизации пользователя. True - вход в аккаунт выполнен.
is_logged_in = False
result = bool()


# Проверка существования учётной записи осуществляется по адресу электронной почты.
def whether_user(email, password):
    global right_password
    with con:
        all_emails = cur.execute(
            "SELECT email FROM Users"
        ).fetchall()
        if (email,) in all_emails:
            request = "SELECT password FROM users WHERE email = ?"
            original_password = cur.execute(
                request, (email,)
            ).fetchall()
            if original_password[0][0] == password:
                right_password = True
                return True
            if original_password[0][0] != password:
                right_password = False
                return True
        else:
            return False


def create_account_or_login(email, password):
    global right_password
    global is_logged_in
    check_result = whether_user(email, password)
    if check_result and right_password:
        is_logged_in = True
    if check_result and not right_password:
        is_logged_in = False
    elif not check_result:
        with con:
            sql = "INSERT INTO Users (email, password, results, money) values(?, ?, ?, ?)"
            data = [(email, password, "0 0", 0)]
            con.executemany(sql, data)
        is_logged_in = True
    return is_logged_in


def add_money():
    with con:
        request = "SELECT money FROM Users WHERE email = ?"
        money = cur.execute(
            request, (current_email,)
        ).fetchall()[0][0]
        request = (
            "UPDATE users SET money = ? WHERE email = ?"
        )
        data = [(int(money) + 10, current_email)]
        con.executemany(request, data)


def add_results_to_database():
    global result
    with con:
        request = "SELECT results FROM Users WHERE email = ?"
        results = cur.execute(
            request, (current_email,)
        ).fetchall()
        results = results[0][0].split()
        request = (
            "UPDATE users SET results = ? WHERE email = ?"
        )
        if result:
            data = [(f"{int(results[0]) + 1} {results[1]}", current_email)]
        else:
            data = [(f"{results[0]} {int(results[1]) + 1}", current_email)]
        con.executemany(request, data)


def open_main_menu():
    global load_main_levels
    main_menu_background = pygame.image.load("main_menu_background.jpeg")

    registration_button = ButtonsWithImages(190, 20, 200, 20, "личный кабинет",
                                            "main_menu_button.jpeg",
                                            "main_menu_hovered_button.jpeg")
    main_levels_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 200, 252, 74, "УРОВНИ",
                                           "main_menu_button.jpeg",
                                           "main_menu_hovered_button.jpeg")
    extra_levels_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 300, 252, 74, "ЕЩЁ УРОВНИ",
                                            "main_menu_button.jpeg",
                                            "main_menu_hovered_button.jpeg")
    market_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 400, 252, 74, "МАГАЗИН",
                                      "main_menu_button.jpeg",
                                      "main_menu_hovered_button.jpeg")

    running = True
    while running:
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(main_menu_background, (0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("GUNFIGHT", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, 100))
        WINDOW.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == registration_button:
                if is_logged_in:
                    open_personal_account()
                else:
                    open_registration()

            if event.type == pygame.USEREVENT and event.button == main_levels_button:
                load_main_levels = True
                open_level_selection()

            if event.type == pygame.USEREVENT and event.button == extra_levels_button:
                open_level_selection()

            if event.type == pygame.USEREVENT and event.button == market_button:
                open_market()

            for button in [registration_button, main_levels_button, extra_levels_button, market_button]:
                button.handle_event(event)

        for button in [registration_button, main_levels_button, extra_levels_button, market_button]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(WINDOW)

        pygame.display.flip()


def open_registration():
    global current_email

    main_menu_background = pygame.image.load("main_menu_background.jpeg")

    back_button = ButtonsWithImages(20, 20, 70, 20, "назад",
                                    "main_menu_button.jpeg",
                                    "main_menu_hovered_button.jpeg")
    login_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 400, 252, 74, "ВОЙТИ",
                                     "main_menu_button.jpeg",
                                     "main_menu_hovered_button.jpeg")

    email_input_box = TextBox(WINDOW, 50, 200, 300, 60, colour=(255, 255, 255), fontSize=30,
                              borderColour=(212, 175, 158), textColour=(0, 0, 0), radius=10, borderThickness=5)
    password_input_box = TextBox(WINDOW, 50, 300, 300, 60, colour=(255, 255, 255), fontSize=30,
                                 borderColour=(212, 175, 158), textColour=(0, 0, 0), radius=10, borderThickness=5)

    running = True
    while running:
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(main_menu_background, (0, 0))

        font = pygame.font.Font(None, 50)
        text_surface = font.render("РЕГИСТРАЦИЯ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, 100))
        WINDOW.blit(text_surface, text_rect)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == login_button:
                email = email_input_box.getText()
                password = password_input_box.getText()
                create_account_or_login(email, password)
                current_email = email
                if is_logged_in:
                    open_personal_account()

            if event.type == pygame.USEREVENT and event.button == back_button:
                open_main_menu()

            for button in [back_button, login_button]:
                button.handle_event(event)

        pygame_widgets.update(events)

        for button in [back_button, login_button]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(WINDOW)

        pygame.display.flip()


def open_personal_account():
    main_menu_background = pygame.image.load("main_menu_background.jpeg")

    back_button = ButtonsWithImages(20, 20, 70, 20, "назад",
                                    "main_menu_button.jpeg",
                                    "main_menu_hovered_button.jpeg")

    running = True
    while running:
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(main_menu_background, (0, 0))

        font = pygame.font.Font(None, 50)
        text_surface = font.render("ЛИЧНЫЙ КАБИНЕТ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, 100))
        WINDOW.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                open_main_menu()

            back_button.handle_event(event)

        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(WINDOW)

        pygame.display.flip()


def open_level_selection():
    main_menu_background = pygame.image.load("main_menu_background.jpeg")

    back_button = ButtonsWithImages(20, 20, 70, 20, "назад",
                                    "main_menu_button.jpeg",
                                    "main_menu_hovered_button.jpeg")
    level1_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 200, 252, 74, "УРОВЕНЬ1",
                                      "main_menu_button.jpeg",
                                      "main_menu_hovered_button.jpeg")
    level2_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 300, 252, 74, "УРОВЕНЬ2",
                                      "main_menu_button.jpeg",
                                      "main_menu_hovered_button.jpeg")
    level3_button = ButtonsWithImages(WINDOW_WIDTH / 2 - (252 / 2), 400, 252, 74, "УРОВЕНЬ3",
                                      "main_menu_button.jpeg",
                                      "main_menu_hovered_button.jpeg")

    running = True
    while running:
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(main_menu_background, (0, 0))

        font = pygame.font.Font(None, 50)
        if load_main_levels:
            text = "ОСНОВНЫЕ УРОВНИ"
        else:
            text = "ЕЩЁ УРОВНИ"
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, 100))
        WINDOW.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == level2_button:
                if load_main_levels:
                    open_grass_level1()
                else:
                    open_snow_level1()

            if event.type == pygame.USEREVENT and event.button == level1_button:
                if load_main_levels:
                    open_grass_level2()
                else:
                    open_snow_level2()

            if event.type == pygame.USEREVENT and event.button == level3_button:
                if load_main_levels:
                    open_grass_level3()
                else:
                    open_snow_level3()

            if event.type == pygame.USEREVENT and event.button == back_button:
                open_main_menu()

            for button in [back_button, level1_button, level2_button, level3_button]:
                button.handle_event(event)

        for button in [back_button, level1_button, level2_button, level3_button]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(WINDOW)

        pygame.display.flip()


def open_market():
    global is_logged_in, new_gun
    with con:
        request = "SELECT money FROM Users WHERE email = ?"
        money = cur.execute(
            request, (current_email,)
        ).fetchall()[0][0]

    main_menu_background = pygame.image.load("main_menu_background.jpeg")

    back_button = ButtonsWithImages(20, 20, 70, 20, "назад",
                                    "main_menu_button.jpeg",
                                    "main_menu_hovered_button.jpeg")

    gun_button = ButtonsWithImages(20, 200, 150, 200, "10",
                                   "Иллюстрация_без_названия-2 3.png",
                                   "Иллюстрация_без_названия-2 3.png")

    running = True
    while running:
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(main_menu_background, (0, 0))

        if is_logged_in:
            font = pygame.font.Font(None, 50)
            text_surface = font.render(str(money), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(300, 50))
            WINDOW.blit(text_surface, text_rect)

        font1 = pygame.font.Font(None, 50)
        text_surface1 = font1.render("МАГАЗИН", True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect(center=(200, 100))
        WINDOW.blit(text_surface1, text_rect1)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                open_main_menu()

            if event.type == pygame.USEREVENT and event.button == gun_button:
                if money >= 10:
                    if not new_gun:
                        request = (
                            "UPDATE users SET money = ? WHERE email = ?"
                        )
                        data = [(int(money) - 10, current_email)]
                        con.executemany(request, data)
                    if new_gun:
                        new_gun = False
                    else:
                        new_gun = True

            for button in [back_button, gun_button]:
                button.handle_event(event)

        for button in [back_button, gun_button]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(WINDOW)

        pygame.display.flip()


def open_grass_level1():
    global result
    gunspeed = 20
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 2000)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон_трава.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат1.png').convert_alpha(),
        pygame.image.load('солдат2.png').convert_alpha(),
        pygame.image.load('солдат3.png').convert_alpha(),
        pygame.image.load('солдат4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 23
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(5 - play) + '/' + '5'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '23'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '20'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 5 and kol < 20:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 10
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
            playery += 10

            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # Стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 5:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level1()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        elif kol >= 20:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level1()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1

        clock.tick(10)
        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


def open_grass_level2():
    global result

    gunspeed = 30
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 1000)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон_трава.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат1.png').convert_alpha(),
        pygame.image.load('солдат2.png').convert_alpha(),
        pygame.image.load('солдат3.png').convert_alpha(),
        pygame.image.load('солдат4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 30
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(3 - play) + '/' + '5'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '30'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '25'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 5 and kol < 25:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 7
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
            playery += 10

            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 5:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level2()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        elif kol >= 25:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level2()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1
        clock.tick(10)

        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


def open_grass_level3():
    global result
    gunspeed = 30
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 1500)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон_трава.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат1.png').convert_alpha(),
        pygame.image.load('солдат2.png').convert_alpha(),
        pygame.image.load('солдат3.png').convert_alpha(),
        pygame.image.load('солдат4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 30
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(3 - play) + '/' + '5'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '30'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '29'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 3 and kol < 29:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 7
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
            playery += 10

            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 3:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level3()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        elif kol >= 29:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_grass_level3()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1
        clock.tick(10)

        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


def open_snow_level1():
    global result
    gunspeed = 20
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 2000)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон-снег.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат_снег_1.png').convert_alpha(),
        pygame.image.load('солдат_снег_2.png').convert_alpha(),
        pygame.image.load('солдат_снег_3.png').convert_alpha(),
        pygame.image.load('солдат_снег_4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 23
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(5 - play) + '/' + '5'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '23'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '20'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 5 and kol < 20:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 10
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
                playery += 10
            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 5:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level1()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        elif kol >= 20:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level1()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1
        clock.tick(10)

        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


def open_snow_level2():
    global result
    gunspeed = 30
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 1000)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон-снег.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат_снег_1.png').convert_alpha(),
        pygame.image.load('солдат_снег_2.png').convert_alpha(),
        pygame.image.load('солдат_снег_3.png').convert_alpha(),
        pygame.image.load('солдат_снег_4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 30
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(3 - play) + '/' + '3'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '30'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '25'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 5 and kol < 25:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 7
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
            playery += 10

            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 5:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level2()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        elif kol >= 25:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level2()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_main_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1
        clock.tick(10)

        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


def open_snow_level3():
    global result
    gunspeed = 30
    gunx = 200
    playery = -3

    counter = 0

    # проигрыш
    play = 0
    label = pygame.font.Font('Times.ttf', 40)
    lose_label = label.render('Вы проиграли!!!', False, 'red')
    label = pygame.font.Font('Times.ttf', 20)
    restart_label = label.render('переиграть', False, 'red')
    restart_label_rect = restart_label.get_rect(topleft=(70, 260))
    label = pygame.font.Font('Times.ttf', 20)
    back_label = label.render('назад', False, 'red')
    back_label_rect = back_label.get_rect(topleft=(300, 260))

    # выигрыш
    label = pygame.font.Font('Times.ttf', 40)
    win_label = label.render('Вы выиграли!!!', False, 'red')

    # установка времени
    clock = pygame.time.Clock()
    player_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_timer, 1500)

    # анимация
    bum = pygame.image.load('пуля.png').convert_alpha()
    bums = []
    bg = pygame.image.load('фон-снег.jpg').convert_alpha()
    gun = pygame.image.load('пушка1.png').convert_alpha()
    player = [
        pygame.image.load('солдат_снег_1.png').convert_alpha(),
        pygame.image.load('солдат_снег_2.png').convert_alpha(),
        pygame.image.load('солдат_снег_3.png').convert_alpha(),
        pygame.image.load('солдат_снег_4.png').convert_alpha(),
    ]
    player_list = []
    count_walking = 0
    running = True
    kol = 0
    kol_bums = 30
    while running:
        # вывод на экран
        wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
        WINDOW.blit(bg, (0, 0))
        WINDOW.blit(gun, (gunx, 470))

        # игровые характеристики
        label = pygame.font.Font('arial.otf', 10)
        text = 'lifes:' + str(3 - play) + '/' + '3'
        life_label = label.render(text, False, 'black')
        WINDOW.blit(life_label, (340, 10))
        text = 'bulles:' + str(kol_bums) + '/' + '30'
        bums_label = label.render(text, False, 'black')
        WINDOW.blit(bums_label, (323, 20))
        text = 'kills:' + str(kol) + '/' + '29'
        kills_label = label.render(text, False, 'black')
        WINDOW.blit(kills_label, (335, 30))

        if play < 3 and kol < 29:
            # автоматический вывод солдат
            if player_list:
                for (i, event) in enumerate(player_list):
                    WINDOW.blit(player[count_walking], event)
                    event.y += 7
                    if wall_rect.colliderect(event):
                        play += 1
                    if event.y > 400:
                        player_list.pop(i)
            playery += 10

            # вдижение пушки
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and gunx > 0:
                gunx -= gunspeed
            elif key[pygame.K_RIGHT] and gunx < 325:
                gunx += gunspeed

            # анимация солдата
            if count_walking == 3:
                count_walking = 0
            else:
                count_walking += 1

            # стрельбa
            if bums:
                for (i, event) in enumerate(bums):
                    WINDOW.blit(bum, (event.x + 21, event.y - 15))
                    event.y -= 10
                    if event.y < -40:
                        bums.pop(i)
                    if player_list:
                        for (ind, el) in enumerate(player_list):
                            if event.colliderect(el):
                                kol += 1
                                player_list.pop(ind)
                                bums.pop(i)

        elif play >= 3:
            result = False
            WINDOW.fill('grey')
            WINDOW.blit(lose_label, (70, 200))
            WINDOW.blit(restart_label, restart_label_rect)
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level3()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_level_selection()

        elif kol >= 29:
            result = True
            WINDOW.fill('grey')
            WINDOW.blit(win_label, (70, 200))
            WINDOW.blit(back_label, back_label_rect)

            # перезапуск
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_snow_level3()

            # заново
            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                open_level_selection()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_timer:
                player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
            if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                bums.append(bum.get_rect(topleft=(gunx, 460)))
                kol_bums -= 1
        clock.tick(10)

        counter += 1
        if counter <= 1:
            add_results_to_database()
            if result:
                add_money()


if __name__ == '__main__':
    open_main_menu()
