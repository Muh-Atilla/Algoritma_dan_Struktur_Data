import tkinter as tk
from tkinter import END
from tkinter import messagebox
import time

# ===============================================
# 1. ALGORITMA BUBBLE SORT
# ===============================================

def bubble_sort(data):
    """Mengurutkan data menggunakan Bubble Sort dan mencatat langkahnya."""
    n = len(data)
    steps = []
    
    # Outer loop: Mengontrol jumlah pass (putaran)
    # n-1 pass sudah cukup
    for i in range(n - 1):
        swapped = False # Flag untuk kasus terbaik O(n)
        
        # Inner loop: Membandingkan elemen yang berdekatan
        # Kita tidak perlu memeriksa i elemen terakhir (karena sudah diurutkan)
        for j in range(n - 1 - i):
            
            # Catat langkah saat ini sebelum perbandingan/penukaran
            steps.append({
                "data": list(data), 
                "comparison_index": j, # Elemen yang dibandingkan
                "is_swapped": False,
                "sorted_boundary": n - i # Batas data yang sudah diurutkan
            })
            
            # Perbandingan
            if data[j] > data[j + 1]:
                # Penukaran (Swap)
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                
                # Catat langkah penukaran
                steps.append({
                    "data": list(data), 
                    "comparison_index": j, 
                    "is_swapped": True,
                    "sorted_boundary": n - i 
                })
        
        # Jika tidak ada penukaran di pass ini, data sudah terurut
        if not swapped:
            break
            
    return steps, data

# --- 2. LOGIKA GUI (Handler Tombol) ---

INITIAL_DATA = [5, 1, 4, 2, 8]
current_steps = []
current_step_index = 0

def update_data_display(data, current_index=-1, swapped=False, boundary=-1):
    """Memperbarui visualisasi daftar data."""
    listbox_data.delete(0, END)
    
    # Menampilkan data array
    display_str = []
    for idx, item in enumerate(data):
        item_str = str(item)
        
        if boundary != -1 and idx >= boundary:
            # Elemen sudah diurutkan (di ujung kanan)
            item_str = f"[{item_str}]" 
        elif idx == current_index:
            # Elemen yang dibandingkan/ditukar
            item_str = f"<{item_str}>" 
        
        display_str.append(item_str)
        
    listbox_data.insert(END, " ".join(display_str))
    
    # Menampilkan status langkah
    status_text = f"Membandingkan Indeks {current_index} dan {current_index + 1}."
    if swapped:
        status_text += " 🔄 DITUKAR!"
    elif current_index != -1:
        status_text += " ✅ Tidak Ditukar."
        
    label_status.config(text=status_text, 
                        fg="green" if swapped else "blue")


def handle_sort():
    """Memulai proses pengurutan."""
    global current_steps, current_step_index
    
    data_to_sort = list(INITIAL_DATA)
    current_steps, sorted_data = bubble_sort(data_to_sort)
    current_step_index = 0
    
    # Tampilkan langkah pertama
    if current_steps:
        handle_next_step()
    else:
        update_data_display(sorted_data)
        label_status.config(text="Data sudah terurut.", fg="green")


def handle_next_step():
    """Melangkah ke langkah berikutnya."""
    global current_step_index
    
    if not current_steps:
        return
        
    if current_step_index < len(current_steps):
        step = current_steps[current_step_index]
        
        update_data_display(step['data'], 
                            step['comparison_index'], 
                            step['is_swapped'], 
                            step['sorted_boundary'])
        
        current_step_index += 1
        
        # Sembunyikan tombol 'Next' jika sudah langkah terakhir
        if current_step_index == len(current_steps):
            label_status.config(text="✅ Pengurutan Selesai!", fg="darkgreen")
            button_next.config(state=tk.DISABLED)
    
    button_next.config(state=tk.NORMAL)


# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Algoritma Pengurutan - Bubble Sort") 
root.geometry("600x450") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"ALGORITMA SORTING: BUBBLE SORT ($O(n^2)$)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Mekanisme: Membandingkan dan Menukar elemen yang berdekatan.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
tk.Label(root, text=f"Data Awal: {INITIAL_DATA}", 
         bg="#E0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=10, padx=20)

# --- Visualisasi Data ---
tk.Label(root, text="STATUS DATA ARRAY:", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold")).pack(pady=5)

listbox_data = tk.Listbox(root, height=1, width=30, font=("Courier", 20), justify='center', bg="#FFFFFF")
listbox_data.pack(padx=20, pady=5)
listbox_data.insert(END, " ".join(map(str, INITIAL_DATA)))

# Label Status
label_status = tk.Label(root, text="Klik 'Mulai Pengurutan' untuk menjalankan algoritma.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Tombol Operasi ---
frame_tombol = tk.Frame(root, bg="#F0FFFF")
frame_tombol.pack(pady=10)

tk.Button(frame_tombol, text="Mulai Pengurutan", command=handle_sort, 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
          
button_next = tk.Button(frame_tombol, text="Langkah Selanjutnya (NEXT STEP)", command=handle_next_step, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
button_next.pack(side=tk.LEFT, padx=10)
button_next.config(state=tk.DISABLED)

root.mainloop()