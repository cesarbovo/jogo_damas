import tkinter as tk
from tkinter import ttk, messagebox
import time
import math
import copy
from regras import DamasRules, BRANCO, VERMELHO

COR_CASA_CLARA = "#F0D9B5"
COR_CASA_ESCURA = "#B58863"
COR_PECA_BRANCA = "#FFFFFF"
COR_PECA_VERMELHA = "#FF4444"
COR_DESTINO = "#AAFF00"
COR_HIGHLIGHT_CODE = "#FFFF00"
COR_TEXTO_CODIGO = "#D4D4D4"
COR_FUNDO_CODIGO = "#1E1E1E"

MINIMAX_CODE_STR = """def minimax(board, depth, is_max, alpha, beta):
 1.  if depth == 0:
 2.      return evaluate(board)
 3.
 4.  if is_max:
 5.      max_eval = -infinity
 6.      for move in get_valid_moves(board, MAX):
 7.          new_board = apply_move(board, move)
 8.          eval = minimax(new_board, depth-1, False, alpha, beta)
 9.          max_eval = max(max_eval, eval)
10.          alpha = max(alpha, max_eval)
11.          if beta <= alpha: break # Poda Beta
12.      return max_eval
13.
14.  else:
15.      min_eval = +infinity
16.      for move in get_valid_moves(board, MIN):
17.          new_board = apply_move(board, move)
18.          eval = minimax(new_board, depth-1, True, alpha, beta)
19.          min_eval = min(min_eval, eval)
20.          beta = min(beta, min_eval)
21.          if beta <= alpha: break # Poda Alpha
22.      return min_eval
"""

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

class VisualizadorMinimax:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Educativo: Algoritmo Minimax")
        self.root.geometry("1200x700")
        
        self.board = DamasRules.criar_tabuleiro()
        self.turn = BRANCO
        self.selected_piece = None
        self.valid_moves_for_selected = []
        self.game_over = False

        self.is_thinking = False
        self.delay = 0.5
        self.stop_execution = False
        
        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(paned, bg="#333")
        paned.add(self.left_frame, width=600)

        self.canvas = tk.Canvas(self.left_frame, width=512, height=512, bg="#333", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.on_board_click)

        self.lbl_status = tk.Label(self.left_frame, text="Sua vez (Brancas)", font=("Arial", 14), bg="#333", fg="white")
        self.lbl_status.pack()

        self.right_frame = tk.Frame(paned, bg="#222")
        paned.add(self.right_frame)

        self.info_frame = tk.Frame(self.right_frame, bg="#444", pady=5)
        self.info_frame.pack(fill=tk.X)
        
        self.var_labels = {}
        for var in ["Profundidade", "Alpha", "Beta", "Avaliação"]:
            frame = tk.Frame(self.info_frame, bg="#444")
            frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            tk.Label(frame, text=var, font=("Consolas", 10, "bold"), bg="#444", fg="#AAA").pack()
            lbl = tk.Label(frame, text="-", font=("Consolas", 14), bg="#444", fg="#FFF")
            lbl.pack()
            self.var_labels[var] = lbl

        self.text_code = tk.Text(self.right_frame, bg=COR_FUNDO_CODIGO, fg=COR_TEXTO_CODIGO, 
                                 font=("Consolas", 12), padx=10, pady=10)
        self.text_code.pack(fill=tk.BOTH, expand=True)
        self.text_code.insert("1.0", MINIMAX_CODE_STR)
        self.text_code.config(state=tk.DISABLED)
        
        self.text_code.tag_config("highlight", background="#444400", foreground="white")
        self.text_code.tag_config("line_num", foreground="#569CD6")
        
        self.text_code.config(state=tk.NORMAL)
        for i in range(1, 25):
            idx = f"{i}.0"
            end_idx = f"{i}.4"
            self.text_code.tag_add("line_num", idx, end_idx)
        self.text_code.config(state=tk.DISABLED)

        self.control_frame = tk.Frame(self.root, bg="#DDD", height=80)
        self.control_frame.pack(fill=tk.X, side=tk.BOTTOM)

        btn_frame = tk.Frame(self.control_frame, bg="#DDD")
        btn_frame.pack(pady=10)

        tk.Label(btn_frame, text="Velocidade:", bg="#DDD").pack(side=tk.LEFT, padx=5)
        self.speed_slider = tk.Scale(btn_frame, from_=1, to=10, orient=tk.HORIZONTAL, bg="#DDD")
        self.speed_slider.set(6)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        tk.Label(btn_frame, text="Profundidade IA:", bg="#DDD").pack(side=tk.LEFT, padx=5)
        self.depth_slider = tk.Scale(btn_frame, from_=1, to=5, orient=tk.HORIZONTAL, bg="#DDD")
        self.depth_slider.set(3)
        self.depth_slider.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(btn_frame, text="Reiniciar Jogo", command=self.reset_game, bg="#ffcccb")
        self.btn_reset.pack(side=tk.LEFT, padx=20)


    def reset_game(self):
        self.stop_execution = True
        self.board = DamasRules.criar_tabuleiro()
        self.turn = BRANCO
        self.selected_piece = None
        self.valid_moves_for_selected = []
        self.is_thinking = False
        self.lbl_status.config(text="Sua vez (Brancas)")
        self.clear_highlight()
        self.update_var_display("-", "-", "-", "-")
        self.draw_board()

    def draw_board(self, ghost_board=None):
        self.canvas.delete("all")
        CELL_SIZE = 64
        board_to_draw = ghost_board if ghost_board else self.board

        for r in range(8):
            for c in range(8):
                x1, y1 = c * CELL_SIZE, (7 - r) * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = COR_CASA_CLARA if (r + c) % 2 == 0 else COR_CASA_ESCURA
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        if not self.is_thinking and not ghost_board:
            for move in self.valid_moves_for_selected:
                end_r, end_c = move['end']
                x1, y1 = end_c * CELL_SIZE, (7 - end_r) * CELL_SIZE
                self.canvas.create_oval(x1+20, y1+20, x1+44, y1+44, fill=COR_DESTINO, outline="")

        for r in range(8):
            for c in range(8):
                piece = board_to_draw[r][c]
                if piece != 0:
                    x1, y1 = c * CELL_SIZE + 10, (7 - r) * CELL_SIZE + 10
                    x2, y2 = x1 + 44, y1 + 44
                    
                    color = COR_PECA_BRANCA if piece > 0 else COR_PECA_VERMELHA
                    outline = "black"
                    width = 1

                    if ghost_board:
                        outline = "yellow"
                        width = 2
                    
                    if abs(piece) == 2:
                        outline = "gold"
                        width = 4

                    self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=width)
                    
                    if abs(piece) == 2:
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        self.canvas.create_text(center_x, center_y, text="D", font=("Arial", 12, "bold"))

        if self.selected_piece and not ghost_board:
            r, c = self.selected_piece
            x1, y1 = c * CELL_SIZE, (7 - r) * CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x1+64, y1+64, outline="blue", width=3)

    def on_board_click(self, event):
        if self.turn != BRANCO or self.is_thinking: return

        c, r = event.x // 64, 7 - (event.y // 64)
        
        move_to_execute = None
        for move in self.valid_moves_for_selected:
            if move['end'] == (r, c):
                move_to_execute = move
                break
        
        if move_to_execute:
            self.execute_human_move(move_to_execute)
            return

        if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] > 0:
            all_valid = DamasRules.get_valid_moves(self.board, BRANCO)
            my_moves = [m for m in all_valid if m['start'] == (r, c)]
            
            if not my_moves and all_valid:
                self.selected_piece = None
                self.valid_moves_for_selected = []
            else:
                self.selected_piece = (r, c)
                self.valid_moves_for_selected = my_moves
            self.draw_board()
        else:
            self.selected_piece = None
            self.valid_moves_for_selected = []
            self.draw_board()

    def execute_human_move(self, move):
        self.board = DamasRules.apply_move(self.board, move)
        self.selected_piece = None
        self.valid_moves_for_selected = []
        self.turn = VERMELHO
        self.draw_board()
        
        self.start_ai_turn()


    def start_ai_turn(self):
        self.is_thinking = True
        self.stop_execution = False
        self.lbl_status.config(text="IA Pensando... (Acompanhe ao lado)")
        self.root.update()

        depth = self.depth_slider.get()
        
        try:
            _, best_move = self.visual_minimax(self.board, depth, True, -math.inf, math.inf)
        except Exception as e:
            print(f"Interrupção ou Erro: {e}")
            best_move = None

        if not self.stop_execution:
            if best_move:
                self.board = DamasRules.apply_move(self.board, best_move)
                self.turn = BRANCO
                self.lbl_status.config(text="Sua vez (Brancas)")
            else:
                messagebox.showinfo("Fim", "A IA não tem movimentos ou desistiu.")
                self.game_over = True
            
            self.clear_highlight()
            self.is_thinking = False
            self.draw_board()
            
            if not DamasRules.get_valid_moves(self.board, BRANCO):
                messagebox.showinfo("Fim de Jogo", "Você perdeu!")

    def visual_hook(self, line_number, local_vars, board_state=None):
        if self.stop_execution:
            raise Exception("Execução Interrompida pelo Usuário")

        self.highlight_line(line_number)

        alpha = local_vars.get('alpha', '?')
        beta = local_vars.get('beta', '?')
        depth = local_vars.get('depth', '?')
        eval_val = local_vars.get('eval', local_vars.get('max_eval', local_vars.get('min_eval', '?')))
        
        def fmt(v):
            if v == math.inf: return "+∞"
            if v == -math.inf: return "-∞"
            if isinstance(v, (int, float)): return f"{v:.0f}"
            return str(v)

        self.update_var_display(depth, fmt(alpha), fmt(beta), fmt(eval_val))

        if board_state:
            self.draw_board(ghost_board=board_state)

        speed = self.speed_slider.get()
        delay = (11 - speed) * 0.1
        
        self.root.update()
        if delay > 0:
            time.sleep(delay)

    def highlight_line(self, line_num):
        self.text_code.config(state=tk.NORMAL)
        self.text_code.tag_remove("highlight", "1.0", "end")
        
        start_index = f"{line_num}.0"
        end_index = f"{line_num+1}.0"
        
        self.text_code.tag_add("highlight", start_index, end_index)
        self.text_code.see(start_index)
        self.text_code.config(state=tk.DISABLED)

    def update_var_display(self, d, a, b, e):
        self.var_labels["Profundidade"].config(text=d)
        self.var_labels["Alpha"].config(text=a)
        self.var_labels["Beta"].config(text=b)
        self.var_labels["Avaliação"].config(text=e)

    def clear_highlight(self):
        self.text_code.config(state=tk.NORMAL)
        self.text_code.tag_remove("highlight", "1.0", "end")
        self.text_code.config(state=tk.DISABLED)

    
    def evaluate_board_logic(self, board):
        score = 0
        PESO_PEDRA = 100
        PESO_DAMA = 300
        PESO_DEFESA_BASE = 20
        
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece == 0: continue
                
                val = PESO_PEDRA
                if abs(piece) == 2: val = PESO_DAMA
                val += BOARD_WEIGHTS[r][c]

                if piece == 1 and r == 0: val += PESO_DEFESA_BASE
                if piece == -1 and r == 7: val += PESO_DEFESA_BASE

                if piece < 0: score += val
                else: score -= val
        return score

    def visual_minimax(self, board, depth, is_max, alpha, beta):
        self.visual_hook(1, locals(), board)
        
        if depth == 0:
            val = self.evaluate_board_logic(board)
            self.visual_hook(2, {**locals(), 'eval': val}, board)
            return val, None

        best_move = None
        
        self.visual_hook(4, locals(), board)

        if is_max:
            max_eval = -math.inf
            self.visual_hook(5, locals(), board)
            
            moves = DamasRules.get_valid_moves(board, VERMELHO)
            
            self.visual_hook(6, locals(), board)
            
            if not moves:
                 return -10000 + depth, None

            for move in moves:
                new_board = DamasRules.apply_move(board, move)
                self.visual_hook(7, locals(), new_board)
                
                eval_val, _ = self.visual_minimax(new_board, depth - 1, False, alpha, beta)
                
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = move
                self.visual_hook(9, locals(), board)
                
                alpha = max(alpha, eval_val)
                self.visual_hook(10, locals(), board)
                
                if beta <= alpha:
                    self.visual_hook(11, locals(), board)
                    break
            
            self.visual_hook(12, locals(), board)
            return max_eval, best_move
        
        else:
            min_eval = math.inf
            self.visual_hook(15, locals(), board)
            
            moves = DamasRules.get_valid_moves(board, BRANCO)
            
            self.visual_hook(16, locals(), board)

            if not moves:
                return 10000 - depth, None

            for move in moves:
                new_board = DamasRules.apply_move(board, move)
                self.visual_hook(17, locals(), new_board)
                
                eval_val, _ = self.visual_minimax(new_board, depth - 1, True, alpha, beta)
                
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                self.visual_hook(19, locals(), board)
                
                beta = min(beta, eval_val)
                self.visual_hook(20, locals(), board)
                
                if beta <= alpha:
                    self.visual_hook(21, locals(), board)
                    break
            
            self.visual_hook(22, locals(), board)
            return min_eval, best_move

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VisualizadorMinimax(root)
        root.mainloop()
    except ImportError:
        print("Erro Crítico: Arquivo 'regras.py' não encontrado no mesmo diretório.")
    except Exception as e:
        print(f"Erro inesperado: {e}")