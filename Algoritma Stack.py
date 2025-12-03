import tkinter as tk
from tkinter import END
from tkinter import messagebox
from collections import deque

# ===============================================
# 1. IMPLEMENTASI STACK (Tumpukan Kotak)
# ===============================================

class BoxStack:
    def __init__(self):
        # Menggunakan deque sebagai wadah Stack untuk efisiensi
        self._items = deque() 

    def is_empty(self):
        return not self._items

    def push(self, item):
        """PUSH: Menambahkan kotak ke puncak (ujung kanan deque)."""
        self._items.append(item)
        
    def pop(self, error_message="Stack kosong"):
        """POP: Mengambil kotak dari puncak (ujung kanan deque)."""
        if self.is_empty():
            return None 
        return self._items.pop()
        
# Inisialisasi Stack
tumpukan = BoxStack()

# --- 2. LOGIKA GUI (Handler Tombol) ---

def tampilkan_stack(pesan=""):
    """Memperbarui visualisasi Stack."""
    
    # 1. Hapus isi visualisasi lama
    stack_list_display.delete(0, END)

    if tumpukan.is_empty():
        stack_list_display.insert(END, "--- DASAR (BASE) ---")
        stack_list_display.insert(END, "Tumpukan Kotak Kosong")
    else:
        stack_list_display.insert(END, "--- DASAR (BASE) ---")
        items = list(tumpukan._items)
        
        # Tampilkan item dari dasar ke puncak
        for i, item in enumerate(items):
            label = f"[{item}]"
            # Tandai Puncak (TOP)
            if i == len(items) - 1:
                label += " <- PUNCAK (TOP/Terakhir Masuk)"
                stack_list_display.insert(END, label)
            else:
                stack_list_display.insert(END, label)

    label_status.config(text=pesan, fg="#004D40" if "✅" in pesan else "red")


def handle_push():
    """Operasi PUSH: Menambahkan kotak ke Puncak."""
    nama_kotak = entry_input.get().strip()
    if not nama_kotak:
        tampilkan_stack("❌ Masukkan nama kotak (misal: Kotak A).")
        return

    # Operasi PUSH
    tumpukan.push(nama_kotak)
    
    pesan = f"✅ PUSH: Kotak '{nama_kotak}' diletakkan di Puncak Tumpukan."
    entry_input.delete(0, END)
    tampilkan_stack(pesan)

def handle_pop():
    """Operasi POP: Mengambil kotak dari Puncak."""
    
    # Operasi POP
    kotak_diambil = tumpukan.pop()
    
    if kotak_diambil is None:
        pesan = "❌ POP GAGAL! Tumpukan kosong."
    else:
        pesan = f"✅ POP: Kotak '{kotak_diambil}' diambil dari Puncak (LIFO)."
    
    tampilkan_stack(pesan)
    

# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Algoritma Stack Sederhana - Tumpukan Kotak") 
root.geometry("600x650") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"STACK SEDERHANA: LIFO (Last In, First Out)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Masukkan nama kotak, lalu PUSH dan POP. Perhatikan kotak yang terakhir masuk adalah yang pertama keluar.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)

# --- Frame Input & Tombol ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Nama Kotak:", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
entry_input = tk.Entry(frame_input, width=30)
entry_input.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Tombol Operasi Utama
frame_tombol = tk.Frame(frame_input, bg="#E0FFFF")
frame_tombol.grid(row=1, column=0, columnspan=3, pady=10)

# 1. PUSH
tk.Button(frame_tombol, text="PUSH (Tambahkan Kotak)", command=handle_push, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
          
# 2. POP
tk.Button(frame_tombol, text="POP (Ambil Kotak Terakhir)", command=handle_pop, 
          bg="#B22222", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

# Label Status
label_status = tk.Label(root, text="Stack siap.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=5)

# --- Visualisasi Stack ---
tk.Label(root, text="VISUALISASI TUMPUKAN (STACK):", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=10)

# Listbox untuk menampilkan isi Stack (vertikal)
stack_list_display = tk.Listbox(root, height=15, width=40, font=("Courier", 12), justify='center', bg="#FFFFFF")
stack_list_display.pack(padx=20, pady=10)

tampilkan_stack("Stack berhasil diinisialisasi.")
root.mainloop()