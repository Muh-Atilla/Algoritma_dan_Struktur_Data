import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Konstan Toko ---
NAMA_TOKO = "TOKO SUMBER TAKWA"

# --- 2. Struktur Data Array Satu Dimensi (List Global) ---
# List kosong yang akan diisi oleh input pengguna
nama_produk_array = []  # Array 1D untuk String (Nama)
harga_produk_array = [] # Array 1D untuk Float (Harga)

def tampilkan_data_toko():
    """Membersihkan dan mengisi Treeview dengan data dari dua Array 1D Global."""
    
    # Bersihkan data lama
    for item in tree.get_children():
        tree.delete(item)
    
    # Tipe Data Integer: Menghitung panjang array
    panjang_array = len(nama_produk_array)
    label_panjang.config(text=f"Total Jenis Produk (Integer): {panjang_array}")
    
    # Iterasi melalui panjang array
    for indeks in range(panjang_array):
        
        # Ekstraksi dan penentuan tipe data
        nama = nama_produk_array[indeks]       # String
        harga_float = harga_produk_array[indeks] # Floating Point
        
        # Format harga menjadi string Rupiah
        # Contoh: 25750.0 -> Rp 25.750,00
        harga_format = f"Rp {harga_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Masukkan data ke Treeview (Tabel)
        tree.insert('', 'end', values=(indeks + 1, nama, harga_format))


def tambah_data_produk():
    """Mengambil input pengguna, memvalidasi tipe data, dan menambahkannya ke Array 1D."""
    
    # Ambil nilai dari input fields
    nama_input = entry_nama.get().strip()
    harga_input_str = entry_harga.get().strip()

    # Validasi Dasar
    if not nama_input or not harga_input_str:
        messagebox.showerror("Error", "Nama produk dan harga wajib diisi.")
        return

    try:
        # --- Validasi Tipe Data Float (Harga) ---
        harga_float = float(harga_input_str)
        
        if harga_float < 0:
            messagebox.showerror("Error", "Harga tidak boleh bernilai negatif.")
            return

        # --- Tambahkan Data ke Array 1D yang Sesuai ---
        
        # Tambahkan ke Array String
        nama_produk_array.append(nama_input) 
        
        # Tambahkan ke Array Floating Point
        harga_produk_array.append(harga_float) 

        # Bersihkan input fields
        entry_nama.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_nama.focus_set()
        
        # Tampilkan data terbaru ke tabel
        tampilkan_data_toko()

    except ValueError:
        # Menangani Error jika konversi ke float gagal
        messagebox.showerror("Error", "Input Harga tidak valid. Harap masukkan angka desimal (float).")


# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Input Data Produk - {NAMA_TOKO}")
root.geometry("650x550")
root.configure(bg="#F0F8FF") 

## 🏷️ Judul Toko
tk.Label(root, text=f"INPUT DATA PRODUK: {NAMA_TOKO.upper()}", 
         bg="#F0F8FF", fg="#000080", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#F0F8FF", padx=10, pady=10)
frame_input.pack(pady=5)

tk.Label(frame_input, text="Nama Produk (String):", bg="#F0F8FF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=30)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Harga (Float):", bg="#F0F8FF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_harga = tk.Entry(frame_input, width=30)
entry_harga.grid(row=1, column=1, padx=5, pady=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Produk", command=tambah_data_produk, 
          bg="#4169E1", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=2, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=600, bg="grey").pack(pady=10)

## 📊 Label Output Informasi
label_panjang = tk.Label(root, text="Total Jenis Produk (Integer): 0", 
                        bg="#F0F8FF", fg="#8B0000", font=("Arial", 12, "bold"))
label_panjang.pack(pady=5)

# --- 4. Tabel (Treeview) untuk Output Rincian ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("No", "Nama", "Harga"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("Nama", text="Nama Produk (String)", anchor=tk.CENTER)
tree.heading("Harga", text="Harga (Float)", anchor=tk.CENTER)

# Lebar Kolom
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("Nama", width=250, anchor=tk.W)
tree.column("Harga", width=150, anchor=tk.E)


# Jalankan aplikasi
root.mainloop()