import tkinter as tk
from tkinter import ttk
from tkinter import END
from tkinter import messagebox

# ===============================================
# 1. DEFINISI STRUKTUR DATA (STRUCT + UNION)
# ===============================================

# Kelas yang mensimulasikan UNION
class IdentitasUnion:
    """Union: Hanya dapat menyimpan satu jenis identitas unik pada satu waktu."""
    def __init__(self):
        # LOKASI MEMORI BERSAMA
        self._memory = {}
        self.active_type = "Tidak Ada"

    def set_value(self, key, value, type_name):
        """Fungsi Union: Menimpa nilai lama di lokasi memori bersama."""
        self._memory = {key: value} # Menimpa data sebelumnya
        self.active_type = type_name

    def get_value(self):
        """Mengambil nilai yang tersimpan dan tipe aktifnya."""
        if not self._memory:
            return "Key Kosong", "KOSONG", "Tidak Ada"
        
        key = list(self._memory.keys())[0]
        value = self._memory[key]
        return key, value, self.active_type

# Kelas yang mensimulasikan STRUCT (Record) yang berisi Union
class RecordUnion:
    """Struct: Menyimpan Nama (lokasi memori sendiri) dan Identitas Unik (Union)."""
    def __init__(self, nama):
        # Anggota Struct (Lokasi Memori Normal)
        self.nama = nama
        # Anggota Union (Lokasi Memori Bersama)
        self.identitas_unik = IdentitasUnion()
        self.is_set = False

# Inisialisasi Record yang berisi Union
record_data = RecordUnion(nama="Belum Terdaftar")


# --- 2. LOGIKA GUI (Handler Tombol) ---

def tampilkan_data_union(pesan=""):
    """Memperbarui tampilan status Union."""
    key, value, tipe = record_data.identitas_unik.get_value()
    
    label_nama.config(text=f"Nama (Struct): {record_data.nama}",
                      fg="#004D40", font=("Arial", 14, "bold"))
    
    label_tipe.config(text=f"Tipe Aktif (Union): {tipe}", 
                      fg="#1E90FF", font=("Arial", 12, "bold")) 
    label_nilai.config(text=f"Nilai Tersimpan (Union): {value}", 
                       fg="#3CB371" if tipe != "Tidak Ada" else "black", 
                       font=("Arial", 12, "bold"))
    
    if pesan:
        tampilkan_notifikasi(pesan, True)

def tampilkan_notifikasi(pesan, sukses=False):
    """Menampilkan pesan status atau error."""
    warna = "red" if not sukses else "green"
    label_error_feedback.config(text=pesan, fg=warna, font=("Arial", 10, "bold"))

def hapus_notifikasi():
    """Menghapus pesan error/status."""
    label_error_feedback.config(text="", fg="red")

# --- Handlers Utama ---

def handle_input(tipe):
    hapus_notifikasi()
    input_nama = entry_nama.get().strip()
    input_val = entry_id.get().strip()

    if not input_nama:
        tampilkan_notifikasi("Gagal: Nama wajib diisi.")
        return
    if not input_val:
        tampilkan_notifikasi("Gagal: Nilai Identitas wajib diisi.")
        return

    # Update Anggota Struct (Nama)
    record_data.nama = input_nama
    record_data.is_set = True
    
    try:
        if tipe == "PEGAWAI":
            id_int = int(input_val)
            # OPERASI UNION: Menimpa nilai lama di Union
            record_data.identitas_unik.set_value("ID_Pegawai", id_int, "ID Pegawai (INT)")
            pesan = f"✅ Record diisi dengan Nama dan ID Pegawai (INT). Data Union DITIMPA."
        
        elif tipe == "MAHASISWA":
            # OPERASI UNION: Menimpa nilai lama di Union
            record_data.identitas_unik.set_value("NIM", input_val, "NIM Mahasiswa (STRING)")
            pesan = f"✅ Record diisi dengan Nama dan NIM Mahasiswa (STRING). Data Union DITIMPA."
            
        elif tipe == "KTP":
            # OPERASI UNION: Menimpa nilai lama di Union
            record_data.identitas_unik.set_value("No_KTP", input_val, "No. KTP (STRING Panjang)")
            pesan = f"✅ Record diisi dengan Nama dan No. KTP (STRING). Data Union DITIMPA."
            
        entry_id.delete(0, END)
        tampilkan_data_union(pesan)
        
    except ValueError:
        if tipe == "PEGAWAI":
             tampilkan_notifikasi("Gagal: ID Pegawai harus berupa angka (Integer).")
        else:
             tampilkan_notifikasi("Input ID/NIM/KTP Gagal.")


# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title(f"Tipe Data Perancangan Struct yang Berisi Union") 
root.geometry("700x550") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
tk.Label(root, text=f"STRUCT YANG BERISI UNION: MEMORI GABUNGAN + MEMORI NORMAL", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Struct (Nama) memiliki memori sendiri. Union (ID/NIM/KTP) berbagi memori.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Nama:", bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Identitas (ID/NIM/KTP):", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
entry_id = tk.Entry(frame_input, width=25)
entry_id.grid(row=1, column=1, padx=5, pady=5)

# Tombol Operasi Utama
frame_tombol = tk.Frame(frame_input, bg="#E0FFFF")
frame_tombol.grid(row=2, column=0, columnspan=4, pady=10)

# Tombol Set Nilai
tk.Button(frame_tombol, text="Set: ID Pegawai (INT)", command=lambda: handle_input("PEGAWAI"), 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
          
tk.Button(frame_tombol, text="Set: NIM Mhs (STRING)", command=lambda: handle_input("MAHASISWA"), 
          bg="#FF8C00", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
          
tk.Button(frame_tombol, text="Set: No. KTP (STRING Pjg)", command=lambda: handle_input("KTP"), 
          bg="#3CB371", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
          
# Label Feedback Error
label_error_feedback = tk.Label(frame_input, text="Masukkan Nama dan ID.", bg="#E0FFFF", fg="blue")
label_error_feedback.grid(row=3, column=0, columnspan=4, pady=5)

# --- Status Struct & Union ---
tk.Frame(root, height=1, width=650, bg="grey").pack(pady=10)

# VISUALISASI STRUCT (Nama - Memori Normal)
tk.Label(root, text="DATA STRUCT (MEMORI NORMAL)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 12, "bold")).pack(pady=5)

label_nama = tk.Label(root, text="Nama (Struct): Belum Terdaftar", 
                            bg="#CCFFCC", # Latar hijau muda untuk Struct
                            fg="#004D40", font=("Arial", 14, "bold"),
                            padx=20, pady=5)
label_nama.pack()

# VISUALISASI UNION (Identitas Unik - Memori Bersama)
tk.Label(root, text="DATA UNION (LOKASI MEMORI BERSAMA)", 
         bg="#F0FFFF", fg="#B22222", font=("Arial", 12, "bold")).pack(pady=5)

label_tipe = tk.Label(root, text="Tipe Aktif (Union): Tidak Ada", 
                            bg="#ADD8E6", # Latar biru muda untuk kotak Union
                            fg="blue", font=("Arial", 14, "bold"),
                            padx=20, pady=5)
label_tipe.pack()

label_nilai = tk.Label(root, text="Nilai Tersimpan (Union): KOSONG", 
                            bg="#ADD8E6", # Latar biru muda
                            fg="black", font=("Arial", 14, "bold"),
                            padx=20, pady=5)
label_nilai.pack()

tampilkan_data_union()
root.mainloop()