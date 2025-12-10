import tkinter as tk
from tkinter import messagebox, Menu
from regras import DamasRules, BRANCO, VERMELHO
from ia import DamasAI
import sys

COR_CASA_CLARA = "#F0D9B5"
COR_CASA_ESCURA = "#B58863"
COR_PECA_BRANCA = "#FFFFFF"
COR_PECA_VERMELHA = "#FF4444"
COR_DESTINO = "#AAFF00"

class DamasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Damas AI - Profissional")
        
        # Imagem da Dama
        try:
            self.img_coroa = tk.PhotoImage(file="coroa.png")
        except Exception:
            print("Imagem 'coroa.png' não encontrada. Usando 'D' como fallback.")
            self.img_coroa = None

        # Criação do Menu
        self.create_menu()

        self.ai = DamasAI(depth=4)
        self.reset_game()

        self.canvas = tk.Canvas(root, width=512, height=512)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.status_label = tk.Label(root, text="Sua vez (Brancas)", font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        self.draw_board()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opções", menu=file_menu)
        file_menu.add_command(label="Jogar Novamente", command=self.reset_game)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

    def reset_game(self):
        """Reinicia todas as variáveis de estado do jogo."""
        self.board = DamasRules.criar_tabuleiro()
        self.turn = BRANCO
        self.selected_piece = None
        self.valid_moves_for_selected = []
        
        if hasattr(self, 'status_label'):
            self.status_label.config(text="Sua vez (Brancas)")
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        CELL_SIZE = 64
        
        for r in range(8):
            for c in range(8):
                x1, y1 = c * CELL_SIZE, (7 - r) * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = COR_CASA_CLARA if (r + c) % 2 == 0 else COR_CASA_ESCURA
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        for move in self.valid_moves_for_selected:
            end_r, end_c = move['end']
            x1, y1 = end_c * CELL_SIZE, (7 - end_r) * CELL_SIZE
            self.canvas.create_oval(x1+20, y1+20, x1+44, y1+44, fill=COR_DESTINO, outline="")

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != 0:
                    x1, y1 = c * CELL_SIZE + 10, (7 - r) * CELL_SIZE + 10
                    x2, y2 = x1 + 44, y1 + 44
                    color = COR_PECA_BRANCA if piece > 0 else COR_PECA_VERMELHA
                    outline = "gold" if abs(piece) == 2 else "black"
                    width = 4 if abs(piece) == 2 else 1
                    
                    self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=width)
                    
                    # Dama
                    if abs(piece) == 2:
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        
                        if self.img_coroa:
                            self.canvas.create_image(center_x, center_y, image=self.img_coroa)
                        else:
                            self.canvas.create_text(center_x, center_y, text="D", font=("Arial", 12, "bold"))
        
        if self.selected_piece:
            r, c = self.selected_piece
            x1, y1 = c * CELL_SIZE, (7 - r) * CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x1+64, y1+64, outline="blue", width=3)

    def on_click(self, event):
        if self.turn != BRANCO: return 

        c, r = event.x // 64, 7 - (event.y // 64)
        
        move_to_execute = None
        for move in self.valid_moves_for_selected:
            if move['end'] == (r, c):
                move_to_execute = move
                break
        
        if move_to_execute:
            self.execute_move(move_to_execute)
            return

        if self.board[r][c] > 0: 
            all_valid_moves = DamasRules.get_valid_moves(self.board, self.turn)
            my_moves = [m for m in all_valid_moves if m['start'] == (r, c)]
            
            if not my_moves and all_valid_moves:
                self.status_label.config(text="Atenção: Lei da Maioria ativa!")
            else:
                self.status_label.config(text="Sua vez (Brancas)")
            
            self.selected_piece = (r, c)
            self.valid_moves_for_selected = my_moves
            self.draw_board()
        else:
            self.selected_piece = None
            self.valid_moves_for_selected = []
            self.draw_board()

    def execute_move(self, move):
        self.board = DamasRules.apply_move(self.board, move)
        self.selected_piece = None
        self.valid_moves_for_selected = []
        self.turn = VERMELHO 
        self.draw_board()
        self.status_label.config(text="IA Pensando...")
        self.root.update()
        
        self.root.after(200, self.ai_turn)

    def ai_turn(self):
        best_move = self.ai.get_best_move(self.board, VERMELHO)
        
        if best_move:
            self.board = DamasRules.apply_move(self.board, best_move)
            self.turn = BRANCO
            self.status_label.config(text="Sua vez (Brancas)")
            self.draw_board()
        else:
            if messagebox.askyesno("Fim de Jogo", "IA não tem movimentos. Você venceu!\nJogar novamente?"):
                self.reset_game()
            else:
                self.root.quit()
                return

        if not DamasRules.get_valid_moves(self.board, BRANCO):
             if messagebox.askyesno("Fim de Jogo", "Você não tem movimentos. A IA venceu!\nJogar novamente?"):
                 self.reset_game()
             else:
                 self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DamasApp(root)
    root.mainloop()
