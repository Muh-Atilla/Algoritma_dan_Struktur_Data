import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Fungsi untuk menambah data ke tabel ---
def tambah_data():
    """Mengambil input, memvalidasi, menghitung diskon, dan menambahkannya ke Treeview."""
    nama_barang = entry_nama.get()
    harga_awal_str = entry_harga_awal.get()
    diskon_str = entry_diskon.get()
    
    # Validasi Input Dasar
    if not nama_barang or not harga_awal_str or not diskon_str:
        messagebox.showerror("Error", "Semua kolom harus diisi.")
        return

    try:
        # Konversi Harga Awal dan Diskon ke Floating Point (float)
        harga_awal = float(harga_awal_str)
        diskon_persen = float(diskon_str)
        
        # Validasi Nilai
        if harga_awal < 0 or diskon_persen < 0 or diskon_persen > 100:
            messagebox.showerror("Error", "Harga awal tidak boleh negatif, dan Diskon harus antara 0-100%.")
            return

        # --- 1. Perhitungan Harga Setelah Diskon (Menggunakan Float) ---
        diskon_desimal = diskon_persen / 100.0
        harga_setelah_diskon = harga_awal * (1.0 - diskon_desimal)
        
        # --- 2. Format Harga untuk Tampilan ---
        
        # Fungsi pembantu untuk memformat float ke string Rupiah dengan dua desimal
        def format_rupiah(nilai_float):
            # Format float ke string desimal dengan koma sebagai pemisah desimal
            return f"Rp {nilai_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        harga_awal_format = format_rupiah(harga_awal)
        harga_diskon_format = format_rupiah(harga_setelah_diskon)
        diskon_format = f"{diskon_persen}%"
        
        # --- 3. Tambahkan data ke tabel (Treeview) ---
        
        # Hitung nomor urut
        nomor_urut = len(tree.get_children()) + 1
        
        # Masukkan data dengan 4 nilai (No, Nama, Harga Awal, Diskon, Harga Setelah Diskon)
        tree.insert('', 'end', values=(nomor_urut, nama_barang, harga_awal_format, diskon_format, harga_diskon_format))
        
        # Bersihkan Entry setelah berhasil
        entry_nama.delete(0, tk.END)
        entry_harga_awal.delete(0, tk.END)
        entry_diskon.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Input harga atau diskon tidak valid. Masukkan angka desimal (float).")

# --- Konfigurasi Jendela Utama (Tkinter GUI) ---
root = tk.Tk()
root.title("Aplikasi Pendataan Harga Barang & Diskon")
root.geometry("800x500") # Diperbesar untuk menampung lebih banyak kolom
root.configure(bg="#E6E6FA") 

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E6E6FA", pady=10)
frame_input.pack(pady=10)

# Input Baris 1: Nama Barang
tk.Label(frame_input, text="Nama Barang:", bg="#E6E6FA", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nama = tk.Entry(frame_input, width=30, font=("Arial", 10))
entry_nama.grid(row=0, column=1, padx=5, pady=5)

# Input Baris 2: Harga Awal
tk.Label(frame_input, text="Harga Awal (Rp):", bg="#E6E6FA", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_harga_awal = tk.Entry(frame_input, width=30, font=("Arial", 10))
entry_harga_awal.grid(row=1, column=1, padx=5, pady=5)

# Input Baris 3: Diskon (%)
tk.Label(frame_input, text="Diskon (%):", bg="#E6E6FA", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_diskon = tk.Entry(frame_input, width=30, font=("Arial", 10))
entry_diskon.grid(row=2, column=1, padx=5, pady=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambah Data", command=tambah_data, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=3, padx=15, pady=5, sticky="nsew")

# --- Tabel (Treeview) ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_tabel)
scrollbar.pack(side="right", fill="y")

# Perhatikan: Nama kolom di sini harus sesuai dengan jumlah data yang dimasukkan (5 data)
tree = ttk.Treeview(frame_tabel, columns=("No", "NamaBarang", "HargaAwal", "Diskon", "HargaDiskon"), show='headings', yscrollcommand=scrollbar.set)
tree.pack(fill="both", expand=True)

scrollbar.config(command=tree.yview)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("NamaBarang", text="Nama Barang", anchor=tk.CENTER)
tree.heading("HargaAwal", text="Harga Awal", anchor=tk.CENTER)
tree.heading("Diskon", text="Diskon", anchor=tk.CENTER)
tree.heading("HargaDiskon", text="Harga Setelah Diskon", anchor=tk.CENTER)

# Lebar Kolom
tree.column("No", width=40, anchor=tk.CENTER)
tree.column("NamaBarang", width=200, anchor=tk.W)
tree.column("HargaAwal", width=150, anchor=tk.E)
tree.column("Diskon", width=80, anchor=tk.CENTER)
tree.column("HargaDiskon", width=150, anchor=tk.E)


# Jalankan aplikasi
root.mainloop()