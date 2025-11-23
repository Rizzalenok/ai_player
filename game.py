import pygame
from board import Board
from ai_player import ChessAI

class Game:
    
    def draw(self):
        self.draw_board()
        self.draw_pieces()
        
        if self.selected_pos:
            self.draw_selection()
        
        if self.valid_moves:
            self.draw_valid_moves() 
        
        if self.game_over:
            self.draw_game_over()
    
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
    
    def draw_pieces(self):
        piece_symbols = {
            'white': {'King': '♔', 'Queen': '♕', 'Rook': '♖', 
                    'Bishop': '♗', 'Knight': '♘', 'Pawn': '♙'},
            'black': {'King': '♚', 'Queen': '♛', 'Rook': '♜',
                    'Bishop': '♝', 'Knight': '♞', 'Pawn': '♟'}
        }
        
        try:
            font = pygame.font.SysFont('segoeuisymbol', 70)
        except:
            try:
                font = pygame.font.SysFont('dejavusans', 70)
            except:
                font = pygame.font.Font(None, 70)
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    symbol = piece_symbols[piece.color][piece.name]
                    
                    if piece.color == 'white':
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
                    
                    text = font.render(symbol, True, color)
                    text_rect = text.get_rect(
                        center=(col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                    )
                    
                    if piece.color == 'white':
                        outline = font.render(symbol, True, (0, 0, 0))
                        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                            outline_rect = text_rect.copy()
                            outline_rect.x += dx
                            outline_rect.y += dy
                            self.screen.blit(outline, outline_rect)
                    else:
                        outline = font.render(symbol, True, (255, 255, 255))
                        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                            outline_rect = text_rect.copy()
                            outline_rect.x += dx
                            outline_rect.y += dy
                            self.screen.blit(outline, outline_rect)
                    
                    self.screen.blit(text, text_rect)

    def draw_selection(self):
        row, col = self.selected_pos
        pygame.draw.rect(
            self.screen,
            self.HIGHLIGHT,
            (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
             self.SQUARE_SIZE, self.SQUARE_SIZE),
            5
        )
    
    def draw_valid_moves(self):
        for row, col in self.valid_moves:
            pygame.draw.circle(
                self.screen,
                self.VALID_MOVE,
                (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                 row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                15
            )