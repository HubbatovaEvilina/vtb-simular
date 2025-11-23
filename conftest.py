"""
Конфигурация для тестов инвестиционного симулятора.
"""

import pytest
import pygame
import os
import tempfile


@pytest.fixture(autouse=True)
def mock_pygame():
    """Мокаем Pygame для всех тестов."""
    # Мокаем основные функции Pygame
    pygame.init = lambda: None
    pygame.quit = lambda: None
    pygame.display.set_mode = lambda size: None
    pygame.display.flip = lambda: None

    # Мокаем шрифты
    pygame.font.Font = lambda *args: type('MockFont', (), {
        'render': lambda self, text, antialias, color: type('MockSurface', (), {
            'get_rect': lambda self: type('MockRect', (), {
                'center': (0, 0),
                'topleft': (0, 0)
            })()
        })()
    })()

    # Мокаем Surface
    pygame.Surface = lambda size, flags=0: type('MockSurface', (), {
        'get_rect': lambda self: type('MockRect', (), {
            'center': (0, 0),
            'topleft': (0, 0),
            'x': 0, 'y': 0, 'width': size[0], 'height': size[1]
        })(),
        'blit': lambda self, source, dest: None,
        'get_size': lambda self: size
    })()

    # Константы Pygame
    pygame.SRCALPHA = 0
    pygame.MOUSEBUTTONDOWN = 5
    pygame.MOUSEBUTTONUP = 6
    pygame.KEYDOWN = 2
    pygame.K_BACKSPACE = 8
    pygame.K_RETURN = 13

    return pygame


@pytest.fixture
def temp_logos_dir():
    """Создает временную директорию для логотипов."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_logos_dir = 'logos'
        # Временно подменяем путь к логотипам
        import investment_simulator
        investment_simulator.LOGOS_DIR = temp_dir
        yield temp_dir
        # Возвращаем оригинальный путь
        investment_simulator.LOGOS_DIR = original_logos_dir


@pytest.fixture
def sample_game_state():
    """Создает образец состояния игры для тестов."""
    from investment_simulator import GameState
    game_state = GameState()
    return game_state


@pytest.fixture
def sample_asset():
    """Создает образец актива для тестов."""
    return {
        'name': 'Тестовый актив',
        'ticker': 'TEST',
        'price': 100.0,
        'base_price': 100.0,
        'change': 0.0,
        'dividend': 5.0,
        'risk': 'Низкий',
        'volatility': 0.02,
        'color': (0, 255, 0),
        'logo': 'TEST'
    }