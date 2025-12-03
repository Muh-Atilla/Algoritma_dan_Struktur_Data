import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Class Mahasiswa dengan Variabel Statis ---

class Mahasiswa:
    # --- VARIABEL STATIS (CLASS VARIABLES) ---
    # Dibagi oleh semua objek Mahasiswa
    NAMA_UNIVERSITAS = "Universitas Cerdas IT"
    counter_mahasiswa = 0

    def __init__(self, nim, nama, lulus):
        self.nim = nim      # Instance Variable
        self.nama = nama    # Instance Variable
        self.lulus = lulus  # Instance Variable
        
        # Setiap kali objek baru dibuat, tambah hitungan variabel statis
        Mahasiswa.counter_mahasiswa += 1

    def get_info(self):
        # Mengakses Variabel Statis menggunakan nama Class
        status = "LULUS" if self.lulus else "TIDAK LULUS"
        return f"{self.nim} - {self.nama} ({status}) | Univ: {Mahasiswa.NAMA_UNIVERSITAS}"

# --- 2. Struktur Data Utama (List of Mahasiswa Objects) ---
data_mahasiswa = []

def tampilkan_data_mahasiswa():
    """Membersihkan dan mengisi Treeview dengan data mahasiswa."""
    
    for item in tree.get_children():
        tree.delete(item)
    
    for i, data in enumerate(data_mahasiswa): 
        
        # Format Status Lulus (Boolean)
        status_lulus_str = "LULUS" if data.lulus else "TIDAK LULUS"
        
        # Masukkan data ke Treeview
        tree.insert('', 'end', values=(
            i + 1, 
            data.nim,
            data.nama,
            status_lulus_str,
            Mahasiswa.NAMA_UNIVERSITAS  # Mengakses Variabel Statis
        ))
    
    # Menampilkan Variabel Statis (Total Mahasiswa)
    label_total_data.config(text=f"Total Mahasiswa Tercatat (Variabel Statis): {Mahasiswa.counter_mahasiswa}")


def tambah_data_mahasiswa():
    """Mengambil input dan membuat objek Mahasiswa baru."""
    
    nim_input = entry_nim.get().strip()
    nama_input = entry_nama.get().strip()
    
    # Status Lulus diambil dari 1 (True) atau 0 (False)
    lulus_input_str = var_lulus.get()
    
    if not all([nim_input, nama_input, lulus_input_str]):
        messagebox.showerror("Error Input", "Semua kolom wajib diisi.")
        return

    try:
        # Konversi Status Lulus ke Boolean
        lulus_bool = True if lulus_input_str == "1" else False
        
        # --- Membuat Objek Mahasiswa Baru ---
        mahasiswa_baru = Mahasiswa(nim_input, nama_input, lulus_bool)
        
        # Menambahkan Objek ke List Global
        data_mahasiswa.append(mahasiswa_baru)

        # Bersihkan input dan tampilkan data
        entry_nim.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        var_lulus.set("1") # Reset ke LULUS
        entry_nim.focus_set()
        
        tampilkan_data_mahasiswa()

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return

# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Konsep Variabel Statis (Class Variable)")
root.geometry("800x500")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul
tk.Label(root, text=f"KONSEP VARIABEL STATIS PADA DATA MAHASISWA", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

# Input Baris 1: NIM dan Nama
tk.Label(frame_input, text="NIM (String):", bg="#E0FFFF").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nim = tk.Entry(frame_input, width=15)
entry_nim.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Nama (String):", bg="#E0FFFF").grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_nama = tk.Entry(frame_input, width=25)
entry_nama.grid(row=0, column=3, padx=5, pady=5)

# Input Baris 2: Status Lulus (Boolean)
var_lulus = tk.StringVar(root)
var_lulus.set("1") # Default LULUS (True)
lulus_options = [("LULUS (1)", "1"), ("TIDAK LULUS (0)", "0")]
tk.Label(frame_input, text="Status Lulus (Boolean):", bg="#E0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)

# Membuat Radio Buttons untuk Status Lulus
for i, (teks, nilai) in enumerate(lulus_options):
    tk.Radiobutton(frame_input, text=teks, variable=var_lulus, value=nilai, bg="#E0FFFF").grid(row=1, column=1 + i, sticky="w", padx=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Mahasiswa", command=tambah_data_mahasiswa, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=750, bg="grey").pack(pady=10)

## 📊 Label Output Total (Menampilkan Nilai Statis)
label_total_data = tk.Label(root, text=f"Total Mahasiswa Tercatat (Variabel Statis): 0", 
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
tree = ttk.Treeview(frame_tabel, columns=("No", "NIM", "Nama", "StatusLulus", "Univ"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("NIM", text="NIM", anchor=tk.CENTER)
tree.heading("Nama", text="Nama", anchor=tk.CENTER)
tree.heading("StatusLulus", text="Status Lulus (Boolean)", anchor=tk.CENTER)
tree.heading("Univ", text="Nama Universitas (Statis)", anchor=tk.CENTER) # Menampilkan Nilai Statis

# Lebar Kolom
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("NIM", width=120, anchor=tk.CENTER)
tree.column("Nama", width=200, anchor=tk.W)
tree.column("StatusLulus", width=150, anchor=tk.CENTER)
tree.column("Univ", width=180, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()