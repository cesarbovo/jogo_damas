import copy
from typing import List, Tuple, Optional

TABULEIRO_TAM = 8
BRANCO = 1
VERMELHO = -1
DAMA_BRANCO = 2
DAMA_VERMELHO = -2

class DamasRules:
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
        moves = []
        has_captures = False

        for r in range(TABULEIRO_TAM):
            for c in range(TABULEIRO_TAM):
                piece = board[r][c]
                if piece == 0 or (piece > 0 and player == -1) or (piece < 0 and player == 1):
                    continue
                
                captures = DamasRules._get_capture_moves(board, r, c, piece)
                moves.extend(captures)

        if moves:
            max_captures = max(len(m['captures']) for m in moves)
            moves = [m for m in moves if len(m['captures']) == max_captures]
            has_captures = True

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
        
        if not is_king:
            forward = 1 if piece == BRANCO else -1
            valid_dirs = [(dr, dc) for dr, dc in directions if dr == forward]
        else:
            valid_dirs = directions

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
                    if not is_king: break
                    dist += 1
                else:
                    break
        return moves

    @staticmethod
    def _get_capture_moves(board, r, c, piece, captured_positions=None) -> List[dict]:
        if captured_positions is None:
            captured_positions = set()

        moves = []
        is_king = abs(piece) == 2
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            dist_enemy = 1
            while True:
                er, ec = r + (dr * dist_enemy), c + (dc * dist_enemy)
                
                if not (0 <= er < 8 and 0 <= ec < 8):
                    break

                piece_at_pos = board[er][ec]

                if piece_at_pos == 0:
                    if not is_king: break
                    dist_enemy += 1
                    continue
                
                if (piece_at_pos > 0 and piece > 0) or (piece_at_pos < 0 and piece < 0):
                    break
                
                if (er, ec) in captured_positions:
                    break

                dist_land = dist_enemy + 1
                while True:
                    lr, lc = r + (dr * dist_land), c + (dc * dist_land)
                    
                    if not (0 <= lr < 8 and 0 <= lc < 8):
                        break
                    
                    if board[lr][lc] != 0:
                        break

                    current_capture = (er, ec)
                    new_captured = captured_positions | {current_capture}
                    
                    board_copy = [row[:] for row in board]
                    
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
                        moves.append({
                            'start': (r, c),
                            'end': (lr, lc),
                            'path': [(lr, lc)],
                            'captures': [current_capture]
                        })

                    if not is_king: break
                    dist_land += 1
                
                break

        return moves

    @staticmethod
    def apply_move(board: List[List[int]], move: dict) -> List[List[int]]:
        new_board = [row[:] for row in board]
        start_r, start_c = move['start']
        end_r, end_c = move['end']
        piece = new_board[start_r][start_c]

        new_board[start_r][start_c] = 0
        new_board[end_r][end_c] = piece

        for cr, cc in move['captures']:
            new_board[cr][cc] = 0

        if piece == BRANCO and end_r == 7:
            new_board[end_r][end_c] = DAMA_BRANCO
        elif piece == VERMELHO and end_r == 0:
            new_board[end_r][end_c] = DAMA_VERMELHO
        
        return new_board
        
