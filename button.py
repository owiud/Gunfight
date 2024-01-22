import pygame


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, image_path: str,
                 hover_image_path: str = None, sound_path: str = None):
        """
        :param x: координата х
        :param y: координата у
        :param width: ширина
        :param height: высота
        :param text: текст
        :param image_path: путь к файлу с изображением
        :param hover_image_path: изображение, появляющееся при наведении на кнопку
        :param sound_path: путь к файлу со звуком
        """
        self.x, self.y, self.width, self.height, self.text = x, y, width, height, text

        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.transform.scale(pygame.image.load(hover_image_path), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, window):
        """
        Устанавливает текст и изображение.
        :param window: окно
        """
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        window.blit(current_image, self.rect.topleft)

        text_surface = pygame.font.Font(None, 36).render(self.text, True, (255, 255, 255))
        window.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def check_hover(self, mouse_pos) -> None:
        """
        Проверяет наведение курсора на кнопку.
        :param mouse_pos: координаты курсора
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event) -> None:
        """
        Обрабатывает событие (нажатие на кнопку).
        :param event: событие (нажатие на кнопку)
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
