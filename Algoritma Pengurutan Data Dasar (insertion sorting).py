import tkinter as tk
from tkinter import END, messagebox
from random import shuffle

# ===============================================
# 1. KONFIGURASI DAN DATA GAME
# ===============================================

# List of integers dari 1 hingga 9
INITIAL_NUMBERS = [i for i in range(1, 10)]
shuffle(INITIAL_NUMBERS) # Acak data awal

current_data = INITIAL_NUMBERS[:] # Salinan data yang akan diubah
sorted_boundary = 1 # Batas antara bagian terurut dan belum terurut (mulai dari elemen kedua)
key_value = None
current_data_temp = None # Data array sementara untuk visualisasi shift

# --- 2. LOGIKA UTAMA INSERTION SORT ---

def get_next_key():
    """Mengambil Key berikutnya dari bagian belum terurut."""
    global key_value, current_data_temp
    
    if sorted_boundary >= len(current_data):
        return False # Game Selesai
    
    key_value = current_data[sorted_boundary]
    
    # Inisialisasi data sementara, menempatkan KEY di 'luar' array untuk disisipkan
    current_data_temp = current_data[:sorted_boundary] + [key_value] + current_data[sorted_boundary + 1:]

    return True

def attempt_shift():
    """Percobaan pemain untuk menggeser elemen ke kanan."""
    global current_data_temp
    
    # Posisi KEY yang 'kosong' akibat pergeseran
    key_current_pos = current_data_temp.index(key_value)
    
    if key_current_pos == 0:
        messagebox.showwarning("Salah!", "KEY sudah di posisi paling kiri (Indeks 0). Tidak bisa digeser lagi.")
        return False
        
    # Elemen di sebelah kiri KEY
    left_element = current_data_temp[key_current_pos - 1]
    
    # Aturan Insertion Sort: Geser jika elemen di sebelah kiri LEBIH BESAR dari KEY
    if left_element > key_value:
        # Lakukan Penukaran (Simulasi Geser)
        current_data_temp[key_current_pos], current_data_temp[key_current_pos - 1] = \
            current_data_temp[key_current_pos - 1], current_data_temp[key_current_pos]
        
        update_display(f"✅ BENAR! {left_element} > {key_value}. Geser ke kanan.", "green")
        return True
    else:
        messagebox.showerror("Salah!", f"❌ SALAH! KEY {key_value} sudah lebih besar dari elemen di kirinya ({left_element}). Seharusnya di-INSERT.")
        return False

def attempt_insert():
    """Percobaan pemain untuk menyisipkan KEY."""
    global current_data, sorted_boundary
    
    key_current_pos = current_data_temp.index(key_value)
    
    # Periksa apakah penyisipan sudah di posisi yang benar (elemen di kiri <= KEY)
    if key_current_pos == 0 or current_data_temp[key_current_pos - 1] <= key_value:
        
        # Lakukan Penyisipan Akhir ke data permanen
        current_data = current_data_temp[:]
        
        # Pindah ke iterasi/pass berikutnya
        sorted_boundary += 1
        
        update_display(f"🎉 SUKSES! KEY {key_value} disisipkan di Indeks {key_current_pos}.", "blue")
        
        # Mulai putaran baru
        start_round()
        return True
    else:
        messagebox.showerror("Salah!", f"❌ SALAH! Elemen di kiri ({current_data_temp[key_current_pos - 1]}) masih lebih besar dari KEY {key_value}. Harus di-SHIFT.")
        return False

# --- 3. LOGIKA VISUALISASI ---

def update_display(message, color="black"):
    """Memperbarui visualisasi daftar data dan status."""
    
    listbox_data.delete(0, END)
    
    if sorted_boundary >= len(current_data):
        listbox_data.insert(END, " ".join([f"[{str(x)}]" for x in current_data]))
        label_status.config(text=f"!!! GAME SELESAI !!! Data Terurut: {current_data}", fg="purple")
        button_shift.config(state=tk.DISABLED)
        button_insert.config(state=tk.DISABLED)
        button_reset.config(state=tk.NORMAL)
        return
        
    display_list = []
    key_current_pos = current_data_temp.index(key_value)
    
    for idx, item in enumerate(current_data_temp):
        item_str = str(item)
        
        if idx < sorted_boundary and idx != key_current_pos:
            # Bagian Terurut (sudah benar)
            item_str = f"[{item_str}]" 
        elif idx == key_current_pos:
            # Key yang sedang digeser/diproses
            item_str = f"|{item_str}|" 
        elif idx > sorted_boundary and item != key_value:
            # Bagian Belum Terurut
            item_str = f"{item_str}" 
        
        display_list.append(item_str)

    # Memasukkan pemisah visual
    display_list.insert(sorted_boundary, "**|**")
        
    listbox_data.insert(END, " ".join(display_list))
    
    label_status.config(text=message, fg=color)
    label_key.config(text=f"KEY (Kartu Baru): {key_value}")


def start_round():
    """Memulai putaran baru (Pass Insertion Sort)."""
    if get_next_key():
        update_display(f"ROUND {sorted_boundary}: Ambil KEY baru: {key_value}. Posisikan!", "darkorange")
    else:
        update_display("", "black") # Game Selesai akan dihandle di update_display


def reset_game():
    """Mengatur ulang game dengan data baru."""
    global current_data, sorted_boundary, key_value
    shuffle(INITIAL_NUMBERS)
    current_data = INITIAL_NUMBERS[:]
    sorted_boundary = 1
    key_value = None
    
    button_shift.config(state=tk.NORMAL)
    button_insert.config(state=tk.NORMAL)
    button_reset.config(state=tk.DISABLED)
    
    start_round()

# ===============================================
# 4. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title("Insertion Sort Game: Susun Kartu Angka")
root.geometry("750x450")
root.configure(bg="#F0FFFF")

## 🏷️ Judul Game
tk.Label(root, text="🃏 INSERTION SORT: PERMAINAN MENYUSUN KARTU", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Aturan: Pindahkan KEY (|Angka|) ke posisi yang benar pada bagian terurut ([Angka]) di sebelah kiri.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
tk.Label(root, text="Jika elemen di kiri > KEY, tekan SHIFT. Jika elemen di kiri <= KEY, tekan INSERT.", 
         bg="#F0FFFF", fg="red", font=("Arial", 10, "italic")).pack(pady=2)

# --- Visualisasi Data ---
tk.Label(root, text="STATUS KARTU: [TERURUT] |KEY| ... | BELUM TERURUT ...", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

listbox_data = tk.Listbox(root, height=1, width=50, font=("Courier", 24), justify='center', bg="#FFFFFF")
listbox_data.pack(padx=20, pady=10)

# --- KEY Information ---
label_key = tk.Label(root, text="KEY (Kartu Baru): -", 
                     bg="#E0FFFF", fg="#004D40", font=("Arial", 12, "bold"))
label_key.pack(pady=10)


# Label Status
label_status = tk.Label(root, text="Klik 'Mulai Putaran' untuk memulai game.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Tombol Operasi ---
frame_tombol = tk.Frame(root, bg="#F0FFFF")
frame_tombol.pack(pady=10)

button_shift = tk.Button(frame_tombol, text="1. SHIFT (Geser Elemen Kiri ke Kanan)", command=attempt_shift, 
          bg="#FF8C00", fg="white", font=("Arial", 10, "bold"))
button_shift.pack(side=tk.LEFT, padx=10)
          
button_insert = tk.Button(frame_tombol, text="2. INSERT (Sisipkan KEY di Sini)", command=attempt_insert, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
button_insert.pack(side=tk.LEFT, padx=10)

button_reset = tk.Button(frame_tombol, text="MULAI ULANG", command=reset_game, 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold"))
button_reset.pack(side=tk.LEFT, padx=20)
button_reset.config(state=tk.DISABLED) # Mulai dengan disable

# Inisiasi Game
start_round()

root.mainloop()