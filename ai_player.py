import math

class ChessAI:

    def __init__(self, depth=3, color='black'):
        self.depth = depth
        self.color = color
        self.opponent_color = 'white' if color == 'black' else 'black'

        self.piece_values = {
            'Pawn': 100,
            'Knight': 320,
            'Bishop': 330,
            'Rook': 500,
            'Queen': 900,
            'King': 20000
        }

    def get_best_move(self, board):
        best_move = None
        best_value = -math.inf

        possible_moves = self._get_all_possible_moves(board, self.color)

        if not possible_moves:
            return None

        for from_pos, to_pos in possible_moves:
            piece = board.get_piece(from_pos)
            captured = board.get_piece(to_pos)
            old_pos = piece.pos

            board.move_piece(from_pos, to_pos)

            value = self._minimax_basic(board, self.depth - 1, False)

            board.set_piece(from_pos, piece)
            board.set_piece(to_pos, captured)
            piece.pos = old_pos

            if value > best_value:
                best_value = value
                best_move = (from_pos, to_pos)

        return best_move

    def _minimax_basic(self, board, depth, is_maximizing):
        if depth == 0:
            return self._evaluate_board_basic(board)

        color = self.color if is_maximizing else self.opponent_color
        possible_moves = self._get_all_possible_moves(board, color)

        if not possible_moves:
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for from_pos, to_pos in possible_moves:
                piece = board.get_piece(from_pos)
                captured = board.get_piece(to_pos)
                old_pos = piece.pos

                board.move_piece(from_pos, to_pos)
                eval = self._minimax_basic(board, depth - 1, False)
                board.set_piece(from_pos, piece)
                board.set_piece(to_pos, captured)
                piece.pos = old_pos

                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for from_pos, to_pos in possible_moves:
                piece = board.get_piece(from_pos)
                captured = board.get_piece(to_pos)
                old_pos = piece.pos

                board.move_piece(from_pos, to_pos)
                eval = self._minimax_basic(board, depth - 1, True)
                board.set_piece(from_pos, piece)
                board.set_piece(to_pos, captured)
                piece.pos = old_pos

                min_eval = min(min_eval, eval)
            return min_eval

    def _get_all_possible_moves(self, board, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(board)
                    for move in valid_moves:
                        if board.is_legal_move((row, col), move, color):
                            moves.append(((row, col), move))
        return moves

    def _evaluate_board_basic(self, board):
        score = 0

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    piece_value = self.piece_values[piece.name]

                    if piece.color == self.color:
                        score += piece_value
                    else:
                        score -= piece_value

        return score

    def _get_piece_positional_value(self, piece, row, col):
        return self.piece_values[piece.name]