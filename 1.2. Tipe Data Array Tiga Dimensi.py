import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Konstan Toko ---
NAMA_TOKO = "TOKO SUMBER TAKWA"
cabang_names = ["Cabang Pakkola", "Cabang Pertokoan", "Cabang Saleppa"]
produk_names = ["Mie Instan", "Kopi Bubuk", "Gula Pasir", "Sabun Mandi"]

# --- 2. Struktur Data (Array 3D yang Disederhanakan) ---
# List of Dictionaries: [Cabang, Produk, StokJumlahDos]
data_stok_simple = []

def tampilkan_data_stok():
    """Membersihkan dan mengisi Treeview dengan data dari List Stok Global."""
    
    # Bersihkan data lama
    for item in tree.get_children():
        tree.delete(item)
    
    total_dos_semua = 0
    
    # Iterasi data
    for i, data in enumerate(data_stok_simple): 
        
        # Ekstraksi Tipe Data
        cabang_name = data['cabang']    # String (Cabang)
        produk_name = data['produk']    # String (Produk)
        stok_dos = data['stok']         # Integer (Stok Jumlah Dos)
        
        total_dos_semua += stok_dos

        # Masukkan data ke Treeview (Tabel)
        tree.insert('', 'end', values=(
            i + 1, 
            cabang_name, 
            produk_name, 
            stok_dos
        ))

    # Perbarui Label Total
    label_total_stok.config(text=f"Total Stok Jumlah Dos Keseluruhan (Integer): {total_dos_semua} dos")


def tambah_data_stok():
    """Mengambil input, memvalidasi, dan menambahkannya ke List Stok Global."""
    
    # Ambil input
    cabang_pilihan = var_cabang.get()
    produk_pilihan = var_produk.get()
    stok_dos_input_str = entry_stok.get().strip()

    # Validasi Dasar
    if not stok_dos_input_str:
        messagebox.showerror("Error", "Stok Jumlah Dos wajib diisi.")
        return

    try:
        # --- Validasi Tipe Data Integer (Stok Jumlah Dos) ---
        stok_dos = int(stok_dos_input_str)
        
        if stok_dos < 0:
            messagebox.showerror("Error", "Nilai Stok Jumlah Dos tidak boleh negatif.")
            return

        # --- Tambahkan Data ke List Stok Global ---
        
        # Menyimpan data dalam format Dictionary
        data_baru = {
            'cabang': cabang_pilihan, # Kategori Cabang
            'produk': produk_pilihan, # Kategori Produk
            'stok': stok_dos          # Nilai Stok
        }
        
        # Menambahkan data ke List Global
        data_stok_simple.append(data_baru)

        # Bersihkan input
        entry_stok.delete(0, tk.END)
        entry_stok.focus_set()
        
        # Tampilkan data terbaru ke tabel
        tampilkan_data_stok()

    except ValueError:
        messagebox.showerror("Error", "Input Stok Jumlah Dos harus berupa bilangan bulat (Integer).")


# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Input Data Stok Toko - {NAMA_TOKO}")
root.geometry("650x500")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Toko
tk.Label(root, text=f"INPUT STOK PER PRODUK PER CABANG: {NAMA_TOKO.upper()}", 
         bg="#F0FFFF", fg="#000080", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#F0FFFF", padx=10, pady=10)
frame_input.pack(pady=5)

# Pilihan Cabang (Kategori 1)
var_cabang = tk.StringVar(root)
var_cabang.set(cabang_names[0]) 
tk.Label(frame_input, text="Kategori Cabang:", bg="#F0FFFF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
cabang_menu = tk.OptionMenu(frame_input, var_cabang, *cabang_names)
cabang_menu.grid(row=0, column=1, padx=5, pady=5)
cabang_menu.config(width=18)

# Pilihan Produk (Kategori 2)
var_produk = tk.StringVar(root)
var_produk.set(produk_names[0]) 
tk.Label(frame_input, text="Kategori Produk:", bg="#F0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
produk_menu = tk.OptionMenu(frame_input, var_produk, *produk_names)
produk_menu.grid(row=1, column=1, padx=5, pady=5)
produk_menu.config(width=18)

# Input Stok (Nilai)
tk.Label(frame_input, text="Stok Jumlah Dos (Nilai):", bg="#F0FFFF").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_stok = tk.Entry(frame_input, width=15)
entry_stok.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Data Stok", command=tambah_data_stok, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=3, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=600, bg="grey").pack(pady=10)

## 📊 Label Output Total
label_total_stok = tk.Label(root, text="Total Stok Jumlah Dos Keseluruhan: 0 dos", 
                            bg="#F0FFFF", fg="#8B0000", font=("Arial", 12, "bold"))
label_total_stok.pack(pady=5)

# --- 4. Tabel (Treeview) untuk Output Rincian ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("No", "Cabang", "Produk", "StokDos"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("Cabang", text="Kategori Cabang", anchor=tk.CENTER)
tree.heading("Produk", text="Kategori Produk", anchor=tk.CENTER)
tree.heading("StokDos", text="Stok Jumlah Dos", anchor=tk.CENTER)

# Lebar Kolom
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("Cabang", width=150, anchor=tk.W)
tree.column("Produk", width=200, anchor=tk.W)
tree.column("StokDos", width=120, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()