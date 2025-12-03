import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Struktur Data Array 2 Dimensi (List Bersarang) Global ---
# List kosong yang akan diisi oleh input pengguna
data_mahasiswa_2d = []

def tampilkan_data_ke_tabel():
    """Membersihkan dan mengisi Treeview dengan data dari Array 2D Global."""
    
    # Bersihkan data lama
    for item in tree.get_children():
        tree.delete(item)
    
    # Iterasi melalui Array 2 Dimensi (List Bersarang)
    for i, baris in enumerate(data_mahasiswa_2d):
        
        # Ekstraksi dan penentuan tipe data
        nim = baris[0]          # String
        nama = baris[1]         # String
        nilai_float = baris[2]  # Floating Point
        
        # Format nilai IPK menjadi string dengan dua desimal
        nilai_format = f"{nilai_float:.2f}"
        
        # Nomor Urut (Integer)
        nomor = i + 1 

        # Masukkan baris data ke Treeview (Tabel)
        tree.insert('', 'end', values=(nomor, nim, nama, nilai_format))
        
    # Perbarui Label Total
    jumlah_mahasiswa_total = len(data_mahasiswa_2d)
    label_total_mahasiswa.config(text=f"Jumlah Total Mahasiswa: {jumlah_mahasiswa_total} orang")


def tambah_data_mahasiswa():
    """Mengambil input pengguna, memvalidasi tipe data, dan menambahkannya ke Array 2D."""
    
    # Ambil nilai dari input fields
    nim_input = entry_nim.get().strip()
    nama_input = entry_nama.get().strip()
    nilai_ipk_str = entry_nilai_ipk.get().strip()

    # Validasi Dasar
    if not nim_input or not nama_input or not nilai_ipk_str:
        messagebox.showerror("Error", "Semua kolom input wajib diisi.")
        return

    try:
        # --- Validasi Tipe Data Float (Nilai IPK) ---
        nilai_ipk_float = float(nilai_ipk_str)
        
        # Validasi Rentang IPK
        if not (0.00 <= nilai_ipk_float <= 4.00):
            messagebox.showerror("Error", "Nilai IPK harus dalam rentang 0.00 hingga 4.00.")
            return

        # --- Tambahkan Data ke Array 2D ---
        # Data baru adalah sub-list: [NIM (String), Nama (String), Nilai (Float)]
        data_baru = [nim_input, nama_input, nilai_ipk_float]
        data_mahasiswa_2d.append(data_baru)

        # Bersihkan input fields
        entry_nim.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        entry_nilai_ipk.delete(0, tk.END)
        
        # Tampilkan data terbaru ke tabel
        tampilkan_data_ke_tabel()

    except ValueError:
        # Menangani Error jika konversi ke float gagal
        messagebox.showerror("Error", "Input Nilai IPK tidak valid. Harap masukkan angka desimal (float).")


# --- 2. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title("Input Mandiri Data Mahasiswa (Array 2D)")
root.geometry("750x550")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul
tk.Label(root, text="Input Data Mahasiswa", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#F0FFFF", padx=10, pady=10)
frame_input.pack(pady=5)

tk.Label(frame_input, text="NIM (String):", bg="#F0FFFF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nim = tk.Entry(frame_input, width=20)
entry_nim.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Nama (String):", bg="#F0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=20)
entry_nama.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Nilai IPK (Float):", bg="#F0FFFF").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_nilai_ipk = tk.Entry(frame_input, width=20)
entry_nilai_ipk.grid(row=2, column=1, padx=5, pady=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambah ke Tabel (Array 2D)", command=tambah_data_mahasiswa, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, rowspan=3, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=700, bg="grey").pack(pady=10)

## 📊 Label Output Jumlah Total
label_total_mahasiswa = tk.Label(root, text="Jumlah Total Mahasiswa: 0 orang", 
                                 bg="#F0FFFF", fg="#8B0000", font=("Arial", 12, "bold"))
label_total_mahasiswa.pack(pady=5)

# --- 3. Tabel (Treeview) untuk Output Rincian ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("No", "NIM", "Nama", "Nilai"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("NIM", text="NIM", anchor=tk.CENTER)
tree.heading("Nama", text="Nama Mahasiswa", anchor=tk.CENTER)
tree.heading("Nilai", text="IPK (Float)", anchor=tk.CENTER)

# Lebar Kolom
tree.column("No", width=40, anchor=tk.CENTER)
tree.column("NIM", width=120, anchor=tk.CENTER)
tree.column("Nama", width=250, anchor=tk.W)
tree.column("Nilai", width=100, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()