import pygame

pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 300, 200
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
BUTTON_FONT = pygame.font.Font(None, 36)
BODY_FONT = pygame.font.Font(None, 18)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Live Subtitles for OBS")

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = BUTTON_FONT.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

class Text:
    def __init__(self, x, y, width, height, text):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def set_text(self, text):
        self.text = text
    
    def draw(self, screen):
        lines = self.wrap_text(self.text, self.width, BODY_FONT)
        for i, line in enumerate(lines):
            text_surface = BODY_FONT.render(line, True, BLACK)
            screen.blit(text_surface, (self.x, self.y + i * BODY_FONT.get_linesize()))
    
    def wrap_text(self, text, max_width, font):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        
        lines.append(current_line)  # Add the last line
        return lines