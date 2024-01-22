import random
import sys

import pygame.mixer

from menu import *
from workWithDataBases import WorkWithDataBases

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('src/music/background_music.mp3')
pygame.mixer.music.play(-1)
gun_sound = pygame.mixer.Sound("src/music/gun_sound.mp3")

COLOR = (255, 255, 255)
BACKGROUND = "src/images/main_menu_background.jpeg"

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('GunFight')


class GameLevels:
    def __init__(self, new_gun, load_main_levels, current_email=None):
        self.new_gun = new_gun
        self.load_extra_levels = load_main_levels
        self.current_email = current_email

    def open_grass_level1(self):
        gunspeed = 20
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 2000)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/grass_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        if self.new_gun:
            gun = pygame.image.load('src/images/gun2.png').convert_alpha()
        player = [
            pygame.image.load('src/images/soldier1.png').convert_alpha(),
            pygame.image.load('src/images/soldier2.png').convert_alpha(),
            pygame.image.load('src/images/soldier3.png').convert_alpha(),
            pygame.image.load('src/images/soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_grass_level1()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 20:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1

            clock.tick(10)

    def open_grass_level2(self):
        gunspeed = 30
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 1000)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/grass_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/soldier1.png').convert_alpha(),
            pygame.image.load('src/images/soldier2.png').convert_alpha(),
            pygame.image.load('src/images/soldier3.png').convert_alpha(),
            pygame.image.load('src/images/soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_grass_level2()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 25:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1
            clock.tick(10)

    def open_grass_level3(self):
        gunspeed = 30
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 1500)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/grass_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/soldier1.png').convert_alpha(),
            pygame.image.load('src/images/soldier2.png').convert_alpha(),
            pygame.image.load('src/images/soldier3.png').convert_alpha(),
            pygame.image.load('src/images/soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_grass_level3()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 29:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1
            clock.tick(10)

    def open_snow_level1(self):
        gunspeed = 20
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 2000)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/snow_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/snow_soldier1.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier2.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier3.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_snow_level1()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 20:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1
            clock.tick(10)

    def open_snow_level2(self):
        gunspeed = 30
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 1000)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/snow_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/snow_soldier1.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier2.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier3.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_snow_level2()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 25:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1
            clock.tick(10)

    def open_snow_level3(self):
        gunspeed = 30
        gunx = 200
        playery = -3

        counter = 0

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Вы проиграли!!!', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('переиграть', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(70, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(300, 260))

        # выигрыш
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        win_label = label.render('Вы выиграли!!!', False, 'red')

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 1500)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/snow_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/snow_soldier1.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier2.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier3.png').convert_alpha(),
            pygame.image.load('src/images/snow_soldier4.png').convert_alpha(),
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
            label = pygame.font.Font('src/fonts/arial.otf', 10)
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
                WINDOW.fill('grey')
                WINDOW.blit(lose_label, (70, 200))
                WINDOW.blit(restart_label, restart_label_rect)
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(False)

                # перезапуск
                mouse = pygame.mouse.get_pos()
                if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    self.open_snow_level3()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            elif kol >= 29:
                WINDOW.fill('grey')
                WINDOW.blit(win_label, (70, 200))
                WINDOW.blit(back_label, back_label_rect)

                counter += 1
                if counter <= 1:
                    if self.current_email:
                        WorkWithDataBases(self.current_email).add_results_to_database(True)

                mouse = pygame.mouse.get_pos()

                # заново
                if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    running = False

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == player_timer:
                    player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))
                if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                    gun_sound.play()
                    bums.append(bum.get_rect(topleft=(gunx, 460)))
                    kol_bums -= 1
            clock.tick(10)

    @staticmethod
    def open_multiplay_game():
        gunspeed = 20
        gunx = 200
        playery = -3

        # проигрыш
        play = 0
        label = pygame.font.Font('src/fonts/times.ttf', 40)
        lose_label = label.render('Игра окончена', False, 'red')
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        restart_label = label.render('следующий', False, 'red')
        restart_label_rect = restart_label.get_rect(topleft=(100, 260))
        label = pygame.font.Font('src/fonts/times.ttf', 20)
        back_label = label.render('назад', False, 'red')
        back_label_rect = back_label.get_rect(topleft=(270, 400))

        # установка времени
        clock = pygame.time.Clock()
        player_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(player_timer, 2000)

        # анимация
        bum = pygame.image.load('src/images/bullet.png').convert_alpha()
        bums = []
        bg = pygame.image.load('src/images/grass_background.jpg').convert_alpha()
        gun = pygame.image.load('src/images/gun1.png').convert_alpha()
        player = [
            pygame.image.load('src/images/soldier1.png').convert_alpha(),
            pygame.image.load('src/images/soldier2.png').convert_alpha(),
            pygame.image.load('src/images/soldier3.png').convert_alpha(),
            pygame.image.load('src/images/soldier4.png').convert_alpha(),
        ]
        player_list = []
        count_walking = 0
        running = True
        kol = 0
        kol_bums = 23
        qwerty = 0
        while running:
            for schet in range(2):
                # вывод на экран
                wall_rect = pygame.draw.rect(WINDOW, (133, 116, 105), (0, 500, 400, 100), 1)
                WINDOW.blit(bg, (0, 0))
                WINDOW.blit(gun, (gunx, 470))

                # игровые характеристики
                label = pygame.font.Font('src/fonts/arial.otf', 10)
                text = 'lifes:' + str(3 - play) + '/' + '3'
                life_label = label.render(text, False, 'black')
                WINDOW.blit(life_label, (340, 10))
                text = 'bulles:' + str(kol_bums) + '/' + '23'
                bums_label = label.render(text, False, 'black')
                WINDOW.blit(bums_label, (323, 20))
                text = 'kills:' + str(kol)
                kills_label = label.render(text, False, 'black')
                WINDOW.blit(kills_label, (335, 30))

                if play < 3:
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

                elif play >= 3:
                    if qwerty == 0:

                        WINDOW.fill('grey')
                        WINDOW.blit(lose_label, (70, 200))
                        WINDOW.blit(restart_label, restart_label_rect)

                        # следующий игрок
                        mouse = pygame.mouse.get_pos()
                        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                            play = 0
                            ochki1 = kol
                            kol = 0
                            kol_bums = 23
                            gunx = 200
                            qwerty = 2
                            player_list.clear()
                            bums.clear()
                            break
                    else:
                        WINDOW.fill('grey')
                        WINDOW.blit(lose_label, (70, 200))
                        if ochki1 > kol:
                            label = pygame.font.Font('src/fonts/times.ttf', 30)
                            text = 'победа за первым игроком'
                            life_label = label.render(text, False, 'black')
                            WINDOW.blit(life_label, (30, 300))
                            WINDOW.blit(back_label, back_label_rect)
                            mouse = pygame.mouse.get_pos()
                            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                                running = False

                        elif ochki1 < kol:
                            label = pygame.font.Font('src/fonts/times.ttf', 30)
                            text = 'победа за вторым игроком'
                            life_label = label.render(text, False, 'black')
                            WINDOW.blit(life_label, (30, 300))
                            WINDOW.blit(back_label, back_label_rect)
                            mouse = pygame.mouse.get_pos()
                            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                                running = False

                        else:
                            label = pygame.font.Font('src/fonts/times.ttf', 30)
                            text = 'ничья'
                            life_label = label.render(text, False, 'black')
                            WINDOW.blit(life_label, (80, 300))
                            WINDOW.blit(back_label, back_label_rect)
                            mouse = pygame.mouse.get_pos()
                            if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                                running = False

                pygame.display.update()

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                    if event.type == player_timer:
                        player_list.append(player[0].get_rect(topleft=(random.randint(10, 350), -70)))

                    if play < 5 and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and kol_bums > 0:
                        gun_sound.play()
                        bums.append(bum.get_rect(topleft=(gunx, 460)))
                        kol_bums -= 1
                clock.tick(10)


if __name__ == '__main__':
    AllMenus(BACKGROUND, COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW).open_main_menu()
