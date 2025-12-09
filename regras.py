import copy
from typing import List, Tuple, Optional

# Constantes
TABULEIRO_TAM = 8
BRANCO = 1
VERMELHO = -1
DAMA_BRANCO = 2
DAMA_VERMELHO = -2

class DamasRules:
    """
    Motor de regras oficial para Damas Brasileiras (64 casas).
    Implementa Lei da Maioria, Captura Obrigatória e Dama Voadora.
    """

    @staticmethod
    def criar_tabuleiro() -> List[List[int]]:
        tab = [[0] * 8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        tab[row][col] = BRANCO
                    elif row > 4:
                        tab[row][col] = VERMELHO
        return tab

    @staticmethod
    def get_valid_moves(board: List[List[int]], player: int) -> List[dict]:
        """
        Retorna todos os movimentos válidos para o jogador.
        Estrutura de retorno: [{'start': (r,c), 'path': [(r,c), ...], 'captures': [...]}]
        APLICA A LEI DA MAIORIA: Retorna apenas os movimentos com maior número de capturas.
        """
        moves = []
        has_captures = False

        # 1. Tenta encontrar capturas (prioridade máxima)
        for r in range(TABULEIRO_TAM):
            for c in range(TABULEIRO_TAM):
                piece = board[r][c]
                if piece == 0 or (piece > 0 and player == -1) or (piece < 0 and player == 1):
                    continue
                
                captures = DamasRules._get_capture_moves(board, r, c, piece)
                moves.extend(captures)

        # Filtragem pela LEI DA MAIORIA
        if moves:
            max_captures = max(len(m['captures']) for m in moves)
            moves = [m for m in moves if len(m['captures']) == max_captures]
            has_captures = True

        # 2. Se não houver capturas, busca movimentos simples
        if not has_captures:
            for r in range(TABULEIRO_TAM):
                for c in range(TABULEIRO_TAM):
                    piece = board[r][c]
                    if piece == 0 or (piece > 0 and player == -1) or (piece < 0 and player == 1):
                        continue
                    moves.extend(DamasRules._get_simple_moves(board, r, c, piece))

        return moves

    @staticmethod
    def _get_simple_moves(board, r, c, piece) -> List[dict]:
        moves = []
        is_king = abs(piece) == 2
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Pedras só andam para frente
        if not is_king:
            forward = 1 if piece == BRANCO else -1
            valid_dirs = [(dr, dc) for dr, dc in directions if dr == forward]
        else:
            valid_dirs = directions # Damas andam em todas

        for dr, dc in valid_dirs:
            dist = 1
            while True:
                nr, nc = r + (dr * dist), c + (dc * dist)
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                
                if board[nr][nc] == 0:
                    moves.append({
                        'start': (r, c),
                        'end': (nr, nc),
                        'path': [(nr, nc)],
                        'captures': []
                    })
                    if not is_king: break # Pedra anda só 1 casa
                    dist += 1 # Dama continua verificando
                else:
                    break # Bloqueado
        return moves

    @staticmethod
    def _get_capture_moves(board, r, c, piece, captured_positions=None) -> List[dict]:
        """Busca recursiva por cadeias de captura."""
        if captured_positions is None:
            captured_positions = set()

        moves = []
        is_king = abs(piece) == 2
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Pedras capturam em todas as direções

        for dr, dc in directions:
            dist_enemy = 1
            while True:
                # Localizar inimigo
                er, ec = r + (dr * dist_enemy), c + (dc * dist_enemy)
                
                if not (0 <= er < 8 and 0 <= ec < 8):
                    break # Fim do tabuleiro

                piece_at_pos = board[er][ec]

                if piece_at_pos == 0:
                    if not is_king: break # Pedra não pode ter buracos antes do inimigo
                    dist_enemy += 1
                    continue
                
                # Se achou peça amiga, para
                if (piece_at_pos > 0 and piece > 0) or (piece_at_pos < 0 and piece < 0):
                    break
                
                # Se achou peça inimiga
                if (er, ec) in captured_positions:
                    break # Já capturada nesta cadeia

                # Verificar casa de pouso após o inimigo
                dist_land = dist_enemy + 1
                while True:
                    lr, lc = r + (dr * dist_land), c + (dc * dist_land)
                    
                    if not (0 <= lr < 8 and 0 <= lc < 8):
                        break
                    
                    if board[lr][lc] != 0:
                        break # Pouso bloqueado

                    # Movimento Válido! Adicionar à cadeia recursiva
                    current_capture = (er, ec)
                    new_captured = captured_positions | {current_capture}
                    
                    # Simular tabuleiro para o próximo passo
                    board_copy = [row[:] for row in board]
                    # Nota: Não removemos a peça ainda na regra oficial até o fim da jogada,
                    # mas para a recursão precisamos considerar a posição de pouso como ocupada pela peça ativa
                    # e a posição original vazia.
                    
                    # Recursão
                    sub_moves = DamasRules._get_capture_moves(
                        board, lr, lc, piece, new_captured
                    )

                    if sub_moves:
                        for sub in sub_moves:
                            moves.append({
                                'start': (r, c),
                                'end': sub['end'],
                                'path': [(lr, lc)] + sub['path'],
                                'captures': [current_capture] + sub['captures']
                            })
                    else:
                        # Fim da cadeia
                        moves.append({
                            'start': (r, c),
                            'end': (lr, lc),
                            'path': [(lr, lc)],
                            'captures': [current_capture]
                        })

                    if not is_king: break # Pedra pousa imediatamente após
                    dist_land += 1 # Dama pode escolher onde pousar
                
                break # Só analisa a primeira peça encontrada na diagonal

        return moves

    @staticmethod
    def apply_move(board: List[List[int]], move: dict) -> List[List[int]]:
        """Retorna um NOVO tabuleiro com o movimento aplicado."""
        new_board = [row[:] for row in board]
        start_r, start_c = move['start']
        end_r, end_c = move['end']
        piece = new_board[start_r][start_c]

        # Mover peça
        new_board[start_r][start_c] = 0
        new_board[end_r][end_c] = piece

        # Remover capturados
        for cr, cc in move['captures']:
            new_board[cr][cc] = 0

        # Promoção
        if piece == BRANCO and end_r == 7:
            new_board[end_r][end_c] = DAMA_BRANCO
        elif piece == VERMELHO and end_r == 0:
            new_board[end_r][end_c] = DAMA_VERMELHO
        
        return new_board
