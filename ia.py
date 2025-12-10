import math
from regras import DamasRules, BRANCO, VERMELHO

PESO_PEDRA = 100
PESO_DAMA = 300
PESO_MOBILIDADE = 5
PESO_DEFESA_BASE = 20

BOARD_WEIGHTS = [
    [0, 4, 0, 4, 0, 4, 0, 4],
    [4, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 2, 0, 2, 0, 4],
    [4, 0, 5, 0, 5, 0, 3, 0],
    [0, 3, 0, 5, 0, 5, 0, 4],
    [4, 0, 2, 0, 2, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 4],
    [4, 0, 4, 0, 4, 0, 4, 0],
]

class DamasAI:
    def __init__(self, depth=4):
        self.max_depth = depth
        self.nodes_evaluated = 0

    def get_best_move(self, board, player):
        self.nodes_evaluated = 0
        _, best_move = self.minimax(board, self.max_depth, True, -math.inf, math.inf, player)
        print(f"IA analisou {self.nodes_evaluated} posições.")
        return best_move

    def evaluate(self, board, player_color):
        """
        Avalia o tabuleiro do ponto de vista do 'player_color'.
        Retorna positivo se 'player_color' estiver ganhando.
        """
        score = 0
        my_pieces = 0
        enemy_pieces = 0
        
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece == 0: continue
                
                val = PESO_PEDRA
                if abs(piece) == 2:
                    val = PESO_DAMA
                
                val += BOARD_WEIGHTS[r][c]

                if piece == 1 and r == 0: val += PESO_DEFESA_BASE
                if piece == -1 and r == 7: val += PESO_DEFESA_BASE

                if (piece > 0 and player_color == 1) or (piece < 0 and player_color == -1):
                    score += val
                    my_pieces += 1
                else:
                    score -= val
                    enemy_pieces += 1

        return score

    def quiescence(self, board, alpha, beta, player_color):
        """
        Busca de Quiescência: Continua a busca além do limite de profundidade
        apenas para movimentos de captura, evitando o 'Horizon Effect'.
        """
        stand_pat = self.evaluate(board, player_color)
        self.nodes_evaluated += 1

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        all_moves = DamasRules.get_valid_moves(board, player_color)
        capture_moves = [m for m in all_moves if m['captures']]

        if not capture_moves:
            return alpha

        for move in capture_moves:
            new_board = DamasRules.apply_move(board, move)
            score = -self.quiescence(new_board, -beta, -alpha, -player_color)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha

    def minimax(self, board, depth, maximizing, alpha, beta, player_color):
        if depth == 0:
            return self.quiescence(board, alpha, beta, player_color if maximizing else -player_color), None

        valid_moves = DamasRules.get_valid_moves(board, player_color if maximizing else -player_color)
        if not valid_moves:
            return (-10000 + depth) if maximizing else (10000 - depth), None

        best_move = None

        if maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                new_board = DamasRules.apply_move(board, move)
                eval_val, _ = self.minimax(new_board, depth - 1, False, alpha, beta, player_color)
                
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = move
                
                alpha = max(alpha, eval_val)
                if beta <= alpha: break
            return max_eval, best_move
        
        else:
            min_eval = math.inf
            for move in valid_moves:
                new_board = DamasRules.apply_move(board, move)
                eval_val, _ = self.minimax(new_board, depth - 1, True, alpha, beta, player_color)
                
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                beta = min(beta, eval_val)
                if beta <= alpha: break
            return min_eval, best_move
