import pygame
from board import Board
from ai_player import ChessAI

class Game:
    def draw(self):
        """Отрисовка игры"""
        self.draw_board()
        self.draw_pieces()
        
        if self.selected_pos:
            self.draw_selection()
        
        if self.valid_moves:
            self.draw_valid_moves() 
        
        if self.game_over:
            self.draw_game_over()
    
    def draw_board(self):
        """Отрисовка доски"""
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )