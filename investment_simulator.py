import pygame
import sys
import random
import math
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
MAX_TRADES_PER_DAY = 10
TOTAL_WEEKS = 12
INITIAL_BALANCE = 10000.0
MESSAGE_DISPLAY_TIME = 3000  # 3 seconds

# Размеры UI элементов
CARD_WIDTH = 500
CARD_HEIGHT = 140
CARD_SPACING = 150
BUTTON_WIDTH_SMALL = 180
BUTTON_WIDTH_MEDIUM = 280
BUTTON_WIDTH_LARGE = 200
BUTTON_HEIGHT = 40
INPUT_FIELD_WIDTH = 100
INPUT_FIELD_HEIGHT = 30
LOGO_SIZE = (40, 40)
CARD_RADIUS = 12
BUTTON_RADIUS = 8

# Создание папки для логотипов
LOGOS_DIR = "logos"
if not os.path.exists(LOGOS_DIR):
    try:
        os.makedirs(LOGOS_DIR)
        print(f"Создана папка для логотипов: {LOGOS_DIR}")
        print("Пожалуйста, добавьте в неё логотипы с именами: sber.png, vtb.png, tinkoff.png")
        print(f"Рекомендуемый размер логотипов: {LOGO_SIZE[0]}x{LOGO_SIZE[1]} пикселей")
    except OSError as e:
        print(f"Ошибка при создании папки {LOGOS_DIR}: {e}")
        sys.exit(1)

# Цветовая палитра
VTB_DARK_BLUE = (13, 37, 72)
VTB_BLUE = (25, 68, 142)
VTB_LIGHT_BLUE = (232, 240, 254)
VTB_WHITE = (255, 255, 255)
VTB_GREEN = (0, 168, 107)
VTB_RED = (227, 58, 61)
VTB_GRAY = (245, 247, 250)
VTB_DARK_GRAY = (102, 112, 133)
VTB_BORDER_GRAY = (226, 230, 238)
VTB_ACCENT_BLUE = (56, 119, 237)
VTB_YELLOW = (255, 184, 0)
VTB_PURPLE = (121, 97, 225)

# Новый цвет основного фона
BACKGROUND_COLOR = (231, 234, 239)

# Цвет для кнопок
BUTTON_COLOR = (85, 106, 159)
BUTTON_HOVER_COLOR = (100, 125, 180)

# Более яркие цвета для шапки
VTB_BRIGHT_BLUE = (0, 91, 187)
VTB_LIGHT_ACCENT = (74, 144, 255)

# Создание экрана
try:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ВТБ Инвестиционный Симулятор")
except pygame.error as e:
    print(f"Ошибка инициализации дисплея: {e}")
    sys.exit(1)

clock = pygame.time.Clock()


def initialize_fonts() -> Tuple[Any, ...]:
    """
    Инициализирует шрифты для приложения.

    Returns:
        Кортеж с шрифтами: (title_font, header_font, normal_font,
                           small_font, large_font, bold_font)
    """
    try:
        title_font = pygame.font.Font(None, 36)
        header_font = pygame.font.Font(None, 24)
        normal_font = pygame.font.Font(None, 18)
        small_font = pygame.font.Font(None, 16)
        large_font = pygame.font.Font(None, 32)
        bold_font = pygame.font.Font(None, 20)
        bold_font.set_bold(True)
        return title_font, header_font, normal_font, small_font, large_font, bold_font
    except:
        # Fallback to system fonts
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        header_font = pygame.font.SysFont('Arial', 24, bold=True)
        normal_font = pygame.font.SysFont('Arial', 18)
        small_font = pygame.font.SysFont('Arial', 16)
        large_font = pygame.font.SysFont('Arial', 32, bold=True)
        bold_font = pygame.font.SysFont('Arial', 20, bold=True)
        return title_font, header_font, normal_font, small_font, large_font, bold_font


# Инициализация шрифтов
title_font, header_font, normal_font, small_font, large_font, bold_font = initialize_fonts()


def load_logo(filename: str, default_size: Tuple[int, int] = LOGO_SIZE) -> pygame.Surface:
    """
    Загружает логотип из файла или создает заглушку.

    Args:
        filename: Имя файла логотипа
        default_size: Размер логотипа (ширина, высота)

    Returns:
        Surface с логотипом
    """
    try:
        logo_path = os.path.join(LOGOS_DIR, filename)
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Файл {logo_path} не найден")

        logo = pygame.image.load(logo_path)
        logo = pygame.transform.smoothscale(logo, default_size)
        return logo
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"Ошибка загрузки логотипа {filename}: {e}")
        return create_dummy_logo(default_size)


def create_dummy_logo(size: Tuple[int, int]) -> pygame.Surface:
    """
    Создает заглушку для отсутствующего логотипа.

    Args:
        size: Размер логотипа (ширина, высота)

    Returns:
        Surface с заглушкой логотипа
    """
    dummy_logo = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(
        dummy_logo, VTB_DARK_GRAY,
        (0, 0, size[0], size[1]),
        border_radius=8
    )
    text = small_font.render("LOGO", True, VTB_WHITE)
    text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
    dummy_logo.blit(text, text_rect)
    return dummy_logo


def load_all_logos() -> Dict[str, pygame.Surface]:
    """
    Загружает все логотипы для приложения.

    Returns:
        Словарь с логотипами
    """
    logos = {}
    logo_mappings = {
        'SBER': 'sber.png',
        'VTBR': 'vtb.png',
        'TCSG': 'tinkoff.png',
        'VTB-B1379': 'vtb.png',
        'SBER-SB29R': 'sber.png',
        'TCSG-2R': 'tinkoff.png',
        'VTB-DEP': 'vtb.png',
        'SBER-DEP': 'sber.png',
        'TCSG-DEP': 'tinkoff.png'
    }

    for key, filename in logo_mappings.items():
        logos[key] = load_logo(filename)

    return logos


# Загружаем логотипы
try:
    LOGOS = load_all_logos()
except Exception as e:
    print(f"Критическая ошибка при загрузке логотипов: {e}")
    sys.exit(1)

# Данные активов
ASSETS = {
    'акции': [
        {
            'name': 'Сбербанк', 'ticker': 'SBER', 'price': 297.17,
            'base_price': 297.17, 'change': 0.0, 'dividend': 6.8,
            'risk': 'Низкий', 'volatility': 0.03, 'color': VTB_GREEN,
            'logo': 'SBER'
        },
        {
            'name': 'ВТБ', 'ticker': 'VTBR', 'price': 69.96,
            'base_price': 69.96, 'change': 0.0, 'dividend': 7.5,
            'risk': 'Средний', 'volatility': 0.05, 'color': VTB_BLUE,
            'logo': 'VTBR'
        },
        {
            'name': 'Тинькофф', 'ticker': 'TCSG', 'price': 2920.20,
            'base_price': 2920.20, 'change': 0.0, 'dividend': 5.2,
            'risk': 'Высокий', 'volatility': 0.07, 'color': VTB_PURPLE,
            'logo': 'TCSG'
        }
    ],
    'облигации': [
        {
            'name': 'Сбер Sb29R', 'ticker': 'SBER-SB29R',
            'price': 964.50, 'base_price': 964.50, 'change': 0.0,
            'yield': 13.26, 'risk': 'Низкий', 'volatility': 0.01,
            'color': VTB_GREEN, 'logo': 'SBER-SB29R'
        },
        {
            'name': 'ВТБ Б1-379', 'ticker': 'VTB-B1379',
            'price': 1001.10, 'base_price': 1001.10, 'change': 0.0,
            'yield': 14.25, 'risk': 'Низкий', 'volatility': 0.01,
            'color': VTB_BLUE, 'logo': 'VTB-B1379'
        },
        {
            'name': 'Тинькофф 2R', 'ticker': 'TCSG-2R',
            'price': 997.90, 'base_price': 997.90, 'change': 0.0,
            'yield': 12.85, 'risk': 'Средний', 'volatility': 0.015,
            'color': VTB_PURPLE, 'logo': 'TCSG-2R'
        }
    ],
    'вклады': [
        {
            'name': 'Сбербанк «Ключевой»', 'ticker': 'SBER-DEP',
            'price': 1.0, 'base_price': 1.0, 'change': 0.0,
            'yield': 18.0, 'risk': 'Низкий', 'volatility': 0.0,
            'color': VTB_GREEN, 'logo': 'SBER-DEP'
        },
        {
            'name': 'ВТБ «Двойная выгода»', 'ticker': 'VTB-DEP',
            'price': 1.0, 'base_price': 1.0, 'change': 0.0,
            'yield': 26.0, 'risk': 'Низкий', 'volatility': 0.0,
            'color': VTB_BLUE, 'logo': 'VTB-DEP'
        },
        {
            'name': 'Тинькофф «СмартВклад»', 'ticker': 'TCSG-DEP',
            'price': 1.0, 'base_price': 1.0, 'change': 0.0,
            'yield': 15.0, 'risk': 'Низкий', 'volatility': 0.0,
            'color': VTB_PURPLE, 'logo': 'TCSG-DEP'
        }
    ]
}


class Button:
    """Класс для создания кнопок интерфейса."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            color: Tuple[int, int, int] = BUTTON_COLOR,
            hover_color: Tuple[int, int, int] = BUTTON_HOVER_COLOR,
            text_color: Tuple[int, int, int] = VTB_WHITE,
            font: Any = normal_font,
            corner_radius: int = BUTTON_RADIUS
    ):
        """
        Инициализация кнопки.

        Args:
            x: Координата X
            y: Координата Y
            width: Ширина кнопки
            height: Высота кнопки
            text: Текст кнопки
            color: Цвет кнопки
            hover_color: Цвет при наведении
            text_color: Цвет текста
            font: Шрифт текста
            corner_radius: Радиус скругления углов
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.is_hovered = False
        self.enabled = True
        self.corner_radius = corner_radius

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает кнопку на поверхности."""
        if not self.enabled:
            color = VTB_DARK_GRAY
        else:
            color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(
            surface, color, self.rect, border_radius=self.corner_radius
        )
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos: Tuple[int, int]) -> None:
        """Проверяет, находится ли курсор над кнопкой."""
        self.is_hovered = self.rect.collidepoint(pos) and self.enabled

    def is_clicked(self, pos: Tuple[int, int], event: pygame.event.Event) -> bool:
        """
        Проверяет, была ли кнопка нажата.

        Returns:
            True если кнопка была нажата, иначе False
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos) and self.enabled
        return False


class InputField:
    """Класс для создания поля ввода."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            default_text: str = "10",
            font: Any = normal_font,
            text_color: Tuple[int, int, int] = VTB_DARK_BLUE,
            bg_color: Tuple[int, int, int] = VTB_WHITE,
            border_color: Tuple[int, int, int] = VTB_BORDER_GRAY,
            active_border_color: Tuple[int, int, int] = VTB_ACCENT_BLUE,
            corner_radius: int = 6
    ):
        """
        Инициализация поля ввода.

        Args:
            x: Координата X
            y: Координата Y
            width: Ширина поля
            height: Высота поля
            default_text: Текст по умолчанию
            font: Шрифт текста
            text_color: Цвет текста
            bg_color: Цвет фона
            border_color: Цвет границы
            active_border_color: Цвет активной границы
            corner_radius: Радиус скругления углов
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = default_text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.corner_radius = corner_radius
        self.active = False
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает поле ввода на поверхности."""
        pygame.draw.rect(
            surface, self.bg_color, self.rect, border_radius=self.corner_radius
        )

        border_color = self.active_border_color if self.active else (
            self.border_color if not self.is_hovered else VTB_ACCENT_BLUE
        )

        pygame.draw.rect(
            surface, border_color, self.rect, 2, border_radius=self.corner_radius
        )

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos: Tuple[int, int]) -> None:
        """Проверяет, находится ли курсор над полем ввода."""
        self.is_hovered = self.rect.collidepoint(pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Обрабатывает события ввода.

        Returns:
            True если событие было обработано, иначе False
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            return self.active

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif event.unicode.isdigit():
                self.text += event.unicode
            return True
        return False


class TabButton:
    """Класс для создания вкладок."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            is_active: bool = False
    ):
        """
        Инициализация вкладки.

        Args:
            x: Координата X
            y: Координата Y
            width: Ширина вкладки
            height: Высота вкладки
            text: Текст вкладки
            is_active: Активна ли вкладка
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_active = is_active
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает вкладку на поверхности."""
        if self.is_active:
            color = BUTTON_COLOR
            text_color = VTB_WHITE
        else:
            color = VTB_WHITE
            text_color = VTB_DARK_BLUE

        if self.is_hovered and not self.is_active:
            color = VTB_LIGHT_BLUE

        pygame.draw.rect(surface, color, self.rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(
            surface, VTB_BORDER_GRAY, self.rect, 1, border_radius=BUTTON_RADIUS
        )

        text_surf = small_font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos: Tuple[int, int]) -> None:
        """Проверяет, находится ли курсор над вкладкой."""
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(
            self,
            pos: Tuple[int, int],
            event: pygame.event.Event
    ) -> bool:
        """
        Проверяет, была ли вкладка нажата.

        Returns:
            True если вкладка была нажата, иначе False
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class AssetCard:
    """Базовый класс для карточек активов."""

    def __init__(
            self,
            asset: Dict[str, Any],
            x: int,
            y: int,
            width: int,
            height: int
    ):
        """
        Инициализация карточки актива.

        Args:
            asset: Данные актива
            x: Координата X
            y: Координата Y
            width: Ширина карточки
            height: Высота карточки
        """
        self.asset = asset
        self.rect = pygame.Rect(x, y, width, height)
        self.is_selected = False

    def draw(self, surface: pygame.Surface, portfolio_qty: int = 0) -> None:
        """Отрисовывает карточку актива."""
        self._draw_card_background(surface)
        self._draw_card_header(surface)
        self._draw_card_content(surface, portfolio_qty)

        if self.is_selected:
            self._draw_selection_border(surface)

    def _draw_card_background(self, surface: pygame.Surface) -> None:
        """Отрисовывает фон карточки."""
        pygame.draw.rect(
            surface, VTB_WHITE, self.rect, border_radius=CARD_RADIUS
        )
        pygame.draw.rect(
            surface, VTB_BORDER_GRAY, self.rect, 1, border_radius=CARD_RADIUS
        )

    def _draw_card_header(self, surface: pygame.Surface) -> None:
        """Отрисовывает заголовок карточки."""
        header_rect = pygame.Rect(
            self.rect.x, self.rect.y, self.rect.width, 70
        )
        pygame.draw.rect(
            surface, VTB_LIGHT_BLUE, header_rect, border_radius=CARD_RADIUS
        )
        pygame.draw.rect(
            surface, VTB_BORDER_GRAY, header_rect, 1, border_radius=CARD_RADIUS
        )

        self._draw_logo_and_text(surface)

    def _draw_logo_and_text(self, surface: pygame.Surface) -> None:
        """Отрисовывает логотип и текст в заголовке."""
        logo_key = self.asset.get('logo', self.asset['ticker'])
        if logo_key in LOGOS:
            logo = LOGOS[logo_key]
            logo_rect = logo.get_rect(
                midleft=(self.rect.x + 15, self.rect.y + 35)
            )
            surface.blit(logo, logo_rect)
            text_x = self.rect.x + 70
        else:
            text_x = self.rect.x + 20

        draw_text(
            surface, self.asset['name'], bold_font, VTB_DARK_BLUE,
            text_x, self.rect.y + 20
        )

        asset_type = self._get_asset_type()
        type_text = f"{self.asset['ticker']} • {asset_type}"
        draw_text(
            surface, type_text, small_font, VTB_DARK_GRAY,
            text_x, self.rect.y + 42
        )

        self._draw_price(surface)

    def _get_asset_type(self) -> str:
        """Определяет тип актива."""
        if 'dividend' in self.asset:
            return 'АКЦИЯ'
        elif 'yield' in self.asset:
            if 'DEP' in self.asset['ticker']:
                return 'ВКЛАД'
            else:
                return 'ОБЛИГАЦИЯ'
        else:
            return 'АКТИВ'

    def _draw_price(self, surface: pygame.Surface) -> None:
        """Отрисовывает цену актива."""
        price = self.asset['price']
        price_text = f"{price:.0f} Р" if price >= 1 else f"{price:.2f} Р"
        draw_text(
            surface, price_text, header_font, VTB_DARK_BLUE,
            self.rect.x + self.rect.width - 100, self.rect.y + 30
        )

    def _draw_card_content(
            self,
            surface: pygame.Surface,
            portfolio_qty: int
    ) -> None:
        """Отрисовывает содержимое карточки."""
        line_y = self.rect.y + 70
        pygame.draw.line(
            surface, VTB_BORDER_GRAY,
            (self.rect.x + 15, line_y),
            (self.rect.x + self.rect.width - 15, line_y), 1
        )

        self._draw_yield_and_risk(surface, line_y)

        if portfolio_qty > 0:
            self._draw_portfolio_info(surface, line_y, portfolio_qty)

    def _draw_yield_and_risk(
            self,
            surface: pygame.Surface,
            line_y: int
    ) -> None:
        """Отрисовывает доходность и риск."""
        y_pos = line_y + 20
        text_x = self.rect.x + 70

        yield_text = self._get_yield_text()
        draw_text(
            surface, yield_text, normal_font, VTB_DARK_GRAY,
            text_x, y_pos
        )

        risk_color = self._get_risk_color()
        risk_text = self._get_risk_text()
        draw_text(
            surface, f"Риск: {risk_text}", normal_font, risk_color,
            text_x, y_pos + 25
        )

    def _get_yield_text(self) -> str:
        """Возвращает текст доходности."""
        if 'dividend' in self.asset:
            return f"Доходность: {self.asset['dividend']}%"
        elif 'yield' in self.asset:
            return f"Доходность: {self.asset['yield']}%"
        else:
            return f"Ставка: {self.asset['yield']}%"

    def _get_risk_color(self) -> Tuple[int, int, int]:
        """Возвращает цвет риска."""
        risk = self.asset['risk']
        if risk == 'Низкий':
            return VTB_GREEN
        elif risk == 'Средний':
            return VTB_GREEN
        else:
            return VTB_GREEN

    def _get_risk_text(self) -> str:
        """Возвращает текст риска."""
        risk = self.asset['risk']
        if risk == 'Низкий':
            return 'Низкий'
        elif risk == 'Низкий':
            return 'Низкий'
        else:
            return 'Низкий'

    def _draw_portfolio_info(
            self,
            surface: pygame.Surface,
            line_y: int,
            portfolio_qty: int
    ) -> None:
        """Отрисовывает информацию о количестве в портфеле."""
        # Исправление: текст не выходит за границы карточки
        portfolio_text = f"В портфеле: {portfolio_qty} шт."
        text_width = small_font.size(portfolio_text)[0]

        # Проверяем, помещается ли текст
        max_width = self.rect.width - 120  # Оставляем отступы
        if text_width > max_width:
            # Если текст слишком длинный, сокращаем его
            portfolio_text = f"В портф.: {portfolio_qty} шт."

        draw_text(
            surface, portfolio_text, small_font, VTB_GREEN,
            self.rect.x + self.rect.width - 100, line_y + 30
        )

    def _draw_selection_border(self, surface: pygame.Surface) -> None:
        """Отрисовывает границу выделения."""
        pygame.draw.rect(
            surface, VTB_ACCENT_BLUE, self.rect, 2, border_radius=CARD_RADIUS
        )

    def check_click(self, pos: Tuple[int, int]) -> bool:
        """
        Проверяет, была ли карточка нажата.

        Returns:
            True если карточка была нажата, иначе False
        """
        return self.rect.collidepoint(pos)


class VTBAssetCard(AssetCard):
    """Класс для карточек активов ВТБ с особым оформлением."""

    def draw(
            self,
            surface: pygame.Surface,
            portfolio_qty: int = 0
    ) -> None:
        """Отрисовывает карточку актива ВТБ с особым оформлением."""
        if 'VTB' in self.asset['ticker']:
            self._draw_vtb_highlight(surface)

        super().draw(surface, portfolio_qty)

    def _draw_vtb_highlight(self, surface: pygame.Surface) -> None:
        """Отрисовывает выделение для активов ВТБ."""
        highlight_rect = pygame.Rect(
            self.rect.x, self.rect.y, self.rect.width, 5
        )
        pygame.draw.rect(
            surface, VTB_LIGHT_ACCENT, highlight_rect, border_radius=CARD_RADIUS
        )
        pygame.draw.rect(
            surface, VTB_ACCENT_BLUE, self.rect, 3, border_radius=CARD_RADIUS
        )

        badge_rect = pygame.Rect(
            self.rect.x + self.rect.width - 80, self.rect.y + 10, 70, 20
        )
        pygame.draw.rect(
            surface, VTB_GREEN, badge_rect, border_radius=10
        )
        draw_text(
            surface, "ВЫГОДА", small_font, VTB_WHITE,
            badge_rect.centerx, badge_rect.centery, centered=True
        )


def format_currency(value: float) -> str:
    """
    Форматирует валюту без лишних нулей.

    Args:
        value: Значение для форматирования

    Returns:
        Отформатированная строка с валютой
    """
    if value == 0:
        return "0 Р"
    elif value < 1:
        return f"{value:.2f} Р"
    elif value < 1000:
        return f"{value:.0f} Р"
    else:
        return f"{value:,.0f} Р".replace(',', ' ')


def draw_text(
        surface: pygame.Surface,
        text: str,
        font: Any,
        color: Tuple[int, int, int],
        x: int,
        y: int,
        centered: bool = False
) -> pygame.Rect:
    """
    Рисует текст на поверхности.

    Args:
        surface: Поверхность для отрисовки
        text: Текст для отрисовки
        font: Шрифт текста
        color: Цвет текста
        x: Координата X
        y: Координата Y
        centered: Центрировать ли текст

    Returns:
        Rect отрисованного текста
    """
    try:
        text_surface = font.render(str(text), True, color)
    except UnicodeEncodeError:
        text_surface = font.render(
            str(text).encode('utf-8', 'ignore').decode('utf-8'), True, color
        )

    if centered:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))

    surface.blit(text_surface, text_rect)
    return text_rect


def draw_card(
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = VTB_WHITE
) -> pygame.Rect:
    """
    Рисует карточку с закругленными углами.

    Args:
        surface: Поверхность для отрисовки
        x: Координата X
        y: Координата Y
        width: Ширина карточки
        height: Высота карточки
        color: Цвет карточки

    Returns:
        Rect отрисованной карточки
    """
    card_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, card_rect, border_radius=CARD_RADIUS)
    pygame.draw.rect(
        surface, VTB_BORDER_GRAY, card_rect, 1, border_radius=CARD_RADIUS
    )
    return card_rect


def draw_vtb_header(
        surface: pygame.Surface,
        week_text: Optional[str] = None
) -> None:
    """
    Рисует заголовок ВТБ с градиентом.

    Args:
        surface: Поверхность для отрисовки
        week_text: Текст недели для отображения
    """
    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
    specified_color = (12, 44, 118)
    light_end = (40, 80, 160)

    for i in range(header_rect.height):
        ratio = i / header_rect.height
        r = int(specified_color[0] * (1 - ratio) + light_end[0] * ratio)
        g = int(specified_color[1] * (1 - ratio) + light_end[1] * ratio)
        b = int(specified_color[2] * (1 - ratio) + light_end[2] * ratio)
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, i), (SCREEN_WIDTH, i))

    draw_text(surface, "ВТБ", title_font, VTB_WHITE, 40, 35)
    draw_text(
        surface, "ИНВЕСТИЦИОННЫЙ СИМУЛЯТОР", header_font, VTB_WHITE, 120, 35
    )

    marketing_text = " ВТБ - лидер по доходности! "
    draw_text(surface, marketing_text, small_font, VTB_WHITE, 120, 60)

    if week_text:
        draw_text(
            surface, week_text, small_font, VTB_WHITE, SCREEN_WIDTH - 120, 60
        )

    current_date = datetime.now().strftime("%d.%m.%Y")
    draw_text(
        surface, current_date, small_font, VTB_WHITE, SCREEN_WIDTH - 120, 40
    )


def draw_pie_chart(
        surface: pygame.Surface,
        x: int,
        y: int,
        radius: int,
        distribution: Dict[str, float],
        total_value: float
) -> None:
    """
    Рисует круговую диаграмму распределения портфеля.

    Args:
        surface: Поверхность для отрисовки
        x: Координата X центра
        y: Координата Y центра
        radius: Радиус диаграммы
        distribution: Распределение активов
        total_value: Общая стоимость портфеля
    """
    if total_value == 0:
        return

    start_angle = -90
    colors = [VTB_BLUE, VTB_GREEN, VTB_PURPLE, VTB_YELLOW, VTB_RED, VTB_ACCENT_BLUE]

    for i, (ticker, value) in enumerate(distribution.items()):
        angle = (value / total_value) * 360
        color = colors[i % len(colors)]

        points = [(x, y)]
        for angle_val in range(int(start_angle), int(start_angle + angle) + 1, 2):
            rad = math.radians(angle_val)
            px = x + radius * math.cos(rad)
            py = y + radius * math.sin(rad)
            points.append((px, py))

        if len(points) > 2:
            pygame.draw.polygon(surface, color, points)

        start_angle += angle

    pygame.draw.circle(surface, VTB_DARK_BLUE, (x, y), radius, 2)


# Рыночные события - расширенный список
MARKET_EVENTS = [
    {
        'name': 'Рост нефтяных цен',
        'description': 'Цены на нефть выросли на мировых рынках',
        'effects': {'VTBR': 0.08, 'SBER': 0.02},
        'volatility_effect': 0.05
    },
    {
        'name': 'Снижение ключевой ставки',
        'description': 'Центральный банк снизил ключевую ставку',
        'effects': {'облигации': 0.03, 'вклады': -0.02},
        'volatility_effect': -0.02
    },
    {
        'name': 'Волатильность на рынке',
        'description': 'Повышенная волатильность на финансовых рынках',
        'effects': {'акции': 0.05},
        'volatility_effect': 0.1
    },
    {
        'name': 'Стабильность в экономике',
        'description': 'Экономическая стабильность положительно влияет на рынок',
        'effects': {'облигации': 0.02, 'акции': 0.03},
        'volatility_effect': -0.05
    },
    {
        'name': 'Рост инфляции',
        'description': 'Уровень инфляции превысил ожидания',
        'effects': {'облигации': -0.03, 'акции': -0.02},
        'volatility_effect': 0.04
    },
    {
        'name': 'Укрепление рубля',
        'description': 'Рубль укрепился по отношению к мировым валютам',
        'effects': {'VTBR': -0.04, 'SBER': 0.01},
        'volatility_effect': -0.03
    },
    {
        'name': 'Новые санкции',
        'description': 'Введены новые экономические санкции',
        'effects': {'акции': -0.06, 'облигации': -0.02},
        'volatility_effect': 0.08
    },
    {
        'name': 'Позитивные корпоративные новости',
        'description': 'Крупные компании сообщили о росте прибыли',
        'effects': {'акции': 0.04},
        'volatility_effect': 0.02
    }
]


class GameState:
    """Класс для управления состоянием игры."""

    def __init__(self):
        """Инициализация состояния игры."""
        self.current_week = 1
        self.total_weeks = TOTAL_WEEKS
        self.initial_balance = INITIAL_BALANCE
        self.player = {
            'balance': INITIAL_BALANCE,
            'portfolio': {},
            'total_value': INITIAL_BALANCE,
            'total_profit': 0.0,
            'trades_today': 0,
            'max_trades_per_day': MAX_TRADES_PER_DAY,
            'history': [INITIAL_BALANCE] * TOTAL_WEEKS,
            'dividends_earned': 0.0,
            'interest_earned': 0.0
        }
        self.current_event = None
        self.selected_asset_ticker = None
        self.selected_asset_type = 'акции'
        self.operation_type = 'buy'
        self.quantity_input = "10"
        self.game_finished = False
        self.message = ""
        self.message_timer = 0
        self.message_type = ""
        self.market_news = []
        self.used_events = []  # Список использованных событий для исключения повторений
        self.market_volatility = 1.0  # Множитель волатильности рынка

    def reset_game(self) -> None:
        """Сбрасывает игру в начальное состояние."""
        self.__init__()
        for asset_type in ASSETS.values():
            for asset in asset_type:
                asset['price'] = asset['base_price']
                asset['change'] = 0.0

    def next_week(self) -> bool:
        """
        Переход к следующей неделе.

        Returns:
            True если игра продолжается, False если игра завершена
        """
        if self.current_week < self.total_weeks:
            self.current_week += 1
            self.player['trades_today'] = 0
            self.market_news = []

            if random.random() < 0.6:
                self.apply_market_event()

            self.update_prices()
            self.apply_dividends_and_interest()
            self.update_portfolio_value()

            if self.current_week <= self.total_weeks:
                self.player['history'][self.current_week - 1] = (
                    self.player['total_value']
                )

            return True
        else:
            self.game_finished = True
            return False

    def apply_market_event(self) -> None:
        """Применяет случайное рыночное событие."""
        # Исключаем повторяющиеся события
        available_events = [
            e for e in MARKET_EVENTS if e not in self.used_events
        ]

        # Если все события уже использовались, сбрасываем список
        if not available_events:
            available_events = MARKET_EVENTS.copy()
            self.used_events = []

        event = random.choice(available_events)
        self.current_event = event
        self.used_events.append(event)

        # Добавляем новость о событии
        self.market_news.append(
            f"📈 {event['name']}: {event['description']}"
        )

        # Применяем эффект волатильности
        self.market_volatility *= (1 + event.get('volatility_effect', 0))
        # Ограничиваем волатильность
        self.market_volatility = max(0.5, min(2.0, self.market_volatility))

        # Применяем эффекты к активам
        for effect_key, effect_value in event['effects'].items():
            if effect_key in ['акции', 'облигации', 'вклады']:
                for asset in ASSETS[effect_key]:
                    self._apply_price_effect(asset, effect_value)
            else:
                self._apply_ticker_effect(effect_key, effect_value)

    def _apply_price_effect(
            self,
            asset: Dict[str, Any],
            effect_value: float
    ) -> None:
        """Применяет эффект цены к активу."""
        old_price = asset['price']
        asset['price'] = max(0.01, asset['price'] * (1 + effect_value))
        asset['change'] = ((asset['price'] - old_price) / old_price) * 100

    def _apply_ticker_effect(
            self,
            ticker: str,
            effect_value: float
    ) -> None:
        """Применяет эффект к активу по тикеру."""
        for asset_type in ASSETS.values():
            for asset in asset_type:
                if asset['ticker'] == ticker:
                    self._apply_price_effect(asset, effect_value)
                    break

    def update_prices(self) -> None:
        """Обновляет цены активов с учетом волатильности."""
        for asset_type in ASSETS.values():
            for asset in asset_type:
                if asset['volatility'] > 0:
                    self._update_asset_price(asset)

    def _update_asset_price(self, asset: Dict[str, Any]) -> None:
        """Обновляет цену конкретного актива."""
        # Учитываем текущую волатильность рынка
        adjusted_volatility = asset['volatility'] * self.market_volatility
        change = random.uniform(-adjusted_volatility, adjusted_volatility)
        old_price = asset['price']
        asset['price'] = max(0.01, asset['price'] * (1 + change))
        asset['change'] = ((asset['price'] - old_price) / old_price) * 100

        if abs(change) > adjusted_volatility * 0.8:
            direction = "рост" if change > 0 else "падение"
            news_text = (
                f"📊 {asset['name']}: {direction} на {abs(change * 100):.1f}%"
            )
            if news_text not in self.market_news:
                self.market_news.append(news_text)

    def apply_dividends_and_interest(self) -> None:
        """Начисляет дивиденды и проценты по активам."""
        self._apply_dividends()
        self._apply_bond_interest()
        self._apply_deposit_interest()

    def _apply_dividends(self) -> None:
        """Начисляет дивиденды по акциям."""
        for asset in ASSETS['акции']:
            ticker = asset['ticker']
            if (ticker in self.player['portfolio'] and
                    self.player['portfolio'][ticker] > 0):
                dividend_amount = (
                        asset['price'] * self.player['portfolio'][ticker] *
                        asset['dividend'] / 100 / 52
                )
                self.player['balance'] += dividend_amount
                self.player['dividends_earned'] += dividend_amount

    def _apply_bond_interest(self) -> None:
        """Начисляет купоны по облигациям."""
        for asset in ASSETS['облигации']:
            ticker = asset['ticker']
            if (ticker in self.player['portfolio'] and
                    self.player['portfolio'][ticker] > 0):
                interest_amount = (
                        asset['price'] * self.player['portfolio'][ticker] *
                        asset['yield'] / 100 / 52
                )
                self.player['balance'] += interest_amount
                self.player['interest_earned'] += interest_amount

    def _apply_deposit_interest(self) -> None:
        """Начисляет проценты по вкладам."""
        for asset in ASSETS['вклады']:
            ticker = asset['ticker']
            if (ticker in self.player['portfolio'] and
                    self.player['portfolio'][ticker] > 0):
                interest_amount = (
                        self.player['portfolio'][ticker] * asset['yield'] / 100 / 52
                )
                self.player['balance'] += interest_amount
                self.player['interest_earned'] += interest_amount

    def update_portfolio_value(self) -> None:
        """Обновляет общую стоимость портфеля."""
        total = self.player['balance']
        for ticker, quantity in self.player['portfolio'].items():
            asset = self.find_asset_by_ticker(ticker)
            if asset:
                total += asset['price'] * quantity

        self.player['total_value'] = total
        self.player['total_profit'] = total - self.initial_balance

    def find_asset_by_ticker(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Находит актив по тикеру.

        Args:
            ticker: Тикер актива

        Returns:
            Данные актива или None если не найден
        """
        for asset_type in ASSETS.values():
            for asset in asset_type:
                if asset['ticker'] == ticker:
                    return asset
        return None

    def execute_trade(self) -> Tuple[bool, str]:
        """
        Выполняет торговую операцию.

        Returns:
            Кортеж (успех, сообщение)
        """
        if self.player['trades_today'] >= self.player['max_trades_per_day']:
            return False, "Достигнут лимит сделок на сегодня"

        try:
            quantity = int(self.quantity_input)
            if quantity <= 0:
                return False, "Количество должно быть больше 0"
        except ValueError:
            return False, "Неверное количество"

        if not self.selected_asset_ticker:
            return False, "Выберите актив"

        asset = self.find_asset_by_ticker(self.selected_asset_ticker)
        if not asset:
            return False, "Актив не найден"

        total_cost = asset['price'] * quantity
        if self.player['balance'] >= total_cost:
            self.player['balance'] -= total_cost
            if self.selected_asset_ticker in self.player['portfolio']:
                self.player['portfolio'][self.selected_asset_ticker] += quantity
            else:
                self.player['portfolio'][self.selected_asset_ticker] = quantity
            self.player['trades_today'] += 1
            self.update_portfolio_value()
            return True, f"Куплено {quantity} {asset['name']}"
        else:
            return False, "Недостаточно средств"

    def get_portfolio_distribution(self) -> Tuple[Dict[str, float], float]:
        """
        Возвращает распределение портфеля.

        Returns:
            Кортеж (распределение, общая стоимость)
        """
        distribution = {}
        total_value = 0

        for ticker, quantity in self.player['portfolio'].items():
            asset = self.find_asset_by_ticker(ticker)
            if asset:
                value = asset['price'] * quantity
                distribution[ticker] = value
                total_value += value

        return distribution, total_value


def initialize_game_objects(
        game_state: GameState
) -> Tuple[Button, Button, Button, InputField, List[TabButton]]:
    """
    Инициализирует игровые объекты.

    Args:
        game_state: Состояние игры

    Returns:
        Кортеж с игровыми объектами
    """
    new_game_btn = Button(
        50, 700, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT,
        "НОВАЯ ИГРА", BUTTON_COLOR, BUTTON_HOVER_COLOR
    )

    next_week_text = (
        f"СЛЕДУЮЩАЯ НЕДЕЛЯ ({game_state.current_week}/{game_state.total_weeks})"
    )
    next_week_btn = Button(
        250, 700, BUTTON_WIDTH_MEDIUM, BUTTON_HEIGHT,
        next_week_text, BUTTON_COLOR, BUTTON_HOVER_COLOR
    )

    execute_trade_btn = Button(
        920, 510, BUTTON_WIDTH_LARGE, 35,  # Изменена позиция кнопки покупки (опущена ниже)
        "КУПИТЬ", BUTTON_COLOR, BUTTON_HOVER_COLOR
    )

    quantity_input_field = InputField(
        690, 470, INPUT_FIELD_WIDTH, INPUT_FIELD_HEIGHT, "10"  # Выровнено по тексту "Количество"
    )

    tab_buttons = [
        TabButton(50, 160, 120, 40, "АКЦИИ", True),
        TabButton(180, 160, 120, 40, "ОБЛИГАЦИИ"),
        TabButton(310, 160, 120, 40, "ВКЛАДЫ")
    ]

    return (
        new_game_btn, next_week_btn, execute_trade_btn,
        quantity_input_field, tab_buttons
    )


def handle_user_input(
        event: pygame.event.Event,
        mouse_pos: Tuple[int, int],
        game_state: GameState,
        tab_buttons: List[TabButton],
        new_game_btn: Button,
        next_week_btn: Button,
        execute_trade_btn: Button,
        quantity_input_field: InputField
) -> None:
    """
    Обрабатывает пользовательский ввод.

    Args:
        event: Событие Pygame
        mouse_pos: Позиция мыши
        game_state: Состояние игры
        tab_buttons: Список вкладок
        new_game_btn: Кнопка новой игры
        next_week_btn: Кнопка следующей недели
        execute_trade_btn: Кнопка выполнения сделки
        quantity_input_field: Поле ввода количества
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        _handle_mouse_click(
            event, mouse_pos, game_state, tab_buttons,
            new_game_btn, next_week_btn, execute_trade_btn
        )

        quantity_input_field.handle_event(event)

    elif event.type == pygame.KEYDOWN:
        quantity_input_field.handle_event(event)


def _handle_mouse_click(
        event: pygame.event.Event,
        mouse_pos: Tuple[int, int],
        game_state: GameState,
        tab_buttons: List[TabButton],
        new_game_btn: Button,
        next_week_btn: Button,
        execute_trade_btn: Button
) -> None:
    """
    Обрабатывает клик мыши.
    """
    current_time = pygame.time.get_ticks()

    # Обработка табов
    for i, tab in enumerate(tab_buttons):
        if tab.is_clicked(mouse_pos, event):
            for t in tab_buttons:
                t.is_active = False
            tab.is_active = True
            game_state.selected_asset_type = ['акции', 'облигации', 'вклады'][i]
            game_state.selected_asset_ticker = None
            break

    if new_game_btn.is_clicked(mouse_pos, event):
        game_state.reset_game()
        next_week_btn.text = (
            f"СЛЕДУЮЩАЯ НЕДЕЛЯ ({game_state.current_week}/{game_state.total_weeks})"
        )
        game_state.message = "Новая игра начата!"
        game_state.message_type = "success"
        game_state.message_timer = current_time

    if (next_week_btn.is_clicked(mouse_pos, event) and
            not game_state.game_finished):

        if game_state.next_week():
            next_week_btn.text = (
                f"СЛЕДУЮЩАЯ НЕДЕЛЯ ({game_state.current_week}/{game_state.total_weeks})"
            )
            game_state.message = f"Неделя {game_state.current_week} началась!"
            game_state.message_type = "success"
            game_state.message_timer = current_time
        else:
            game_state.message = "Игра завершена!"
            game_state.message_type = "success"
            game_state.message_timer = current_time

    if execute_trade_btn.is_clicked(mouse_pos, event):
        game_state.quantity_input = game_state.quantity_input
        success, msg = game_state.execute_trade()
        game_state.message = msg
        game_state.message_type = "success" if success else "error"
        game_state.message_timer = current_time

    # Выбор актива
    y_pos = 210
    for asset in ASSETS[game_state.selected_asset_type]:
        card_rect = pygame.Rect(50, y_pos, CARD_WIDTH, CARD_HEIGHT)
        if card_rect.collidepoint(mouse_pos):
            game_state.selected_asset_ticker = asset['ticker']
            break
        y_pos += CARD_SPACING


def main() -> None:
    """Основная функция игры."""
    try:
        game_state = GameState()
        game_objects = initialize_game_objects(game_state)
        new_game_btn, next_week_btn, execute_trade_btn = game_objects[:3]
        quantity_input_field, tab_buttons = game_objects[3:]

        running = True
        while running:
            current_time = pygame.time.get_ticks()
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    handle_user_input(
                        event, mouse_pos, game_state, tab_buttons,
                        new_game_btn, next_week_btn, execute_trade_btn,
                        quantity_input_field
                    )

            # Обновление состояний
            new_game_btn.check_hover(mouse_pos)
            next_week_btn.check_hover(mouse_pos)
            execute_trade_btn.check_hover(mouse_pos)
            quantity_input_field.check_hover(mouse_pos)

            for tab in tab_buttons:
                tab.check_hover(mouse_pos)

            game_state.quantity_input = quantity_input_field.text
            game_state.update_portfolio_value()

            # Отрисовка
            if game_state.game_finished:
                _draw_final_screen(game_state, new_game_btn)
            else:
                _draw_main_screen(
                    game_state, new_game_btn, next_week_btn,
                    execute_trade_btn, quantity_input_field,
                    tab_buttons, current_time
                )

            pygame.display.flip()
            clock.tick(FPS)

    except Exception as e:
        print(f"Критическая ошибка в игре: {e}")
    finally:
        pygame.quit()
        sys.exit()


def _draw_final_screen(game_state: GameState, new_game_btn: Button) -> None:
    """Отрисовывает финальный экран игры."""
    screen.fill(BACKGROUND_COLOR)
    draw_vtb_header(screen, f"Неделя: {game_state.current_week}/{game_state.total_weeks}")

    final_text = f"Финальный результат: {format_currency(game_state.player['total_value'])}"
    draw_text(
        screen, final_text, large_font, VTB_DARK_BLUE,
        SCREEN_WIDTH // 2, 200, centered=True
    )

    new_game_btn.draw(screen)


def _draw_main_screen(
        game_state: GameState,
        new_game_btn: Button,
        next_week_btn: Button,
        execute_trade_btn: Button,
        quantity_input_field: InputField,
        tab_buttons: List[TabButton],
        current_time: int
) -> None:
    """Отрисовывает основной игровой экран."""
    screen.fill(BACKGROUND_COLOR)
    week_text = f"Неделя: {game_state.current_week}/{game_state.total_weeks}"
    draw_vtb_header(screen, week_text)

    _draw_portfolio_info(game_state)
    _draw_tabs(tab_buttons)
    _draw_asset_cards(game_state)
    _draw_portfolio_panel(game_state)
    _draw_trading_panel(game_state, quantity_input_field, execute_trade_btn)
    _draw_news_window(game_state)  # Перемещено после торговой панели

    new_game_btn.draw(screen)
    next_week_btn.enabled = not game_state.game_finished
    next_week_btn.draw(screen)

    _draw_message(game_state, current_time)


def _draw_portfolio_info(game_state: GameState) -> None:
    """Отрисовывает информацию о портфеле."""
    portfolio_card = draw_card(screen, 50, 110, 800, 60)
    draw_text(
        screen, "Общая стоимость портфеля", normal_font,
        VTB_DARK_GRAY, 70, 125
    )
    draw_text(
        screen, format_currency(game_state.player['total_value']),
        large_font, VTB_DARK_BLUE, 70, 145
    )

    total_return = (
                           (game_state.player['total_value'] - game_state.initial_balance) /
                           game_state.initial_balance
                   ) * 100
    return_color = VTB_GREEN if total_return >= 0 else VTB_RED
    return_sign = "+" if total_return >= 0 else ""
    draw_text(
        screen, f"Доходность: {return_sign}{total_return:.1f}%",
        normal_font, return_color, 300, 145
    )

    draw_text(
        screen, f"Баланс: {format_currency(game_state.player['balance'])}",
        normal_font, VTB_DARK_BLUE, 500, 145
    )


def _draw_news_window(game_state: GameState) -> None:
    """Отрисовывает окно рыночных новостей с пользовательским изображением как иконкой."""
    window_rect = pygame.Rect(570, 580, 580, 150)

    # Основное окно
    pygame.draw.rect(screen, VTB_WHITE, window_rect, border_radius=8)
    pygame.draw.rect(screen, VTB_BORDER_GRAY, window_rect, 2, border_radius=8)

    # Заголовок окна
    header_rect = pygame.Rect(window_rect.x, window_rect.y, window_rect.width, 30)
    pygame.draw.rect(screen, VTB_LIGHT_BLUE, header_rect, border_radius=8)
    pygame.draw.rect(screen, VTB_BORDER_GRAY, header_rect, 1, border_radius=8)

    # Загрузка и отрисовка вашего изображения как иконки в заголовке
    try:
        # Используем английское имя файла
        news_icon = pygame.image.load("news_icon.png")
        # Масштабируем до маленького размера для заголовка
        icon_size = (20, 20)  # Маленький размер для заголовка
        news_icon = pygame.transform.smoothscale(news_icon, icon_size)
        # Позиционируем иконку слева в заголовке
        icon_rect = news_icon.get_rect(midleft=(window_rect.x + 10, window_rect.y + 15))
        screen.blit(news_icon, icon_rect)

        # Сдвигаем текст заголовка вправо, чтобы освободить место для иконки
        header_text_x = window_rect.centerx + 10
    except (pygame.error, FileNotFoundError) as e:
        print(f"Ошибка загрузки иконки новостей: {e}")
        # Если изображение не найдено, используем эмодзи как запасной вариант
        header_text_x = window_rect.centerx

    draw_text(
        screen, "РЫНОЧНЫЕ НОВОСТИ", small_font, VTB_DARK_BLUE,
        header_text_x, window_rect.y + 15, centered=True
    )

    # Содержимое новостей
    news_start_y = window_rect.y + 40

    if game_state.market_news:
        # Показываем несколько последних новостей
        news_to_show = game_state.market_news[-3:]  # Последние 3 новости
        for i, news in enumerate(news_to_show):
            if len(news) > 35:
                news = news[:35] + "..."
            draw_text(
                screen, f"• {news}", small_font, VTB_DARK_GRAY,
                window_rect.x + 20, news_start_y + i * 25
            )
    else:
        draw_text(
            screen, "Рынок стабилен", small_font, VTB_DARK_GRAY,
            window_rect.centerx, news_start_y + 20, centered=True
        )


def _draw_tabs(tab_buttons: List[TabButton]) -> None:
    """Отрисовывает вкладки."""
    for tab in tab_buttons:
        tab.rect.y = 180
        tab.draw(screen)


def _draw_asset_cards(game_state: GameState) -> None:
    """Отрисовывает карточки активов."""
    y_pos = 210
    for asset in ASSETS[game_state.selected_asset_type]:
        portfolio_qty = game_state.player['portfolio'].get(asset['ticker'], 0)

        if 'VTB' in asset['ticker']:
            card = VTBAssetCard(asset, 50, y_pos, CARD_WIDTH, CARD_HEIGHT)
        else:
            card = AssetCard(asset, 50, y_pos, CARD_WIDTH, CARD_HEIGHT)

        card.is_selected = (asset['ticker'] == game_state.selected_asset_ticker)
        card.draw(screen, portfolio_qty)
        y_pos += CARD_SPACING


def _draw_portfolio_panel(game_state: GameState) -> None:
    """Отрисовывает панель портфеля."""
    portfolio_card = draw_card(screen, 570, 210, 580, 150)
    draw_text(
        screen, "ПОРТФЕЛЬ ИНВЕСТИЦИЙ", header_font, VTB_DARK_BLUE, 590, 230
    )

    portfolio_info = [
        f"Сделок сегодня: {game_state.player['trades_today']}/{game_state.player['max_trades_per_day']}",
        f"Всего активов: {len(game_state.player['portfolio'])}",
        f"Баланс: {format_currency(game_state.player['balance'])}"
    ]

    for i, info in enumerate(portfolio_info):
        draw_text(screen, info, small_font, VTB_DARK_GRAY, 590, 260 + i * 25)

    distribution, total_dist_value = game_state.get_portfolio_distribution()
    if total_dist_value > 0:
        # Исправление: график сдвинут ближе к концу контейнера
        draw_pie_chart(screen, 950, 285, 40, distribution, total_dist_value)  # Сдвинуто вправо
        y_legend = 260
        colors = [VTB_BLUE, VTB_GREEN, VTB_PURPLE, VTB_YELLOW]
        for i, (ticker, value) in enumerate(list(distribution.items())[:4]):
            asset = game_state.find_asset_by_ticker(ticker)
            if asset:
                color = colors[i % len(colors)]
                pygame.draw.rect(screen, color, (750, y_legend, 10, 10))
                percentage = (value / total_dist_value) * 100
                draw_text(
                    screen, f"{asset['ticker']} ({percentage:.1f}%)",
                    small_font, VTB_DARK_GRAY, 765, y_legend
                )
                y_legend += 15
    else:
        draw_text(
            screen, "Портфель пуст", small_font, VTB_DARK_GRAY,
            850, 285, centered=True
        )


def _draw_trading_panel(
        game_state: GameState,
        quantity_input_field: InputField,
        execute_trade_btn: Button
) -> None:
    """Отрисовывает панель торговли."""
    trade_card = draw_card(screen, 570, 370, 580, 200)
    draw_text(
        screen, "ТОРГОВАЯ ОПЕРАЦИЯ", header_font, VTB_DARK_BLUE, 590, 390
    )

    if game_state.selected_asset_ticker:
        asset = game_state.find_asset_by_ticker(game_state.selected_asset_ticker)
        if asset:
            draw_text(
                screen, f"Актив: {asset['name']}", normal_font,
                VTB_DARK_BLUE, 590, 430
            )

    # Выравнивание поля ввода с текстом "Количество"
    quantity_text_y = 470
    draw_text(
        screen, "Количество:", normal_font, VTB_DARK_BLUE, 590, quantity_text_y
    )

    # Поле ввода выровнено по тексту "Количество"
    quantity_input_field.rect.x = 690
    quantity_input_field.rect.y = quantity_text_y - 8  # Центрируем по вертикали относительно текста
    quantity_input_field.draw(screen)

    if game_state.selected_asset_ticker:
        asset = game_state.find_asset_by_ticker(game_state.selected_asset_ticker)
        if asset:
            try:
                qty = int(quantity_input_field.text) if quantity_input_field.text else 0
                cost = asset['price'] * qty
                draw_text(
                    screen, f"Стоимость: {format_currency(cost)}",
                    normal_font, VTB_DARK_BLUE, 850, quantity_text_y
                )
            except ValueError:
                pass

    # Кнопка покупки опущена ниже
    execute_trade_btn.rect.x = 920
    execute_trade_btn.rect.y = 510  # Опущена ниже
    execute_trade_btn.draw(screen)


def _draw_message(game_state: GameState, current_time: int) -> None:
    """Отрисовывает сообщение для пользователя."""
    if current_time - game_state.message_timer < MESSAGE_DISPLAY_TIME:
        msg_color = VTB_GREEN if game_state.message_type == "success" else VTB_RED
        msg_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 170, 400, 40)
        pygame.draw.rect(screen, msg_color, msg_rect, border_radius=8)
        pygame.draw.rect(screen, VTB_WHITE, msg_rect, 2, border_radius=8)
        draw_text(
            screen, game_state.message, normal_font, VTB_WHITE,
            SCREEN_WIDTH // 2, 190, centered=True
        )


if __name__ == "__main__":
    main()