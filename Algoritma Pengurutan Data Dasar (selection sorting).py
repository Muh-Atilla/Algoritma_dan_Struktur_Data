import tkinter as tk
from tkinter import END
from tkinter import messagebox
import time

# ===============================================
# 1. ALGORITMA SELECTION SORT
# ===============================================

def selection_sort(data):
    """Mengurutkan data menggunakan Selection Sort dan mencatat langkahnya."""
    n = len(data)
    steps = []
    
    # Outer loop: Mengontrol batas Bagian Terurut (i adalah batas kiri)
    for i in range(n - 1):
        min_idx = i # Anggap elemen saat ini (i) adalah yang terkecil
        
        # Inner loop: Mencari elemen terkecil di Bagian Belum Terurut
        for j in range(i + 1, n):
            
            # Catat langkah saat ini: perbandingan dengan elemen di j
            steps.append({
                "data": list(data), 
                "comparison_index": j,       # Elemen yang sedang dibandingkan
                "min_index_current": min_idx, # Indeks elemen terkecil yang ditemukan sejauh ini
                "is_swapped": False,
                "sorted_boundary": i         # Batas data yang sudah terurut
            })
            
            # Perbandingan untuk menemukan minimum baru
            if data[j] < data[min_idx]:
                min_idx = j # Update indeks terkecil
        
        # Penukaran (Swap): Tukar elemen terkecil yang ditemukan dengan elemen di posisi i
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            
            # Catat langkah penukaran (selalu terjadi setelah inner loop selesai)
            steps.append({
                "data": list(data), 
                "comparison_index": i, 
                "min_index_current": min_idx, # Indeks elemen terkecil yang ditemukan
                "is_swapped": True,
                "sorted_boundary": i + 1 # Boundary berpindah setelah penukaran
            })
        else:
            # Jika tidak ada penukaran, tetap catat status
            steps.append({
                "data": list(data), 
                "comparison_index": i, 
                "min_index_current": i, 
                "is_swapped": False,
                "sorted_boundary": i + 1
            })

    # Catat langkah terakhir (selesai)
    steps.append({"data": list(data), "comparison_index": -1, "min_index_current": -1, "is_swapped": False, "sorted_boundary": n})
            
    return steps, data

# --- 2. LOGIKA GUI (Handler Tombol) ---

current_steps = []
current_step_index = 0
DATA_INPUT = [] # Variabel global untuk menyimpan data dari input

def parse_input_data(input_string):
    """Mengubah string input menjadi list of integers."""
    try:
        # Pisahkan berdasarkan koma, spasi, atau keduanya, lalu konversi ke int
        data = [int(x.strip()) for x in input_string.replace(',', ' ').split() if x.strip()]
        return data
    except ValueError:
        return None

def update_data_display(data, current_index, min_idx, swapped, boundary):
    """Memperbarui visualisasi daftar data."""
    listbox_data.delete(0, END)
    
    # Menampilkan data array
    display_str = []
    for idx, item in enumerate(data):
        item_str = str(item)
        
        if idx < boundary:
            # Elemen sudah diurutkan (di ujung kiri)
            item_str = f"[{item_str}]"
        elif idx == min_idx and min_idx != current_index:
            # Elemen terkecil saat ini
            item_str = f"|{item_str}|"
        elif idx == current_index and current_index >= boundary:
            # Elemen yang sedang dibandingkan/dicari (di unsorted portion)
            item_str = f"<{item_str}>"
        
        display_str.append(item_str)
        
    listbox_data.insert(END, " ".join(display_str))
    
    # Menampilkan status langkah
    if swapped:
        status_text = f"🔄 SWAP: Menukar posisi {current_index} dengan elemen terkecil ({data[current_index]}) di posisi {min_idx}. Minimum Swap!"
        fg_color = "green"
    elif current_index != -1 and current_index < boundary and current_index == 0:
        status_text = f"Mulai Pass {boundary}. Mencari elemen terkecil..."
        fg_color = "blue"
    elif current_index != -1 and current_index < boundary:
        status_text = f"Membandingkan Indeks {current_index}. Minimum sementara: {data[min_idx]}."
        fg_color = "blue"
    else:
        status_text = "Pengurutan Selesai atau menunggu langkah selanjutnya."
        fg_color = "black"

    label_status.config(text=status_text, fg=fg_color)


def handle_sort():
    """Memulai proses pengurutan."""
    global current_steps, current_step_index, DATA_INPUT
    
    # 1. Parsing input
    input_text = entry_input.get().strip()
    parsed_data = parse_input_data(input_text)
    
    if not parsed_data or len(parsed_data) < 2:
        messagebox.showerror("Input Error", "Masukkan minimal 2 angka integer yang valid, dipisahkan spasi atau koma.")
        return
        
    DATA_INPUT = parsed_data
    
    data_to_sort = list(DATA_INPUT)
    current_steps, sorted_data = selection_sort(data_to_sort)
    current_step_index = 0
    
    listbox_data.delete(0, END)
    listbox_data.insert(END, " ".join(map(str, DATA_INPUT)))
    
    # Tampilkan langkah pertama
    if current_steps:
        handle_next_step()
    else:
        update_data_display(sorted_data, -1, -1, False, len(sorted_data))
        label_status.config(text="Data sudah terurut.", fg="green")
        button_next.config(state=tk.DISABLED)

    button_next.config(state=tk.NORMAL)
    button_start.config(state=tk.DISABLED) # Disable start after beginning


def handle_next_step():
    """Melangkah ke langkah berikutnya."""
    global current_step_index
    
    if not current_steps:
        return
        
    if current_step_index < len(current_steps):
        step = current_steps[current_step_index]
        
        update_data_display(step['data'], 
                            step['comparison_index'], 
                            step['min_index_current'], 
                            step['is_swapped'], 
                            step['sorted_boundary'])
        
        current_step_index += 1
        
        if current_step_index == len(current_steps):
            label_status.config(text="✅ Pengurutan Selesai!", fg="darkgreen")
            button_next.config(state=tk.DISABLED)
            button_start.config(state=tk.NORMAL) # Re-enable start
    
    

# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Algoritma Pengurutan - Selection Sort Interaktif") 
root.geometry("750x550") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"ALGORITMA SORTING: SELECTION SORT INTERAKTIF ($O(n^2)$)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Masukkan angka Anda sendiri. Selection Sort akan mencari minimum dan menukarnya di setiap Pass.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
# --- Frame Input Data ---
frame_input_data = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input_data.pack(pady=10)

tk.Label(frame_input_data, text="Input Angka (Pisahkan dengan spasi/koma, cth: 8, 3, 1, 9):", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)

entry_input = tk.Entry(frame_input_data, width=40)
entry_input.grid(row=0, column=1, padx=5, pady=5)
entry_input.insert(END, "9, 5, 2, 7, 1") # Contoh default

# --- Visualisasi Data Awal ---
tk.Label(root, text="STATUS DATA ARRAY: [Terurut] <Dibandingkan> |Minimum Sementara|", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold")).pack(pady=5)

listbox_data = tk.Listbox(root, height=1, width=45, font=("Courier", 20), justify='center', bg="#FFFFFF")
listbox_data.pack(padx=20, pady=5)
# Tampilkan data default
listbox_data.insert(END, " ".join(map(str, parse_input_data(entry_input.get()))))


# Label Status
label_status = tk.Label(root, text="Masukkan angka, lalu klik 'Mulai Pengurutan'.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Tombol Operasi ---
frame_tombol = tk.Frame(root, bg="#F0FFFF")
frame_tombol.pack(pady=10)

button_start = tk.Button(frame_tombol, text="Mulai Pengurutan", command=handle_sort, 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold"))
button_start.pack(side=tk.LEFT, padx=10)
          
button_next = tk.Button(frame_tombol, text="Langkah Selanjutnya (NEXT STEP)", command=handle_next_step, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold"))
button_next.pack(side=tk.LEFT, padx=10)
button_next.config(state=tk.DISABLED)

root.mainloop()