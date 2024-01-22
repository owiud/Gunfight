import sys

import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox

from button import Button
from main import GameLevels
from workWithDataBases import *


class AllMenus:
    def __init__(self, background, color, window_width, window_height, window) -> None:
        """
        :param self.new_gun: показатель выбранной пушки. True - выбранная пушка из магазина.
        :param self.load_main_levels: показатель локации уровня. True - фон - трава.
        :param self.current_email: показатель наличия входа в аккаунт, содержит текущий адрес электронной почты.
        """
        self.BACKGROUND = background
        self.COLOR = color
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.WINDOW = window
        self.new_gun = False
        self.load_main_levels = False
        self.current_email = ""

    def open_main_menu(self) -> None:
        """
        Загружает и обрабатывает основное меню.
        """
        main_menu_background = pygame.image.load(self.BACKGROUND)

        registration_button = Button(190, 20, 200, 20, "личный кабинет", "src/images/button.jpeg",
                                     "src/images/hovered_button.jpeg")
        main_levels_button = Button(74, 200, 252, 74, "УРОВНИ", "src/images/button.jpeg",
                                    "src/images/hovered_button.jpeg")
        extra_levels_button = Button(74, 300, 252, 74, "ЕЩЁ УРОВНИ", "src/images/button.jpeg",
                                     "src/images/hovered_button.jpeg")
        multiplayer_game_button = Button(74, 500, 252, 20, "игра на двоих", "src/images/button.jpeg",
                                         "src/images/hovered_button.jpeg")
        market_button = Button(74, 400, 252, 74, "МАГАЗИН", "src/images/button.jpeg", "src/images/hovered_button.jpeg")

        while True:
            self.WINDOW.fill(self.COLOR)
            self.WINDOW.blit(main_menu_background, (0, 0))

            self.set_text(("GUNFIGHT", 200, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == registration_button:
                    if self.current_email:
                        self.open_personal_account()
                    else:
                        self.open_registration()

                if event.type == pygame.USEREVENT and event.button == main_levels_button:
                    self.load_main_levels = True
                    self.open_level_selection()

                if event.type == pygame.USEREVENT and event.button == extra_levels_button:
                    self.load_main_levels = False
                    self.open_level_selection()

                if event.type == pygame.USEREVENT and event.button == multiplayer_game_button:
                    GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_multiplay_game()

                if event.type == pygame.USEREVENT and event.button == market_button:
                    self.open_market()

                for button in [registration_button, main_levels_button, extra_levels_button, market_button,
                               multiplayer_game_button]:
                    button.handle_event(event)

            for button in [registration_button, main_levels_button, extra_levels_button, market_button,
                           multiplayer_game_button]:
                button.check_hover(pygame.mouse.get_pos())
                button.draw(self.WINDOW)

            pygame.display.flip()

    def open_registration(self):
        """
        Загружает и обрабатывает поля для регистрации.
        """
        main_menu_background = pygame.image.load(self.BACKGROUND)

        back_button = Button(20, 20, 70, 20, "назад", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        login_button = Button(74, 400, 252, 74, "ВОЙТИ", "src/images/button.jpeg", "src/images/hovered_button.jpeg")

        email_input_box = TextBox(self.WINDOW, 50, 200, 300, 60, colour=(255, 255, 255), fontSize=30,
                                  borderColour=(212, 175, 158), textColour=(0, 0, 0), radius=10, borderThickness=5)
        password_input_box = TextBox(self.WINDOW, 50, 300, 300, 60, colour=(255, 255, 255), fontSize=30,
                                     borderColour=(212, 175, 158), textColour=(0, 0, 0), radius=10, borderThickness=5)

        while True:
            self.WINDOW.fill(self.COLOR)
            self.WINDOW.blit(main_menu_background, (0, 0))

            self.set_text(("РЕГИСТРАЦИЯ", 200, 100))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == login_button:
                    email = email_input_box.getText()
                    password = password_input_box.getText()

                    if WorkWithDataBases(email).account_existence():
                        if WorkWithDataBases(email).get_all_information_about_user()[0] == password:
                            self.current_email = email
                            self.open_personal_account()
                    else:
                        WorkWithDataBases(email, password).create_new_account()
                        self.current_email = email
                        self.open_personal_account()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.open_main_menu()

                for button in [back_button, login_button]:
                    button.handle_event(event)

            pygame_widgets.update(events)

            for button in [back_button, login_button]:
                button.check_hover(pygame.mouse.get_pos()), button.draw(self.WINDOW)

            pygame.display.flip()

    def open_personal_account(self):
        """
        Загружает и обрабатывает личный кабинет.
        """
        main_menu_background = pygame.image.load(self.BACKGROUND)

        back_button = Button(20, 20, 70, 20, "назад", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        results = WorkWithDataBases(self.current_email).get_all_information_about_user()[1].split()

        while True:
            self.WINDOW.fill(self.COLOR)
            self.WINDOW.blit(main_menu_background, (0, 0))

            self.set_text(("ЛИЧНЫЙ КАБИНЕТ", 200, 100))
            self.set_text((f"Победы: {results[0]}", 200, 300))
            self.set_text((f"Поражения: {results[1]}", 200, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.open_main_menu()

                back_button.handle_event(event)

            back_button.check_hover(pygame.mouse.get_pos()), back_button.draw(self.WINDOW)

            pygame.display.flip()

    def open_level_selection(self):
        """
        Загружает и обрабатывает меню с выбором уровня.
        """
        main_menu_background = pygame.image.load(self.BACKGROUND)

        back_button = Button(20, 20, 70, 20, "назад", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        level1_button = Button(74, 200, 252, 74, "УРОВЕНЬ1", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        level2_button = Button(74, 300, 252, 74, "УРОВЕНЬ2", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        level3_button = Button(74, 400, 252, 74, "УРОВЕНЬ3", "src/images/button.jpeg", "src/images/hovered_button.jpeg")

        while True:
            self.WINDOW.fill(self.COLOR)
            self.WINDOW.blit(main_menu_background, (0, 0))

            if self.load_main_levels:
                self.set_text(("ОСНОВНЫЕ УРОВНИ", 200, 100))
            else:
                self.set_text(("ЕЩЁ УРОВНИ", 200, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == level1_button:
                    if self.load_main_levels:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_grass_level1()
                    else:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_snow_level1()

                if event.type == pygame.USEREVENT and event.button == level2_button:
                    if self.load_main_levels:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_grass_level2()
                    else:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_snow_level2()

                if event.type == pygame.USEREVENT and event.button == level3_button:
                    if self.load_main_levels:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_grass_level3()
                    else:
                        GameLevels(self.new_gun, self.load_main_levels, self.current_email).open_snow_level3()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.open_main_menu()

                for button in [back_button, level1_button, level2_button, level3_button]:
                    button.handle_event(event)

            for button in [back_button, level1_button, level2_button, level3_button]:
                button.check_hover(pygame.mouse.get_pos())
                button.draw(self.WINDOW)

            pygame.display.flip()

    def open_market(self):
        """
        Загружает и обрабатывает магазин.
        """
        main_menu_background = pygame.image.load(self.BACKGROUND)

        back_button = Button(20, 20, 70, 20, "назад", "src/images/button.jpeg", "src/images/hovered_button.jpeg")
        gun_button = Button(20, 200, 150, 200, "10", "src/images/market_gun.png", "src/images/market_gun.png")

        while True:
            self.WINDOW.fill(self.COLOR)
            self.WINDOW.blit(main_menu_background, (0, 0))

            if self.current_email:
                self.set_text(
                    (str(WorkWithDataBases(self.current_email).get_all_information_about_user()[2]), 300, 50))

            self.set_text(("МАГАЗИН", 200, 100))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == back_button:
                    self.open_main_menu()

                if event.type == pygame.USEREVENT and event.button == gun_button:
                    if self.current_email:
                        if WorkWithDataBases(self.current_email).get_all_information_about_user()[2] >= 10:
                            if WorkWithDataBases(self.current_email).get_all_information_about_user()[3] == 0:
                                WorkWithDataBases(self.current_email).cash_out()
                            if self.new_gun:
                                self.new_gun = False
                            else:
                                self.new_gun = True

                for button in [back_button, gun_button]:
                    button.handle_event(event)

            for button in [back_button, gun_button]:
                button.check_hover(pygame.mouse.get_pos()), button.draw(self.WINDOW)

            pygame.display.flip()

    def set_text(self, *texts_and_coordinates: tuple) -> None:
        """
        Вывод текста.
        :param texts_and_coordinates: (текст, ширина (х), высота (у))
        """
        for (text, coordinate1, coordinate2) in texts_and_coordinates:
            text_surface = pygame.font.Font(None, 50).render(text, True, self.COLOR)
            self.WINDOW.blit(text_surface, text_surface.get_rect(center=(coordinate1, coordinate2)))
