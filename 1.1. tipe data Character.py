import tkinter as tk
from tkinter import messagebox, ttk

# --- Fungsi Utama: Memproses dan Menganalisis Nama ---

def proses_nama_mahasiswa():
    """Mengambil input nama, melakukan analisis string yang kompleks, dan menampilkan hasilnya dalam tabel."""
    
    nama_lengkap = entry_nama_lengkap.get().strip()
    
    # 1. Validasi Input Dasar
    if not nama_lengkap:
        messagebox.showerror("Error", "Nama mahasiswa tidak boleh kosong.")
        return

    try:
        # --- 2. Analisis String & Tipe Data Boolean ---
        
        # Tipe Data Integer: Panjang total karakter
        panjang_nama_total = len(nama_lengkap)
        
        # Tipe Data Boolean: Apakah nama mengandung spasi (Nama Majemuk)?
        is_majemuk = ' ' in nama_lengkap
        
        # Validasi Panjang Nama
        if panjang_nama_total < 3:
            messagebox.showwarning("Peringatan", "Nama terlalu pendek.")
            return
        if panjang_nama_total > 50:
            messagebox.showwarning("Peringatan", "Nama terlalu panjang (maksimal 50 karakter disarankan).")
            return

        # Pemisahan dan Komponen Nama
        komponen_nama = nama_lengkap.split()
        nama_depan = komponen_nama[0]
        nama_belakang = " ".join(komponen_nama[1:]) if len(komponen_nama) > 1 else "(T/A)"
        
        # --- 3. Manipulasi String ---
        
        # Operasi Urutan Terbalik (Slicing)
        nama_depan_terbalik = nama_depan[::-1]
        
        # Operasi Pengubahan Kasus (Case Conversion)
        nama_kapital = nama_lengkap.upper()
        nama_title = nama_lengkap.title() # Huruf Kapital di Setiap Kata
        
        # --- 4. Persiapan Data untuk Tabel ---
        
        data_analisis = [
            ("Nama Lengkap (String)", nama_lengkap),
            ("Nama Depan (String)", nama_depan),
            ("Nama Belakang (String)", nama_belakang),
            ("Panjang Total (Integer)", panjang_nama_total),
            ("Nama Majemuk (Boolean)", "YA" if is_majemuk else "TIDAK"),
            ("Urutan Depan Terbalik", nama_depan_terbalik),
            ("Nama Kapital (String)", nama_kapital),
            ("Nama Title Case (String)", nama_title)
        ]

        # 5. Tampilkan Hasil dalam Tabel
        tampilkan_tabel_analisis(data_analisis)

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")


def tampilkan_tabel_analisis(data):
    """Membuat atau membersihkan dan mengisi widget Treeview dengan hasil analisis."""
    
    # Bersihkan data lama
    for item in tree.get_children():
        tree.delete(item)
    
    # Masukkan data baru
    for jenis, nilai in data:
        tree.insert('', 'end', values=(jenis, nilai))


# --- Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title("Analisis Data Mahasiswa (Lengkap)")
root.geometry("650x550")
root.configure(bg="#F5FFFA") 

## ➡️ Frame Input
frame_input = tk.Frame(root, bg="#F5FFFA", pady=10)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Nama Lengkap Mahasiswa:", 
         bg="#F5FFFA", fg="#004D40", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
entry_nama_lengkap = tk.Entry(frame_input, bg="white", fg="black", font=("Arial", 12), width=35)
entry_nama_lengkap.pack(side=tk.LEFT, padx=10)

## 🛠️ Tombol Proses
tk.Button(root, text="Proses & Analisis Data", command=proses_nama_mahasiswa, 
          bg="#3CB371", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=600, bg="grey").pack(pady=10)

## 📊 Tabel Output Analisis
tk.Label(root, text="HASIL ANALISIS TIPE DATA STRING & OPERASI:", 
         bg="#F5FFFA", fg="#004D40", font=("Arial", 11, "bold")).pack(pady=5)

# Style untuk Treeview
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#B0C4DE", foreground="#000000")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

# Frame untuk Treeview
frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("JenisAnalisis", "NilaiHasil"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("JenisAnalisis", text="Jenis Analisis / Tipe Data", anchor=tk.W)
tree.heading("NilaiHasil", text="Nilai Hasil", anchor=tk.W)

# Lebar Kolom
tree.column("JenisAnalisis", width=250, anchor=tk.W)
tree.column("NilaiHasil", width=300, anchor=tk.W)


# Jalankan aplikasi
root.mainloop()