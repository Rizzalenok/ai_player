import pygame
from game import Game

class Button:

    def __init__(self, x, y, width, height ,text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 48)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3, border_radius=10)
        
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
def show_menu(screen):
    ai_button = Button(200, 250, 400, 80, "Играть с ИИ", (52, 78, 137), (70, 100, 180))
    pvp_button = Button(200, 370, 400, 80, "Играть с другом", (37, 103, 58), (50, 140, 80))
    quit_button = Button(200, 490, 400, 80, "Выход", (120, 40, 40), (160, 60, 60))
    
    buttons = [ai_button, pvp_button, quit_button]
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((30, 30, 30))
        
        title_font = pygame.font.Font(None, 80)
        title = title_font.render("ШАХМАТЫ", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 120))
        screen.blit(title, title_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            
            for button in buttons:
                button.handle_event(event)
            
            if ai_button.handle_event(event):
                return 'ai'
            
            if pvp_button.handle_event(event):
                return 'pvp'
            
            if quit_button.handle_event(event):
                return None
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Шахматы')
    
    while True:
        mode = show_menu(screen)
        
        if mode is None:
            break
        
        if mode == 'ai':
            difficulty = show_difficulty_menu(screen)
            if difficulty is None:
                continue
            game = Game(screen, ai_enabled=True, ai_color='black', ai_depth=difficulty)
        else:
            game = Game(screen, ai_enabled=False)
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_click(pygame.mouse.get_pos())
            
            game.update()
            game.draw()
            pygame.display.flip()
            
            if game.ai_thinking:
                game.make_ai_move()
            
            if game.game_over:
                show_game_over_screen(screen, game.winner)
                running = False
    
    pygame.quit()


def show_difficulty_menu(screen):
    easy_button = Button(200, 200, 400, 80, "Легко (быстро)", (52, 78, 137), (70, 100, 180))
    medium_button = Button(200, 320, 400, 80, "Средне", (52, 78, 137), (70, 100, 180))
    hard_button = Button(200, 440, 400, 80, "Сложно (медленно)", (52, 78, 137), (70, 100, 180))
    back_button = Button(200, 560, 400, 80, "Назад", (120, 40, 40), (160, 60, 60))
    
    buttons = [easy_button, medium_button, hard_button, back_button]
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((30, 30, 30))
        
        title_font = pygame.font.Font(None, 60)
        title = title_font.render("Выберите сложность", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 100))
        screen.blit(title, title_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            
            for button in buttons:
                button.handle_event(event)
            
            if easy_button.handle_event(event):
                return 2
            if medium_button.handle_event(event):
                return 3
            if hard_button.handle_event(event):
                return 4
            if back_button.handle_event(event):
                return None
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def show_game_over_screen(screen, winner):
    """Экран окончания игры"""
    overlay = pygame.Surface((800, 800))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    big_font = pygame.font.Font(None, 72)
    text = big_font.render(f"Победа: {winner}!", True, (255, 215, 0))
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 40)
    restart_text = font.render("Нажмите любую клавишу", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(400, 400))
    screen.blit(restart_text, restart_rect)
    
    continue_text = font.render("для возврата в меню", True, (255, 255, 255))
    continue_rect = continue_text.get_rect(center=(400, 450))
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


if __name__ == '__main__':
    main()