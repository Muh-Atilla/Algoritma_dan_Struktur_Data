import tkinter as tk
from tkinter import ttk
from tkinter import END

# ===============================================
# 1. STRUKTUR DATA (Menggunakan Array/List Python)
# ===============================================

# Array/List Python ini menyimpan semua data absensi dengan statusnya.
DAFTAR_HADIR = [] 
KELAS_OPTIONS = ["Sisfo A", "Sisfo B", "Sisfo C"]

# --- FUNGSI DASAR ARRAY (Operasi Absensi) ---

def find_mahasiswa_index(nim: str):
    """Mencari indeks (posisi) mahasiswa berdasarkan NIM."""
    for i, mahasiswa in enumerate(DAFTAR_HADIR):
        if mahasiswa['nim'] == nim:
            return i
    return -1 

def tambah_data_absen(nim: str, nama: str, kelas: str, status: str):
    """Menambahkan mahasiswa ke Array dengan status awal (Hadir/Alfa)."""
    
    if find_mahasiswa_index(nim) != -1:
        return False, f"❌ Gagal Tambah! Mahasiswa dengan NIM {nim} sudah terdaftar absensi."
    
    # Tambah data ke Array dengan status yang ditentukan
    DAFTAR_HADIR.append({"nim": nim, "nama": nama, "kelas": kelas, "status_hadir": status})
    return True, f"✅ Mahasiswa {nim} ({kelas}) berhasil terdaftar dengan status: {status}."

def ubah_status(nim: str, status_baru: str):
    """Mengubah status mahasiswa yang sudah terdaftar (Update Record)."""
    
    index = find_mahasiswa_index(nim)
    
    if index == -1:
        return False, f"❌ Gagal Ubah Status! NIM {nim} tidak ditemukan dalam daftar hadir."
        
    # UPDATE data di dalam Array
    DAFTAR_HADIR[index]['status_hadir'] = status_baru
    return True, f"🔄 Status NIM {nim} berhasil diubah menjadi {status_baru}."

def cek_status_hadir(nim: str):
    """Mencari dan mengembalikan status kehadiran mahasiswa."""
    
    index = find_mahasiswa_index(nim)
    
    if index == -1:
        return False, f"❌ NIM {nim} belum terdaftar absensi."
        
    status = DAFTAR_HADIR[index]['status_hadir']
    return True, f"👀 Status Kehadiran NIM {nim}: {status}."

# --- FUNGSI GUI (Tampilan & Handler) ---

def tampilkan_daftar_hadir():
    """Memperbarui Treeview agar daftar hadir terlihat."""
    
    for item in tree.get_children():
        tree.delete(item)

    if not DAFTAR_HADIR:
        label_status.config(text="Daftar Absensi kosong.", fg="#8B0000")
        return

    hadir_count = sum(1 for data in DAFTAR_HADIR if data['status_hadir'] == 'Hadir')
    alfa_count = sum(1 for data in DAFTAR_HADIR if data['status_hadir'] == 'Alfa')
    
    # Tampilkan seluruh Array
    for i, data in enumerate(DAFTAR_HADIR):
        posisi = f"No. {i + 1}"
        status_warna = 'green' if data['status_hadir'] == 'Hadir' else 'red'
        
        tree.insert('', 'end', 
                    values=(posisi, data['nim'], data['nama'], data['kelas'], data['status_hadir']),
                    tags=(status_warna,)) 
        
    # Konfigurasi warna baris untuk visualisasi status
    tree.tag_configure('green', foreground='#006400') 
    tree.tag_configure('red', foreground='#B22222') 
        
    label_status.config(text=f"Total: {len(DAFTAR_HADIR)}. Hadir: {hadir_count}. Alfa: {alfa_count}.", fg="#004D40")

def tampilkan_notifikasi(pesan, sukses=False):
    """Menampilkan pesan status atau error."""
    warna = "red" if not sukses else "green"
    label_error_feedback.config(text=pesan, fg=warna, font=("Arial", 10, "bold"))

def hapus_notifikasi():
    """Menghapus pesan error/status."""
    label_error_feedback.config(text="", fg="red")

def validate_input():
    """Validasi input dasar untuk NIM, Nama, dan Kelas."""
    nim_input = entry_nim.get().strip()
    nama_input = entry_nama.get().strip()
    kelas_input = var_kelas.get() 
    
    if not nim_input or not nama_input or kelas_input not in KELAS_OPTIONS:
        tampilkan_notifikasi("Gagal: NIM, Nama, dan Kelas wajib diisi untuk pendaftaran.")
        return None, None, None
    return nim_input, nama_input, kelas_input

def handle_absen_hadir():
    """Tombol ABSEN MASUK (Tambah Array dengan status Hadir)."""
    hapus_notifikasi()
    nim, nama, kelas = validate_input()
    if nim is None: return

    sukses, pesan = tambah_data_absen(nim, nama, kelas, "Hadir")
    tampilkan_notifikasi(pesan, sukses)
    
    if sukses:
        entry_nim.delete(0, END)
        entry_nama.delete(0, END)
        tampilkan_daftar_hadir()

def handle_absen_alfa():
    """Tombol TANDAI ALFA BARU (Tambah Array dengan status Alfa)."""
    hapus_notifikasi()
    nim, nama, kelas = validate_input()
    if nim is None: return

    sukses, pesan = tambah_data_absen(nim, nama, kelas, "Alfa")
    tampilkan_notifikasi(pesan, sukses)
    
    if sukses:
        entry_nim.delete(0, END)
        entry_nama.delete(0, END)
        tampilkan_daftar_hadir()
        
def handle_ubah_ke_alfa():
    """Tombol UBAH KE ALFA (Update status menjadi Alfa)."""
    hapus_notifikasi()
    nim_input = entry_nim.get().strip()

    if not nim_input:
        tampilkan_notifikasi("Gagal: NIM harus diisi untuk mengubah status.")
        return

    sukses, pesan = ubah_status(nim_input, "Alfa")
    tampilkan_notifikasi(pesan, sukses)
    
    if sukses:
        tampilkan_daftar_hadir()

def handle_ubah_ke_hadir():
    """Tombol UBAH KE HADIR (Update status menjadi Hadir)."""
    hapus_notifikasi()
    nim_input = entry_nim.get().strip()

    if not nim_input:
        tampilkan_notifikasi("Gagal: NIM harus diisi untuk mengubah status.")
        return

    # Panggil fungsi ubah_status dengan status baru: "Hadir"
    sukses, pesan = ubah_status(nim_input, "Hadir")
    tampilkan_notifikasi(pesan, sukses)
    
    if sukses:
        tampilkan_daftar_hadir()
        
def handle_cek_absen():
    """Tombol CEK KEHADIRAN (Mencari status di Array)."""
    hapus_notifikasi()
    nim_input = entry_nim.get().strip()
    
    if not nim_input:
        tampilkan_notifikasi("Gagal: NIM harus diisi untuk Cek Kehadiran.")
        return

    sukses, pesan = cek_status_hadir(nim_input)
    tampilkan_notifikasi(pesan, sukses)
    
# ===============================================
# 2. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Tipe Data Perancangan Array - Absensi Kelas (Update Record)") 
root.geometry("1000x650") # Lebar diperluas sedikit
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"SIMULASI ABSENSI KELAS (ARRAY DENGAN UPDATE STATUS)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Input Data:", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=6, sticky="w", pady=5)
         
tk.Label(frame_input, text="NIM:", bg="#E0FFFF").grid(row=1, column=0, sticky="w", padx=5)
entry_nim = tk.Entry(frame_input, width=15)
entry_nim.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="Nama:", bg="#E0FFFF").grid(row=1, column=2, sticky="w", padx=5)
entry_nama = tk.Entry(frame_input, width=30)
entry_nama.grid(row=1, column=3, padx=5)

tk.Label(frame_input, text="Kelas:", bg="#E0FFFF").grid(row=1, column=4, sticky="w", padx=5)
var_kelas = tk.StringVar(root)
var_kelas.set(KELAS_OPTIONS[0]) 

dropdown_kelas = ttk.Combobox(frame_input, textvariable=var_kelas, values=KELAS_OPTIONS, state="readonly", width=8)
dropdown_kelas.grid(row=1, column=5, padx=5)

# --- Label Feedback Error Khusus ---
label_error_feedback = tk.Label(frame_input, text="Siap menerima absensi.", bg="#E0FFFF", fg="blue")
label_error_feedback.grid(row=2, column=0, columnspan=6, pady=5)

# Tombol Operasi Utama
frame_tombol = tk.Frame(frame_input, bg="#E0FFFF")
frame_tombol.grid(row=3, column=0, columnspan=6, pady=10, sticky="nsew")

# BARIS PERTAMA: TAMBAH DATA BARU
tk.Label(frame_tombol, text="TAMBAH DATA BARU (Lengkapi NIM, Nama, Kelas):", 
         bg="#E0FFFF", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=5)

# 1. ABSEN MASUK (Tambah Hadir)
tk.Button(frame_tombol, text="1. ABSEN MASUK (Hadir)", command=handle_absen_hadir, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, sticky="w")
          
# 2. TANDAI ALFA BARU (Tambah Alfa)
tk.Button(frame_tombol, text="2. TANDAI ALFA BARU (Tidak Hadir)", command=handle_absen_alfa, 
          bg="#CD5C5C", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=1, padx=5, sticky="w")
          
# BARIS KEDUA: UPDATE DAN CEK
tk.Label(frame_tombol, text="UPDATE STATUS & CEK (Hanya perlukan NIM):", 
         bg="#E0FFFF", font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=3, sticky="w", pady=5)

# 3. UBAH KE ALFA (Update Record)
tk.Button(frame_tombol, text="3. UBAH KE ALFA", command=handle_ubah_ke_alfa, 
          bg="#FF8C00", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, sticky="w")
          
# 4. UBAH KE HADIR (Tombol Baru)
tk.Button(frame_tombol, text="4. UBAH KE HADIR", command=handle_ubah_ke_hadir, 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=1, padx=5, sticky="w")
          
# 5. CEK KEHADIRAN (Mencari Status)
tk.Button(frame_tombol, text="5. CEK STATUS KEHADIRAN", command=handle_cek_absen, 
          bg="#FFD700", fg="black", font=("Arial", 10, "bold")).grid(row=3, column=2, padx=5, sticky="w")
          
# --- Status & Tabel ---

tk.Frame(root, height=1, width=950, bg="grey").pack(pady=10)

label_status = tk.Label(root, text="Daftar hadir siap.", 
                            bg="#F0FFFF", fg="#8B0000", font=("Arial", 11, "bold"))
label_status.pack(pady=5)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("No", "NIM", "Nama", "Kelas", "Status"), show='headings') 
tree.pack(fill="both", expand=True)

tree.heading("No", text="No. Urut", anchor=tk.CENTER)
tree.heading("NIM", text="NIM (Data)", anchor=tk.CENTER)
tree.heading("Nama", text="Nama (Data)", anchor=tk.CENTER)
tree.heading("Kelas", text="Kelas", anchor=tk.CENTER)
tree.heading("Status", text="Status", anchor=tk.CENTER) 

tree.column("No", width=80, anchor=tk.CENTER)
tree.column("NIM", width=120, anchor=tk.CENTER)
tree.column("Nama", width=250, anchor=tk.W)
tree.column("Kelas", width=100, anchor=tk.CENTER)
tree.column("Status", width=100, anchor=tk.CENTER)

tampilkan_daftar_hadir()
root.mainloop()