import tkinter as tk
import random
import time

# =================================================================
# 1. PENGATURAN AWAL (VARIABEL GLOBAL & TEMA)
# =================================================================

# --- Warna dan Tema ---
COLOR_BLUE = "#3498DB"          
COLOR_YELLOW = "#F1C40F"        
COLOR_BACKGROUND = "#2C3E50"    
COLOR_LIGHT_GRAY = "#34495E"    
COLOR_HIGHLIGHT = "#1ABC9C"     

# --- Status Permainan ---
playerX = "X"
playerO = "O"
curr_player = playerX       
score_x = 0                 
score_o = 0                 
turns = 0                   
game_over = False           
GAME_MODE = "AI vs Player"  
AI_DIFFICULTY = "Sulit"     

# --- Objek Utama Tkinter (Jendela Aplikasi) ---
window = tk.Tk()

# --- Frame (Bingkai) Utama ---
cover_frame = None          
game_frame = None           

# --- Struktur Data ---
board = [[None, None, None], [None, None, None], [None, None, None]] 
mode_var = tk.StringVar(window) 
diff_var = tk.StringVar(window) 

# --- Referensi Elemen UI ---
label = None                
score_label = None          
diff_label_game = None      
diff_menu_game = None       
diff_label_cover = None     
diff_menu_cover = None      

# =================================================================
# 2. FUNGSI LOGIKA PERMAINAN (AI dan Pemenang)
# =================================================================

def update_score_label():
    global score_label
    if score_label:
        score_label.config(text=f"Skor: X ({score_x}) | O ({score_o})")

def new_game():
    global turns, game_over, curr_player
    turns = 0
    game_over = False
    curr_player = playerX
    
    label.config(text=f"Giliran {curr_player}", foreground="white", background=COLOR_BACKGROUND) 
    
    for row in range(3):
        for column in range(3):
            board[row][column].config(text="", 
                                      foreground=COLOR_BLUE, 
                                      background=COLOR_BACKGROUND,
                                      activebackground=COLOR_LIGHT_GRAY,
                                      state=tk.NORMAL) 
    update_score_label() 

def check_simulated_win(r, c):
    current_player_symbol = board[r][c]["text"]
    
    if all(board[r][col]["text"] == current_player_symbol for col in range(3)): return True
    if all(board[row][c]["text"] == current_player_symbol for row in range(3)): return True
    if r == c and all(board[i][i]["text"] == current_player_symbol for i in range(3)): return True
    if r + c == 2 and all(board[i][2-i]["text"] == current_player_symbol for i in range(3)): return True
    return False

def check_winner():
    global turns, game_over
    turns += 1

    def handle_winner(winner_tile, row_indices, col_indices):
        global game_over, score_x, score_o
        
        if winner_tile == playerX: score_x += 1
        else: score_o += 1
        update_score_label() 
        
        label.config(text=f"Pemenangnya adalah {winner_tile}!", foreground=COLOR_YELLOW, background=COLOR_LIGHT_GRAY)
        
        for r, c in zip(row_indices, col_indices):
            board[r][c].config(foreground=COLOR_YELLOW, background=COLOR_LIGHT_GRAY, state=tk.DISABLED)
        for row in range(3):
            for col in range(3):
                if board[row][col]["text"] == "":
                    board[row][col].config(state=tk.DISABLED)
        
        game_over = True
        return True
    
    for row in range(3):
        first_tile = board[row][0]["text"]
        if (first_tile == board[row][1]["text"] and first_tile == board[row][2]["text"] and first_tile != ""): return handle_winner(first_tile, [row, row, row], [0, 1, 2])
    for column in range(3):
        first_tile = board[0][column]["text"]
        if (first_tile == board[1][column]["text"] and first_tile == board[2][column]["text"] and first_tile != ""): return handle_winner(first_tile, [0, 1, 2], [column, column, column])
    first_tile = board[0][0]["text"]
    if (first_tile == board[1][1]["text"] and first_tile == board[2][2]["text"] and first_tile != ""): return handle_winner(first_tile, [0, 1, 2], [0, 1, 2])
    first_tile = board[0][2]["text"]
    if (first_tile == board[1][1]["text"] and first_tile == board[2][0]["text"] and first_tile != ""): return handle_winner(first_tile, [0, 1, 2], [2, 1, 0])


    if turns == 9:
        label.config(text="Hasilnya Seri! 🤝", foreground=COLOR_YELLOW, background=COLOR_LIGHT_GRAY)
        game_over = True
        return True
    return False

def set_tile(row, column, is_ai_move=False):
    global curr_player, game_over
    
    if board[row][column]["text"] != "" or game_over: return
    if not is_ai_move and curr_player == playerO and GAME_MODE == "AI vs Player": return

    color = COLOR_YELLOW if curr_player == playerX else COLOR_BLUE
    board[row][column].config(text=curr_player, foreground=color) 
    
    check_winner()

    if not game_over:
        curr_player = playerX if curr_player == playerO else playerO
        label.config(text=f"Giliran {curr_player}")
        
        if GAME_MODE == "AI vs Player" and curr_player == playerO:
            window.after(500, ai_turn) 

def get_empty_tiles():
    empty_tiles = []
    for r in range(3):
        for c in range(3):
            if board[r][c]["text"] == "": empty_tiles.append((r, c))
    return empty_tiles

def find_critical_move(player):
    empty_tiles = get_empty_tiles()
    
    for r, c in empty_tiles:
        board[r][c]["text"] = player 
        winner = check_simulated_win(r, c)
        board[r][c]["text"] = ""     
        if winner: return r, c       
    return None

def ai_move_easy():
    empty_tiles = get_empty_tiles()
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        set_tile(r, c, is_ai_move=True)

def ai_move_medium():
    move = find_critical_move(playerO)
    if move: r, c = move; set_tile(r, c, is_ai_move=True); return
    
    if random.random() < 0.5:
        move = find_critical_move(playerX)
        if move: r, c = move; set_tile(r, c, is_ai_move=True); return
        
    ai_move_easy() 

def ai_move_hard():
    move = find_critical_move(playerO)
    if move: r, c = move; set_tile(r, c, is_ai_move=True); return

    move = find_critical_move(playerX)
    if move: r, c = move; set_tile(r, c, is_ai_move=True); return

    if board[1][1]["text"] == "": set_tile(1, 1, is_ai_move=True); return

    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]; random.shuffle(corners)
    for r, c in corners:
        if board[r][c]["text"] == "": set_tile(r, c, is_ai_move=True); return
        
    ai_move_easy()

def ai_turn():
    global AI_DIFFICULTY
    if AI_DIFFICULTY == "Mudah": ai_move_easy()
    elif AI_DIFFICULTY == "Sedang": ai_move_medium()
    elif AI_DIFFICULTY == "Sulit": ai_move_hard()


# =================================================================
# 3. FUNGSI KONTROL TAMPILAN (Mengganti Halaman/Frame)
# =================================================================

def show_game_board():
    """Menampilkan papan permainan dan menyembunyikan halaman sampul."""
    global GAME_MODE, AI_DIFFICULTY
    if cover_frame:
        cover_frame.pack_forget() 
    
    # Menggunakan grid di window utama agar game_frame bisa meregang
    game_frame.grid(row=0, column=0, sticky="nsew")
    
    GAME_MODE = mode_var.get()
    AI_DIFFICULTY = diff_var.get()
    
    if GAME_MODE == "AI vs Player":
        diff_label_game.pack(side=tk.LEFT, padx=(0, 5))
        diff_menu_game.pack(side=tk.LEFT)
    else:
        diff_label_game.pack_forget()
        diff_menu_game.pack_forget()

    new_game()
    window.title("Tic Tac Toe | Bermain") 
    center_window()

def show_cover_page():
    """Menampilkan halaman sampul dan menyembunyikan papan permainan."""
    if game_frame:
        game_frame.grid_forget()
    cover_frame.pack(expand=True)
    window.title("Tic Tac Toe | Halaman Sampul") 
    center_window()
    
def start_game():
    show_game_board()

def set_game_mode_menu(selection):
    if selection == "AI vs Player":
        diff_label_cover.grid(row=3, column=0, sticky="w", pady=(10, 0))
        diff_menu_cover.grid(row=3, column=1, sticky="w", pady=(10, 0))
    else:
        diff_label_cover.grid_remove()
        diff_menu_cover.grid_remove()

def set_game_mode_board(selection):
    global GAME_MODE
    GAME_MODE = selection
    if GAME_MODE == "AI vs Player":
        diff_label_game.pack(side=tk.LEFT, padx=(0, 5))
        diff_menu_game.pack(side=tk.LEFT)
    else:
        diff_label_game.pack_forget()
        diff_menu_game.pack_forget()
    new_game()

def set_difficulty(selection):
    global AI_DIFFICULTY
    AI_DIFFICULTY = selection
    new_game()

def center_window():
    """Menengahkan jendela aplikasi di tengah layar."""
    window.update_idletasks() 
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() 
    window_x = int(screen_width / 2 - window_width / 2)
    window_y = int(screen_height / 2 - window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')


# =================================================================
# 4. KONFIGURASI UI (MEMBANGUN FRAME)
# =================================================================

def build_ui():
    """Fungsi utama untuk membuat semua elemen tampilan (UI)."""
    global cover_frame, game_frame, label, score_label, diff_label_game, diff_menu_game, diff_label_cover, diff_menu_cover
    
    # Kunci: Kotak Latar (Jendela) Dibuat Persegi
    window.geometry("500x500") 
    
    window.config(bg=COLOR_BACKGROUND) 
    window.resizable(False, False) 
    
    # Memastikan game_frame dapat meregang di window utama
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    # --- FRAME 1: HALAMAN SAMPUL ---
    cover_frame = tk.Frame(window, bg=COLOR_BACKGROUND, padx=30, pady=30) 

    tk.Label(cover_frame, text="✨ Tic Tac Toe ✨", font=("Consolas", 32, "bold"), fg=COLOR_YELLOW, bg=COLOR_BACKGROUND).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tk.Label(cover_frame, text="Pilih Mode:", font=("Consolas", 14), fg="white", bg=COLOR_BACKGROUND).grid(row=1, column=0, sticky="w", pady=(10, 0))

    mode_options = ["AI vs Player", "Player vs Player"]
    mode_var.set(GAME_MODE)
    mode_menu_cover = tk.OptionMenu(cover_frame, mode_var, *mode_options, command=set_game_mode_menu)
    mode_menu_cover.config(bg=COLOR_LIGHT_GRAY, fg="white", activebackground=COLOR_BLUE, borderwidth=0, relief=tk.FLAT, highlightthickness=0, font=("Consolas", 12))
    mode_menu_cover.grid(row=1, column=1, sticky="w", pady=(10, 0))

    diff_options = ["Mudah", "Sedang", "Sulit"]
    diff_var.set(AI_DIFFICULTY) 
    diff_label_cover = tk.Label(cover_frame, text="Tingkat Kesulitan:", font=("Consolas", 14), fg="white", bg=COLOR_BACKGROUND)
    diff_menu_cover = tk.OptionMenu(cover_frame, diff_var, *diff_options) 
    diff_menu_cover.config(bg=COLOR_LIGHT_GRAY, fg="white", activebackground=COLOR_BLUE, borderwidth=0, relief=tk.FLAT, highlightthickness=0, font=("Consolas", 12))

    set_game_mode_menu(GAME_MODE)

    tk.Button(cover_frame, 
              text="▶ MULAI PERMAINAN", 
              font=("Consolas", 18, "bold"), 
              bg=COLOR_HIGHLIGHT, 
              fg=COLOR_BACKGROUND, 
              activebackground=COLOR_LIGHT_GRAY,
              relief=tk.FLAT,
              command=start_game).grid(row=4, column=0, columnspan=2, pady=(30, 0), sticky="we")


    # --- FRAME 2: PAPAN PERMAINAN ---
    game_frame = tk.Frame(window, bg=COLOR_BACKGROUND, padx=10, pady=10) 

    # Kunci: Konfigurasi agar Semua baris dan kolom yang berisi kotak game meregang sama rata (weight=1)
    for i in range(3):
        game_frame.grid_columnconfigure(i, weight=1)
        # Baris papan game dimulai dari row 3 (0:Label, 1:Skor, 2:Kontrol)
        game_frame.grid_rowconfigure(i+3, weight=1) 
    
    # Baris 0: Label Status
    label = tk.Label(game_frame, text=f"Giliran {curr_player}", font=("Consolas", 16, "bold"), background=COLOR_BACKGROUND, foreground="white", pady=2) 
    label.grid(row=0, column=0, columnspan=3, sticky="we") 

    # Baris 1: Label Skor
    score_label = tk.Label(game_frame, text=f"Skor: X ({score_x}) | O ({score_o})", font=("Consolas", 10), background=COLOR_BACKGROUND, foreground="white", pady=2)
    score_label.grid(row=1, column=0, columnspan=3, sticky="we") 

    # BARIS 2: KONTROL MODE DAN KESULITAN 
    
    # Frame Kontrol Mode (KIRI)
    mode_control_frame = tk.Frame(game_frame, bg=COLOR_BACKGROUND)
    mode_control_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=5, padx=5)

    tk.Label(mode_control_frame, text="Mode:", bg=COLOR_BACKGROUND, fg="white", font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=(0, 5))
    mode_menu_game = tk.OptionMenu(mode_control_frame, mode_var, *mode_options, command=set_game_mode_board)
    mode_menu_game.config(bg=COLOR_LIGHT_GRAY, fg="white", activebackground=COLOR_BLUE, borderwidth=0, relief=tk.FLAT, highlightthickness=0, font=("Consolas", 10))
    mode_menu_game.pack(side=tk.LEFT, padx=(0, 0))

    # Frame Kontrol Kesulitan (KANAN)
    diff_control_frame = tk.Frame(game_frame, bg=COLOR_BACKGROUND)
    diff_control_frame.grid(row=2, column=2, sticky="e", pady=5, padx=5)

    diff_label_game = tk.Label(diff_control_frame, text="Kesulitan:", bg=COLOR_BACKGROUND, fg="white", font=("Consolas", 10, "bold"))
    diff_menu_game = tk.OptionMenu(diff_control_frame, diff_var, *diff_options, command=set_difficulty)
    diff_menu_game.config(bg=COLOR_LIGHT_GRAY, fg="white", activebackground=COLOR_BLUE, borderwidth=0, relief=tk.FLAT, highlightthickness=0, font=("Consolas", 10))
    
    diff_label_game.pack(side=tk.LEFT, padx=(0, 5))
    diff_menu_game.pack(side=tk.LEFT)
    

    # Loop untuk membuat 9 tombol papan (Kotak Game Seragam)
    for row in range(3):
        for column in range(3):
            btn = tk.Button(game_frame, 
                            text="", 
                            font=("Consolas", 50, "bold"), # Ukuran font yang besar membantu mengisi ruang
                            background=COLOR_BACKGROUND, 
                            foreground=COLOR_BLUE, 
                            activebackground=COLOR_LIGHT_GRAY, 
                            relief=tk.RIDGE, borderwidth=3,          
                            highlightbackground=COLOR_BLUE, highlightcolor=COLOR_BLUE,
                            # PENTING: Menghapus width dan height agar grid(sticky="nsew") mengontrol ukuran
                            command=lambda r=row, c=column: set_tile(r, c)) 
            
            board[row][column] = btn 
            # sticky="nsew" memastikan kotak mengisi ruang grid secara merata dan seragam.
            board[row][column].grid(row=row+3, column=column, padx=0, pady=0, sticky="nsew") 

    # Baris 6: Tombol Restart dan Menu Utama
    button_frame_bottom = tk.Frame(game_frame, bg=COLOR_BACKGROUND)
    button_frame_bottom.grid(row=6, column=0, columnspan=3, sticky="we", pady=(5, 0))

    tk.Button(button_frame_bottom, 
              text="ULANG 🔄", 
              font=("Consolas", 12, "bold"), 
              background=COLOR_LIGHT_GRAY, fg="white", 
              activebackground=COLOR_BLUE, relief=tk.FLAT,
              command=new_game).pack(side=tk.LEFT, expand=True, fill='x')

    tk.Button(button_frame_bottom, 
              text="MENU UTAMA 🏠", 
              font=("Consolas", 12, "bold"), 
              background=COLOR_LIGHT_GRAY, fg="white", 
              activebackground=COLOR_BLUE, relief=tk.FLAT,
              command=show_cover_page).pack(side=tk.LEFT, expand=True, fill='x', padx=(5, 0))


# =================================================================
# 5. EKSEKUSI UTAMA
# =================================================================

build_ui()          
show_cover_page()   
window.mainloop()