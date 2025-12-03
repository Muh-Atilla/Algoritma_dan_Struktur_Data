import tkinter as tk
from tkinter import END, messagebox, ttk
from random import shuffle
import re

# ===============================================
# 0. STRUKTUR DATA (DATA PRODUK)
# ===============================================

class Product:
    """Merepresentasikan produk dengan Nama dan Harga."""
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __lt__(self, other):
        # Merge Sort akan mengurutkan berdasarkan harga (dari termurah ke termahal)
        return self.price < other.price
        
    def __repr__(self):
        return f"({self.name}: Rp{self.price})"
        
    def display_data(self):
        # Format untuk tampilan tabel
        return (self.name, f"Rp {self.price:,.0f}")


# ===============================================
# 1. ALGORITMA MERGE SORT (REKURSIF)
# ===============================================

current_data = [] 

def merge(left, right, steps, data_main_ref):
    """Menggabungkan dua sub-daftar produk terurut."""
    i = j = 0
    merged = []
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]: 
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    start_index = -1
    try:
         if left:
              start_index = data_main_ref.index(left[0])
         elif right:
              start_index = data_main_ref.index(right[0])
    except ValueError:
        # Jika objek tidak bisa dicari (misalnya karena duplikasi), abaikan.
        return merged
    
    steps.append({
        "action": "MERGE",
        "left": [str(o) for o in left],
        "right": [str(o) for o in right],
        "result": [str(o) for o in merged],
        "start_index": start_index,
        "length": len(merged)
    })
    
    return merged

def merge_sort_recursive(data, steps, data_main_ref):
    """Fungsi utama rekursif untuk Merge Sort."""
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    
    left = data[:mid]
    right = data[mid:]
    
    left = merge_sort_recursive(left, steps, data_main_ref)
    right = merge_sort_recursive(right, steps, data_main_ref)
    
    return merge(left, right, steps, data_main_ref) 

# --- 2. LOGIKA GUI (Handler Tombol & Tabelisasi) ---

current_steps = []
current_step_index = 0

def parse_input_data(input_string):
    """Mengubah string input menjadi list objek Product."""
    products = []
    items = re.split(r'[,\n]', input_string)
    
    for item in items:
        item = item.strip()
        if not item:
            continue
            
        try:
            name, price_str = item.split(':')
            name = name.strip()
            # Membersihkan input harga dari format ribuan/pemisah
            price = int(price_str.strip().replace('.', '').replace(',', '')) 
            
            if name and price >= 0:
                products.append(Product(name, price))
            
        except ValueError:
            messagebox.showwarning("Input Format Salah", f"Format '{item}' tidak valid. Gunakan format 'Nama:Harga'.")
            return None
        except Exception:
             messagebox.showwarning("Input Format Salah", f"Format input keseluruhan tidak valid. Pastikan setiap item dipisahkan koma atau baris baru.")
             return None

    return products

def create_table_data(data, highlighted_start=-1, highlighted_length=0):
    """Mengubah list objek Product menjadi format tabel."""
    
    for item in tree.get_children():
        tree.delete(item)
    
    tree.tag_configure('highlight', background='#ADD8E6', foreground='black') 
    tree.tag_configure('normal', background='white', foreground='black')
    
    for idx, product_obj in enumerate(data):
        tags_style = ('highlight',) if highlighted_start <= idx < highlighted_start + highlighted_length else ('normal',)
        
        tree.insert('', tk.END, values=product_obj.display_data(), tags=tags_style)


def update_data_display(step):
    """Memperbarui visualisasi tabel berdasarkan langkah saat ini."""
    global current_data 
    
    if step['action'] == "INITIAL":
        create_table_data(step['data'])
        label_status.config(text="Data Barang Awal (Teracak). Klik 'Next Step' untuk melihat Penggabungan.", fg="black")
        return
        
    result_str = step['result']
    start_index = step['start_index']
    length = step['length']
    
    merged_products = []
    for s in result_str:
        match = re.search(r'\(([^:]+):', s)
        if match:
            product_name = match.group(1).strip()
            for product in current_data:
                if product.name == product_name and product not in merged_products:
                    merged_products.append(product)
                    break
        
    # 1. Terapkan hasil gabungan ke porsi yang benar dari data utama
    if merged_products:
        current_data[start_index: start_index + length] = merged_products
    data = current_data
    
    # 2. Perbarui tampilan tabel dengan highlight
    create_table_data(data, start_index, length)

    # 3. Update status
    status_text = f"🔄 MERGE: Menggabungkan sub-daftar produk {step['left']} dan {step['right']}."
    status_text += f" Hasil terurut berdasarkan harga diletakkan di posisi {start_index}."
    label_status.config(text=status_text, fg="blue")


def handle_sort():
    """Memulai proses Merge Sort."""
    global current_steps, current_step_index, current_data
    
    input_text = text_input.get(1.0, END).strip()
    parsed_data = parse_input_data(input_text)
    
    if not parsed_data or len(parsed_data) < 2:
        messagebox.showerror("Input Error", "Masukkan minimal 2 item produk dengan format yang benar.")
        return
        
    shuffle(parsed_data) # **MENGACAK DATA (SESUAI PERMINTAAN USER)**
    current_data = parsed_data[:] 
    
    current_steps = []
    current_steps.append({"action": "INITIAL", "data": current_data})
    
    merge_sort_recursive(current_data[:], current_steps, current_data) 
    current_step_index = 0
    
    if current_steps:
        handle_next_step()
    
    button_next.config(state=tk.NORMAL)
    button_start.config(state=tk.DISABLED)


def handle_next_step():
    """Melangkah ke langkah berikutnya."""
    global current_step_index
    
    if not current_steps:
        return
        
    if current_step_index < len(current_steps):
        step = current_steps[current_step_index]
        update_data_display(step)
        
        current_step_index += 1
        
        if current_step_index == len(current_steps):
            label_status.config(text=f"✅ Pengurutan Selesai! Daftar Barang Terurut (Termurah ke Termahal).", fg="darkgreen")
            button_next.config(state=tk.DISABLED)
            button_start.config(state=tk.NORMAL)
    
    

# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Merge Sort: Mengurutkan Data Barang") 
# UKURAN JENDELA: DIBIARKAN AGAR TIDAK TERLALU BESAR
root.geometry("800x500") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"🛍️ MERGE SORT: MENGURUTKAN BARANG BERDASARKAN HARGA", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Diurutkan berdasarkan Harga (Termurah ke Termahal). Data awal akan diacak.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
# --- Frame Input Data ---
frame_input_data = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input_data.pack(pady=5) 

tk.Label(frame_input_data, text="Input Data (Format: Nama:Harga, Pisahkan dengan koma atau baris baru):", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).pack(pady=5)

text_input = tk.Text(frame_input_data, width=50, height=4) 
text_input.pack(padx=5, pady=5)
text_input.insert(END, "Sepatu: 350000\nCelana: 120000\nBaju: 80000\nTopi: 45000\nJaket: 250000") 


# --- Visualisasi Tabel ---
tk.Label(root, text="STATUS PENGURUTAN (Area yang baru digabungkan di-highlight):", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold")).pack(pady=5)

# Konfigurasi Style dan Treeview (Tabel)
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#E0FFFF")
# MENGURANGI TINGGI BARIS TABEL (ROW HEIGHT)
style.configure("Treeview", font=('Arial', 11), rowheight=20) 

tree_frame = tk.Frame(root)
tree_frame.pack(padx=20, pady=5)

# MENGURANGI JUMLAH BARIS MAKSIMUM YANG DITAMPILKAN (HEIGHT)
tree = ttk.Treeview(tree_frame, columns=('Nama', 'Harga'), show='headings', height=6) 
tree.pack(side="left", fill="both", expand=True)

tree.heading('Nama', text='NAMA BARANG')
tree.heading('Harga', text='HARGA')

tree.column('Nama', width=200, anchor='w')
tree.column('Harga', width=150, anchor='e')

initial_data = parse_input_data(text_input.get(1.0, END))
if initial_data:
    create_table_data(initial_data)


# Label Status
label_status = tk.Label(root, text="Tekan 'Mulai Pengurutan' setelah memasukkan data.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=5) 

# --- Tombol Operasi ---
frame_tombol = tk.Frame(root, bg="#F0FFFF")
frame_tombol.pack(pady=5) # Padding minimal agar tombol dekat dengan status

button_start = tk.Button(frame_tombol, text="Mulai Pengurutan & Acak Data", command=handle_sort, 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold")) # KOTAK HIJAU
button_start.pack(side=tk.LEFT, padx=10)
          
button_next = tk.Button(frame_tombol, text="Langkah Selanjutnya (NEXT STEP)", command=handle_next_step, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")) # KOTAK BIRU
button_next.pack(side=tk.LEFT, padx=10)
button_next.config(state=tk.DISABLED)

root.mainloop()