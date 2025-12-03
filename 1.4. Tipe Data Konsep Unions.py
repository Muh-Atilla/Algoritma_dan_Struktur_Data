import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Struktur Union (Simulasi menggunakan Class) ---

class DataKelulusan:
    """
    Class ini mereplikasi Konsep Union: status_lulus dan keterangan 
    berbagi slot nilai yang sama.
    """
    def __init__(self):
        self._shared_data = {} 
        self.tipe_aktif = "None"

    def set_status_lulus(self, nilai_boolean):
        # Jalur 1: Boolean
        self._shared_data['nilai'] = bool(nilai_boolean)
        self.tipe_aktif = "Status Lulus (Boolean)"

    def set_keterangan(self, nilai_string):
        # Jalur 2: String
        self._shared_data['nilai'] = str(nilai_string)
        self.tipe_aktif = "Keterangan (String)"

    def get_nilai_aktif(self):
        # Mengambil nilai yang terakhir disimpan
        return self._shared_data.get('nilai', 'Kosong')

# --- 2. Struktur Data Utama (List of Structures) ---
data_mahasiswa = []

def tampilkan_data_mahasiswa():
    """Membersihkan dan mengisi Treeview dengan data mahasiswa."""
    
    for item in tree.get_children():
        tree.delete(item)
    
    for i, data in enumerate(data_mahasiswa): 
        
        # Mengakses nilai dari objek Union (DataKelulusan)
        objek_union = data['kelulusan']
        nilai_union = objek_union.get_nilai_aktif()
        tipe_union = objek_union.tipe_aktif
        
        # Format nilai union agar lebih mudah dibaca di tabel
        if tipe_union == "Status Lulus (Boolean)":
            nilai_tampil = "LULUS" if nilai_union is True else "TIDAK LULUS"
        else:
            # Nilai Tampil untuk Keterangan (String)
            nilai_tampil = str(nilai_union)
        
        # Masukkan data ke Treeview (Tabel)
        tree.insert('', 'end', values=(
            i + 1, 
            data['nim'],
            data['nama'],
            nilai_tampil,         # Nilai dari Union yang sudah diformat
            tipe_union            # Tipe Union
        ))
    
    label_total_data.config(text=f"Total Data Mahasiswa: {len(data_mahasiswa)}")


def tambah_data_mahasiswa():
    """Mengambil input dan membuat Structure yang berisi Union dengan VALIDASI LENGKAP."""
    
    nim_input = entry_nim.get().strip()
    nama_input = entry_nama.get().strip()
    nilai_union_str = entry_nilai_union.get().strip()
    tipe_union_pilihan = var_tipe_union.get()

    # **VALIDASI 1: Cek Kolom Kosong**
    if not all([nim_input, nama_input, nilai_union_str]):
        messagebox.showerror("Error Input", "NIM, Nama, dan Nilai/Status Wajib diisi.")
        return

    # Membuat objek Union baru
    data_kelulusan_baru = DataKelulusan()
    
    try:
        if tipe_union_pilihan == "Status Lulus (Boolean)":
            # Input Jalur Boolean: Hanya terima 1 (True) atau 0 (False)
            nilai_int = int(nilai_union_str)
            if nilai_int not in [0, 1]:
                 messagebox.showerror("Error Input", "Untuk 'Status Lulus', masukkan 1 (LULUS) atau 0 (TIDAK LULUS).")
                 return
                 
            data_kelulusan_baru.set_status_lulus(bool(nilai_int))
            
        elif tipe_union_pilihan == "Keterangan (String)":
            # Input Jalur String: Cukup memastikan input tidak kosong (sudah dilakukan di Validasi 1)
            data_kelulusan_baru.set_keterangan(nilai_union_str)
            
        else:
            messagebox.showerror("Error Internal", "Pilihan Tipe Union tidak valid.")
            return

    except ValueError:
        # Menangkap error jika konversi gagal (misalnya, Status Lulus diisi huruf)
        messagebox.showerror("Error Tipe Data", "Input tidak valid. Untuk jalur 'Status Lulus', input harus berupa **angka 1 atau 0**.")
        return

    # --- Membuat Struktur Utama (Dictionary) ---
    mahasiswa_baru = {
        'nim': nim_input,
        'nama': nama_input,
        'kelulusan': data_kelulusan_baru # Objek Union
    }
    
    data_mahasiswa.append(mahasiswa_baru)

    # Bersihkan input
    entry_nim.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    entry_nilai_union.delete(0, tk.END)
    entry_nim.focus_set()
    
    tampilkan_data_mahasiswa()


# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Konsep Unions (Simulasi Class) - Data Mahasiswa")
root.geometry("850x550")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul
tk.Label(root, text=f"KONSEP UNIONS (GABUNGAN) PADA DATA MAHASISWA", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

# Input Baris 1: NIM dan Nama (Bagian dari Structure)
tk.Label(frame_input, text="NIM (String):", bg="#E0FFFF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nim = tk.Entry(frame_input, width=15)
entry_nim.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Nama Mahasiswa (String):", bg="#E0FFFF").grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=3, padx=5, pady=5)


# Input Baris 2: Union
# PILIHAN UNION BARU
tipe_union_options = ["Status Lulus (Boolean)", "Keterangan (String)"]
var_tipe_union = tk.StringVar(root)
var_tipe_union.set(tipe_union_options[0]) 
tk.Label(frame_input, text="Pilih Data Union:", bg="#E0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tipe_menu = tk.OptionMenu(frame_input, var_tipe_union, *tipe_union_options)
tipe_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
tipe_menu.config(width=15)

tk.Label(frame_input, text="Status (1/0) / Keterangan:", bg="#E0FFFF").grid(row=1, column=2, sticky="w", padx=5, pady=5)
entry_nilai_union = tk.Entry(frame_input, width=25)
entry_nilai_union.grid(row=1, column=3, padx=5, pady=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Data", command=tambah_data_mahasiswa, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=800, bg="grey").pack(pady=10)

## 📊 Label Output Total
label_total_data = tk.Label(root, text="Total Data Mahasiswa: 0", 
                            bg="#F0FFFF", fg="#8B0000", font=("Arial", 11, "bold"))
label_total_data.pack(pady=5)

# --- 4. Tabel (Treeview) untuk Output Rincian ---

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("No", "NIM", "Nama", "NilaiUnion", "TipeUnion"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("NIM", text="NIM", anchor=tk.CENTER)
tree.heading("Nama", text="Nama", anchor=tk.CENTER)
# JUDUL KOLOM BARU
tree.heading("NilaiUnion", text="Lulus / Keterangan", anchor=tk.CENTER)
tree.heading("TipeUnion", text="Tipe Data Union", anchor=tk.CENTER)

# Lebar Kolom Optimal
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("NIM", width=120, anchor=tk.CENTER)
tree.column("Nama", width=250, anchor=tk.W)
tree.column("NilaiUnion", width=180, anchor=tk.CENTER)
tree.column("TipeUnion", width=150, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()