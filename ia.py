import math
from regras import DamasRules, BRANCO, VERMELHO

# Pesos da Avaliação
PESO_PEDRA = 100
PESO_DAMA = 300  # Damas valem 3x uma pedra
PESO_MOBILIDADE = 5  # Bônus por ter mais opções de movimento
PESO_DEFESA_BASE = 20 # Bônus por manter a linha de trás fechada

# Tabela de calor posicional (8x8)
# Valores mais altos incentivam a IA a ocupar essas casas.
# Bordas são seguras (4), Centro é forte (3), Cantos mortos (1).
BOARD_WEIGHTS = [
    [0, 4, 0, 4, 0, 4, 0, 4], # Linha 0 (Base Brancas)
    [4, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 2, 0, 2, 0, 4],
    [4, 0, 5, 0, 5, 0, 3, 0], # Centro alto valor
    [0, 3, 0, 5, 0, 5, 0, 4], # Centro alto valor
    [4, 0, 2, 0, 2, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 4],
    [4, 0, 4, 0, 4, 0, 4, 0], # Linha 7 (Base Vermelhas)
]

class DamasAI:
    def __init__(self, depth=4):
        self.max_depth = depth
        self.nodes_evaluated = 0

    def get_best_move(self, board, player):
        self.nodes_evaluated = 0
        # A IA sempre quer MAXIMIZAR o score dela.
        # Passamos 'player' para saber quem somos, mas a recursão trata alpha/beta padrão.
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
        
        # 1. Avaliação Material e Posicional
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece == 0: continue
                
                # Determina valor base da peça + posição
                val = PESO_PEDRA
                if abs(piece) == 2:
                    val = PESO_DAMA
                
                # Adiciona o valor da posição (onde a peça está)
                val += BOARD_WEIGHTS[r][c]

                # Defesa da Base (Impede promoções inimigas)
                # Se for BRANCO (1), proteger linha 0. Se VERMELHO (-1), proteger linha 7.
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

        # Gera APENAS movimentos de captura nesta fase
        # Precisamos filtrar moves que tenham 'captures' não vazio
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
        # Se chegou ao limite, entra na Quiescência em vez de retornar direto
        if depth == 0:
            # Se for a vez de 'player_color' (maximizing), chamamos normal.
            # A quiescência retorna o valor do tabuleiro estático.
            return self.quiescence(board, alpha, beta, player_color if maximizing else -player_color), None

        # Verifica vitória/derrota
        valid_moves = DamasRules.get_valid_moves(board, player_color if maximizing else -player_color)
        if not valid_moves:
            # Sem movimentos: Derrota (retorna valor muito baixo) ou Vitória (valor muito alto)
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
                # Passamos player_color inalterado para manter a referência de quem é o "Heroi" da avaliação
                eval_val, _ = self.minimax(new_board, depth - 1, True, alpha, beta, player_color)
                
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                
                beta = min(beta, eval_val)
                if beta <= alpha: break
            return min_eval, best_move
