import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Konstan Toko ---
NAMA_TOKO = "TOKO SUMBER TAKWA"

# --- 2. Struktur Data (List of Dictionaries/Structs) ---
# Struktur (Dictionary) untuk menyimpan data satu produk lengkap
data_produk_struct = [] 

def tampilkan_data_struct():
    """Membersihkan dan mengisi Treeview dengan data dari Struktur (Dictionary)."""
    
    # Bersihkan data lama
    for item in tree.get_children():
        tree.delete(item)
    
    # Iterasi data
    for i, data in enumerate(data_produk_struct): 
        
        # Ekstraksi dan Format Tipe Data
        harga_format = f"Rp {data['harga_beli']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        status_kadaluarsa = "YA" if data['kadaluarsa'] else "TIDAK" # Boolean

        # Masukkan data ke Treeview (Tabel)
        tree.insert('', 'end', values=(
            i + 1, 
            # data['kode_produk'],   <--- DIHAPUS
            data['nama_produk'],   # String
            harga_format,          # Float
            data['stok_dos'],      # Integer
            status_kadaluarsa      # Boolean
        ))
    
    label_total_data.config(text=f"Total Struktur Data Produk: {len(data_produk_struct)}")


def tambah_data_struct():
    """Mengambil input, memvalidasi tipe data, dan menambahkannya sebagai satu Struktur (Dictionary)."""
    
    # Ambil input (Kode Produk DIHAPUS)
    nama_input = entry_nama.get().strip()
    harga_input_str = entry_harga.get().strip()
    stok_input_str = entry_stok.get().strip()
    kadaluarsa_bool = var_kadaluarsa.get() # True/False dari Checkbutton

    # Validasi Dasar
    if not all([nama_input, harga_input_str, stok_input_str]):
        messagebox.showerror("Error", "Nama Produk, Harga Beli, dan Stok Dos wajib diisi.")
        return

    try:
        # Konversi dan Validasi Tipe Data
        harga_beli_float = float(harga_input_str)   # Harus Float
        stok_dos_int = int(stok_input_str)          # Harus Integer
        
        if stok_dos_int < 0 or harga_beli_float < 0:
            messagebox.showerror("Error", "Harga dan Stok tidak boleh negatif.")
            return

        # --- Membuat Struktur Data Baru (Dictionary) ---
        produk_baru = {
            # 'kode_produk': kode_input,       <--- DIHAPUS
            'nama_produk': nama_input,       # String
            'harga_beli': harga_beli_float,  # Float
            'stok_dos': stok_dos_int,        # Integer
            'kadaluarsa': kadaluarsa_bool    # Boolean
        }
        
        # Menambahkan Struktur ke List Global
        data_produk_struct.append(produk_baru)

        # Bersihkan input
        entry_nama.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_stok.delete(0, tk.END)
        var_kadaluarsa.set(False) # Reset Checkbutton
        entry_nama.focus_set()
        
        # Tampilkan data terbaru
        tampilkan_data_struct()

    except ValueError:
        messagebox.showerror("Error", "Pastikan Harga diisi angka desimal (Float) dan Stok diisi angka bulat (Integer).")


# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Konsep Struktur Data (Dictionary) - {NAMA_TOKO}")
root.geometry("750x600")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul
tk.Label(root, text=f"INPUT STRUKTUR DATA PRODUK: {NAMA_TOKO.upper()}", 
         bg="#F0FFFF", fg="#000080", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#F0FFFF", padx=10, pady=10)
frame_input.pack(pady=5)

# Input Baris 1 (Kode Produk DIHAPUS, dipindahkan ke kolom 0)
tk.Label(frame_input, text="Nama Produk (String):", bg="#F0FFFF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Harga Beli (Float):", bg="#F0FFFF").grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_harga = tk.Entry(frame_input, width=15)
entry_harga.grid(row=0, column=3, padx=5, pady=5)

# Input Baris 2
tk.Label(frame_input, text="Stok Dos (Integer):", bg="#F0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_stok = tk.Entry(frame_input, width=15)
entry_stok.grid(row=1, column=1, padx=5, pady=5)

# Input Baris 3 (Boolean)
var_kadaluarsa = tk.BooleanVar()
check_kadaluarsa = tk.Checkbutton(frame_input, text="Status Kadaluarsa (Boolean)", variable=var_kadaluarsa, 
                                  bg="#F0FFFF", fg="#8B0000")
check_kadaluarsa.grid(row=1, column=2, sticky="w", padx=5, pady=10)

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Struktur Data", command=tambah_data_struct, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=700, bg="grey").pack(pady=10)

## 📊 Label Output Total
label_total_data = tk.Label(root, text="Total Struktur Data Produk: 0", 
                            bg="#F0FFFF", fg="#8B0000", font=("Arial", 12, "bold"))
label_total_data.pack(pady=5)

# --- 4. Tabel (Treeview) untuk Output Rincian ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview (Kolom Kode DIHAPUS)
tree = ttk.Treeview(frame_tabel, columns=("No", "Nama", "HargaBeli", "StokDos", "Kadaluarsa"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("Nama", text="Nama (String)", anchor=tk.CENTER)
tree.heading("HargaBeli", text="Harga Beli (Float)", anchor=tk.CENTER)
tree.heading("StokDos", text="Stok Dos (Integer)", anchor=tk.CENTER)
tree.heading("Kadaluarsa", text="Kadaluarsa (Boolean)", anchor=tk.CENTER)

# Lebar Kolom
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("Nama", width=220, anchor=tk.W)
tree.column("HargaBeli", width=120, anchor=tk.E)
tree.column("StokDos", width=100, anchor=tk.CENTER)
tree.column("Kadaluarsa", width=120, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()