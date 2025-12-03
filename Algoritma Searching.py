import tkinter as tk
from tkinter import END
from operator import itemgetter 
from tkinter import font as tkfont

# ===============================================
# 1. DATA (Wajib Terurut berdasarkan 'title')
# ===============================================

DATA_RAK_BUKU_UNSORTED = [
    {'title': 'Sejarah Kuno', 'shelf': 'A05'},
    {'title': 'Algoritma dan Struktur Data', 'shelf': 'C12'},
    {'title': 'Filsafat Timur', 'shelf': 'B01'},
    {'title': 'Pemrograman Python Lanjut', 'shelf': 'C15'},
    {'title': 'Ekonomi Mikro', 'shelf': 'A01'},
    {'title': 'Matematika Diskrit', 'shelf': 'C08'},
    {'title': 'Statistik Lanjutan', 'shelf': 'D03'},
    {'title': 'Desain Grafis Dasar', 'shelf': 'B10'},
]

# Data Wajib Terurut berdasarkan 'title'
DATA_RAK_BUKU = sorted(DATA_RAK_BUKU_UNSORTED, key=itemgetter('title'))


# ===============================================
# 2. ALGORITMA TERNARY SEARCH
# ===============================================

def ternary_search_book(data_list, target_title):
    """Mencari buku menggunakan Ternary Search."""
    low = 0
    high = len(data_list) - 1
    steps = []
    target_title_lower = target_title.strip().lower() 
    
    while low <= high:
        # Menentukan dua titik tengah (mid1 dan mid2)
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        guess1 = data_list[mid1]['title'].lower()
        guess2 = data_list[mid2]['title'].lower()

        # Catat langkah
        steps.append({
            "low": low, "high": high, "mid1": mid1, "mid2": mid2,
            "guess1": data_list[mid1]['title'],
            "guess2": data_list[mid2]['title']
        })

        if guess1 == target_title_lower:
            return data_list[mid1]['shelf'], steps, True
        if guess2 == target_title_lower:
            return data_list[mid2]['shelf'], steps, True

        # Membandingkan dan memotong ruang pencarian
        if target_title_lower < guess1:
            # Target ada di segmen KIRI (S1: low hingga mid1-1)
            high = mid1 - 1
        elif target_title_lower > guess2:
            # Target ada di segmen KANAN (S3: mid2+1 hingga high)
            low = mid2 + 1
        else:
            # Target ada di segmen TENGAH (S2: mid1+1 hingga mid2-1)
            low = mid1 + 1
            high = mid2 - 1
            
    return None, steps, False

# --- 3. LOGIKA GUI (Handler Tombol) ---

def handle_search():
    """Menangani tombol Pencarian Buku."""
    target_input = entry_target.get().strip()
    
    if not target_input:
        update_output("❌ Masukkan Judul Buku yang ingin dicari.", "red")
        return
    
    # Panggil Ternary Search
    shelf_number, steps, found = ternary_search_book(DATA_RAK_BUKU, target_input)
    
    # Tampilkan Hasil dan Langkah
    update_result_display(shelf_number, target_input, steps, found)

def update_output(message, color="black"):
    """Update label status."""
    label_status.config(text=message, fg=color)

def update_result_display(shelf_number, target, steps, found):
    """Menampilkan langkah dan hasil pencarian."""
    
    listbox_steps.delete(0, END)
    
    if not found:
        message = f"❌ Gagal: Judul '{target}' tidak ditemukan setelah {len(steps)} langkah pembagian terner."
        update_output(message, "red")
        
    else:
        message = f"✅ BERHASIL: '{target}' ditemukan di Rak {shelf_number} hanya dalam {len(steps)} langkah pembagian terner."
        update_output(message, "green")
    
    # Tampilkan Langkah-Langkah Pencarian
    listbox_steps.insert(END, f"DETAIL LANGKAH PENCARIAN TERNER UNTUK '{target}':")
    
    for i, step in enumerate(steps):
        
        # Tentukan arah
        if step['guess1'].lower() == target.lower():
            status = "Ditemukan di Mid1"
        elif step['guess2'].lower() == target.lower():
            status = "Ditemukan di Mid2"
        elif target.lower() < step['guess1'].lower():
            status = "Lanjut ke Segmen Kiri (S1)"
        elif target.lower() > step['guess2'].lower():
            status = "Lanjut ke Segmen Kanan (S3)"
        else:
            status = "Lanjut ke Segmen Tengah (S2)"

        # Tampilkan rentang pencarian yang aktif
        range_display = f"[ {step['low']}...{step['high']} ]"
        
        step_str = (f"Lgkh {i+1} {range_display} | MID1={step['mid1']} (Tebakan: '{step['guess1']}') | "
                    f"MID2={step['mid2']} (Tebakan: '{step['guess2']}'). Arah: {status}")
        
        listbox_steps.insert(END, step_str)

    listbox_steps.insert(END, "-------------------------------------------------------------")
    
    if found:
        listbox_steps.insert(END, f"HASIL AKHIR: Ditemukan di Rak {shelf_number}")

def setup_book_list_display():
    """Menampilkan daftar buku yang tersedia di awal."""
    listbox_books.delete(0, END)
    listbox_books.insert(END, "--- DAFTAR BUKU TERSEDIA (Wajib Terurut Sesuai Judul) ---")
    listbox_books.insert(END, "-------------------------------------------------------------")
    for i, record in enumerate(DATA_RAK_BUKU):
        listbox_books.insert(END, f"[{i}] Rak {record['shelf']}: {record['title']}")

# ===============================================
# 4. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Algoritma Searching - Ternary Search (Mencari Buku)") 
root.geometry("1000x800") 
root.configure(bg="#F0FFFF") 
custom_font = tkfont.Font(family="Arial", size=10)

## 🏷️ Judul Konsep
tk.Label(root, text=f"ALGORITMA TERNARY SEARCH: KASUS MENCARI BUKU ($O(\log_3 n)$)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text=f"Algoritma membagi ruang pencarian menjadi TIGA segmen di setiap langkah. (Hanya untuk data TERURUT).", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)

# --- Frame Daftar Buku ---
tk.Label(root, text="BUKU YANG TERSEDIA DI PERPUSTAKAAN (Terurut Sesuai Judul):", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

listbox_books = tk.Listbox(root, height=10, width=120, font=custom_font, justify='left', bg="#E0FFFF")
listbox_books.pack(padx=20, pady=5)
setup_book_list_display()

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Judul Buku yang Dicari:", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
entry_target = tk.Entry(frame_input, width=40)
entry_target.grid(row=0, column=1, padx=5, pady=5)
entry_target.insert(END, "Filsafat Timur") # Contoh default

# Tombol Pencarian
tk.Button(frame_input, text="CARI BUKU (TERNARY SEARCH)", command=handle_search, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10)

# Label Status
label_status = tk.Label(root, text="Masukkan judul buku yang ingin dicari. Data sudah terurut.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Visualisasi Langkah ---
tk.Label(root, text="DETAIL LANGKAH PENCARIAN (Membagi Tiga):", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

listbox_steps = tk.Listbox(root, height=15, width=120, font=("Courier", 10))
listbox_steps.pack(padx=20, pady=10)

root.mainloop()