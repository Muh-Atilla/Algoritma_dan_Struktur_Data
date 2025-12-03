import tkinter as tk
from tkinter import END, messagebox, ttk
from random import shuffle
import re

# ===============================================
# 0. STRUKTUR DATA (DATA PRODUK)
# ===============================================

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __lt__(self, other):
        # Quick Sort berdasarkan harga (termurah ke termahal)
        return self.price < other.price
        
    def display_data(self):
        return (self.name, f"Rp {self.price:,.0f}")

# ===============================================
# 1. ALGORITMA QUICK SORT (REKURSIF)
# (Inti logika Partisi tetap sama)
# ===============================================

current_data = [] 

def partition(data, low, high, steps):
    """
    Fungsi Partisi: Mengatur ulang elemen di sekitar Pivot (elemen terakhir).
    """
    pivot = data[high]
    i = low - 1
    
    steps.append({
        "action": "PIVOT_SELECT",
        "low": low,
        "high": high,
        "pivot_val": str(pivot),
        "data_display": [p.display_data() for p in data]
    })

    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]

            if i != j:
                steps.append({
                    "action": "SWAP",
                    "low": low,
                    "high": high,
                    "index1": i,
                    "index2": j,
                    "data_display": [p.display_data() for p in data]
                })

    data[i + 1], data[high] = data[high], data[i + 1]

    steps.append({
        "action": "PIVOT_FINAL",
        "low": low,
        "high": high,
        "pivot_index": i + 1,
        "data_display": [p.display_data() for p in data]
    })

    return i + 1

def quick_sort_recursive(data, low, high, steps):
    if low < high:
        pi = partition(data, low, high, steps)
        quick_sort_recursive(data, low, pi - 1, steps)
        quick_sort_recursive(data, pi + 1, high, steps)


# --- 2. LOGIKA GUI (Handler Tombol & Tabelisasi) ---

current_steps = []
current_step_index = 0

def parse_input_data(input_string):
    products = []
    items = re.split(r'[,\n]', input_string)
    
    for item in items:
        item = item.strip()
        if not item: continue
        try:
            name, price_str = item.split(':')
            name = name.strip()
            price = int(price_str.strip().replace('.', '').replace(',', ''))
            if name and price >= 0:
                products.append(Product(name, price))
        except:
             messagebox.showwarning("Input Error", "Format input salah. Gunakan 'Nama:Harga'.")
             return None
    return products

def create_table_data(data_display, low=-1, high=-1, pivot_index=-1, swap_index1=-1, swap_index2=-1):
    for item in tree.get_children(): tree.delete(item)
    
    # Konfigurasi Highlight
    tree.tag_configure('pivot', background='#F08080', foreground='white')
    tree.tag_configure('swap', background='#DAA520', foreground='white')
    tree.tag_configure('range', background='#ADD8E6', foreground='black')

    for idx, item in enumerate(data_display):
        tags_list = ['normal']
        if low <= idx <= high and low != -1: tags_list.append('range')
        if idx == high and pivot_index == -1: tags_list.append('pivot')
        if idx == pivot_index: tags_list = ['pivot']
        if idx == swap_index1 or idx == swap_index2: tags_list.append('swap')
            
        tree.insert('', tk.END, values=(idx, item[0], item[1]), tags=tuple(tags_list))


def update_data_display(step):
    global current_data 
    
    action = step['action']
    data_display = step['data_display']
    
    low = step.get('low', -1)
    high = step.get('high', -1)
    pivot_index = step.get('pivot_index', -1)
    swap_index1 = step.get('index1', -1)
    swap_index2 = step.get('index2', -1)

    create_table_data(data_display, low, high, pivot_index, swap_index1, swap_index2)

    status_text = ""
    if action == "INITIAL":
        status_text = "Data Awal. Klik NEXT STEP."
        label_status.config(text=status_text, fg="black")
        return
    elif action == "PIVOT_SELECT":
        status_text = f"🎯 PIVOT: Range [{low}-{high}]. Pivot: {step['pivot_val']}."
        label_status.config(text=status_text, fg="#8B0000") 
    elif action == "SWAP":
        status_text = f"🔄 SWAP: Tukar Index {swap_index1} dan {swap_index2}."
        label_status.config(text=status_text, fg="#CC9900") 
    elif action == "PIVOT_FINAL":
        status_text = f"✅ FINAL: Pivot di Index {pivot_index}."
        label_status.config(text=status_text, fg="darkgreen") 
    
    

def handle_sort():
    global current_steps, current_step_index, current_data
    
    input_text = text_input.get(1.0, END).strip()
    parsed_data = parse_input_data(input_text)
    
    if not parsed_data or len(parsed_data) < 2:
        messagebox.showerror("Input Error", "Masukkan minimal 2 item.")
        return
        
    shuffle(parsed_data)
    current_data = parsed_data[:] 
    
    current_steps = []
    initial_display = [p.display_data() for p in current_data] 
    current_steps.append({"action": "INITIAL", "data_display": initial_display})
    
    quick_sort_recursive(current_data, 0, len(current_data) - 1, current_steps) 
    current_step_index = 0
    
    if current_steps:
        handle_next_step()
    
    button_next.config(state=tk.NORMAL)
    button_start.config(state=tk.DISABLED)


def handle_next_step():
    global current_step_index
    
    if not current_steps: return
        
    if current_step_index < len(current_steps):
        step = current_steps[current_step_index]
        update_data_display(step)
        
        current_step_index += 1
        
        if current_step_index == len(current_steps):
            label_status.config(text=f"✅ Selesai! Data Terurut.", fg="darkgreen")
            button_next.config(state=tk.DISABLED)
            button_start.config(state=tk.NORMAL)
    
    

# ===============================================
# 3. KONFIGURASI TKINTER GUI (MINIMALIS)
# ===============================================

root = tk.Tk()
root.title(f"Quick Sort Minimalis") 
# UKURAN JENDELA SANGAT KECIL
root.geometry("550x450") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"⚔️ QUICK SORT: BARANG BERDASARKAN HARGA", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

# --- Frame Input Data ---
frame_input_data = tk.Frame(root, bg="#E0FFFF", padx=10, pady=5, bd=1, relief=tk.GROOVE)
frame_input_data.pack(pady=5) 

tk.Label(frame_input_data, text="Input (Nama:Harga):", 
         bg="#E0FFFF", font=("Arial", 9, "bold")).pack(pady=2)

text_input = tk.Text(frame_input_data, width=35, height=3) # Tinggi Text Input Minimal
text_input.pack(padx=5, pady=2)
text_input.insert(END, "Sepatu: 350000\nCelana: 120000\nBaju: 80000\nTopi: 45000\nJaket: 250000") 


# --- Visualisasi Tabel ---
tk.Label(root, text="STATUS PENGURUTAN:", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 10, "bold")).pack(pady=3)

# Konfigurasi Style dan Treeview (Tabel)
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 9, 'bold'), background="#E0FFFF")
style.configure("Treeview", font=('Arial', 10), rowheight=18) 

tree_frame = tk.Frame(root)
tree_frame.pack(padx=20, pady=2)

tree = ttk.Treeview(tree_frame, columns=('Index', 'Nama', 'Harga'), show='headings', height=5) # Tinggi Tabel Minimal
tree.pack(side="left", fill="both", expand=True)

tree.heading('Index', text='IDX')
tree.heading('Nama', text='NAMA')
tree.heading('Harga', text='HARGA')

# Lebar Kolom Diatur Sangat Kecil
tree.column('Index', width=40, anchor='center')
tree.column('Nama', width=120, anchor='w')
tree.column('Harga', width=80, anchor='e')

initial_data = parse_input_data(text_input.get(1.0, END))
if initial_data:
    initial_display = [p.display_data() for p in initial_data]
    create_table_data(initial_display)


# Label Status
label_status = tk.Label(root, text="Tekan 'Mulai' untuk Pengurutan.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 9, "bold"))
label_status.pack(pady=5) 

# --- Tombol Operasi ---
frame_tombol = tk.Frame(root, bg="#F0FFFF")
frame_tombol.pack(pady=5) 

button_start = tk.Button(frame_tombol, text="Mulai", command=handle_sort, 
          bg="#3CB371", fg="white", font=("Arial", 9, "bold"), padx=5, pady=3)
button_start.pack(side=tk.LEFT, padx=10)
          
button_next = tk.Button(frame_tombol, text="NEXT STEP", command=handle_next_step, 
          bg="#4682B4", fg="white", font=("Arial", 9, "bold"), padx=5, pady=3)
button_next.pack(side=tk.LEFT, padx=10)
button_next.config(state=tk.DISABLED)

root.mainloop()