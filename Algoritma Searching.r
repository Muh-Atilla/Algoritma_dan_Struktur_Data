import tkinter as tk
from tkinter import END
from random import shuffle

# ===============================================
# 1. ALGORITMA LINEAR SEARCH
# ===============================================

def linear_search(data, target):
    """Mencari target dalam data (tidak terurut) secara beruntun."""
    steps = [] # Untuk mencatat langkah-langkah
    
    # Proses utama Linear Search: Iterasi dari indeks 0 hingga akhir
    for i, item in enumerate(data):
        
        # Catat langkah saat ini
        steps.append({
            "index": i, 
            "item_checked": item
        })
        
        if item == target:
            # Ditemukan, segera kembalikan indeks dan langkah
            return i, steps, True 
            
    return -1, steps, False # Tidak Ditemukan

# --- 2. LOGIKA GUI (Handler Tombol) ---

# Data awal (tetap, tetapi tidak terurut)
data_list_initial = [56, 2, 72, 12, 91, 23, 8, 38, 5, 16]
data_list = data_list_initial.copy() # Gunakan salinan untuk operasi

def handle_search():
    """Menangani tombol Pencarian."""
    target_input = entry_target.get().strip()
    
    try:
        target = int(target_input)
    except ValueError:
        update_output("❌ Masukkan angka integer yang valid.", "red")
        return
    
    # Panggil Linear Search
    index, steps, found = linear_search(data_list, target)
    
    # Tampilkan Hasil dan Langkah
    update_result_display(index, target, steps, found)

def update_output(message, color="black"):
    """Update label status."""
    label_status.config(text=message, fg=color)

def update_result_display(index, target, steps, found):
    """Menampilkan langkah dan hasil pencarian."""
    
    listbox_steps.delete(0, END)
    
    if not found:
        message = f"❌ Gagal: Angka {target} tidak ditemukan setelah memeriksa {len(steps)} elemen."
        update_output(message, "red")
        
    else:
        message = f"✅ BERHASIL: Angka {target} ditemukan pada Indeks ke-{index} dalam {len(steps)} langkah."
        update_output(message, "green")
    
    # Tampilkan Langkah-Langkah Pencarian
    listbox_steps.insert(END, f"--- PENCARIAN BERUNTUN UNTUK {target} ---")
    listbox_steps.insert(END, f"DATA (TIDAK TERURUT): {data_list}")
    listbox_steps.insert(END, "------------------------------------------")
    
    for i, step in enumerate(steps):
        status = "Ditemukan!" if step['item_checked'] == target else "Mencocokkan..."
        
        # Tanda panah menunjukkan elemen yang sedang diperiksa
        data_display = [str(x) for x in data_list]
        data_display[step['index']] = f"-->{data_display[step['index']]}<--"
        
        step_str = f"Langkah {i+1} (Indeks {step['index']}): Memeriksa angka {step['item_checked']}. Status: {status}"
        
        listbox_steps.insert(END, step_str)
        listbox_steps.insert(END, f"       Data Status: {' '.join(data_display)}")

    listbox_steps.insert(END, "------------------------------------------")
    
    if found:
        listbox_steps.insert(END, f"HASIL AKHIR: Ditemukan pada Indeks {index}")
    else:
        listbox_steps.insert(END, "Pencarian berakhir di akhir data.")


# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Algoritma Searching - Linear Search") 
root.geometry("850x650") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"ALGORITMA SEARCHING: LINEAR SEARCH ($O(n)$)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text=f"Data Awal (Tidak Terurut): {data_list_initial}", 
         bg="#E0FFFF", fg="#004D40", font=("Arial", 11, "bold")).pack(pady=5, padx=20)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Angka yang Dicari (Target):", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
entry_target = tk.Entry(frame_input, width=15)
entry_target.grid(row=0, column=1, padx=5, pady=5)
entry_target.insert(END, "8") # Contoh default yang ada di tengah

# Tombol Pencarian
tk.Button(frame_input, text="JALANKAN LINEAR SEARCH", command=handle_search, 
          bg="#B22222", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10)

# Label Status
label_status = tk.Label(root, text="Masukkan target pencarian.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Visualisasi Langkah ---
tk.Label(root, text="DETAIL LANGKAH PENCARIAN (Cek Satu Per Satu):", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

listbox_steps = tk.Listbox(root, height=20, width=120, font=("Courier", 10))
listbox_steps.pack(padx=20, pady=10)

root.mainloop()