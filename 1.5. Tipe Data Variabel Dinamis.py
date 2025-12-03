import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- 1. Class Mahasiswa dengan Variabel Dinamis ---

class Mahasiswa:
    # --- VARIABEL STATIS (CLASS VARIABLE) DIPERBARUI ---
    # Nilai ini dibagi oleh semua objek Mahasiswa
    NAMA_UNIVERSITAS = "Universitas Sulawesi Barat" 
    
    def __init__(self, nim, nama, ipk):
        # --- VARIABEL DINAMIS (INSTANCE VARIABLES) ---
        # Setiap objek Mahasiswa memiliki nilai ini sendiri.
        self.nim = nim      
        self.nama = nama    
        self.ipk = ipk      
        
# --- 2. Struktur Data Utama (List of Mahasiswa Objects) ---
data_mahasiswa = []

def tampilkan_data_mahasiswa():
    """Membersihkan dan mengisi Treeview dengan data mahasiswa."""
    
    for item in tree.get_children():
        tree.delete(item)
    
    for i, data in enumerate(data_mahasiswa): 
        
        # Mengakses Variabel Dinamis (IPK)
        ipk_format = f"{data.ipk:.2f}" 
        
        # Masukkan data ke Treeview
        tree.insert('', 'end', values=(
            i + 1, 
            data.nim,
            data.nama,
            ipk_format,
            Mahasiswa.NAMA_UNIVERSITAS  # Mengakses Variabel Statis (Universitas Sulawesi Barat)
        ))
    
    # Menampilkan total objek yang ada
    label_total_data.config(text=f"Total Data Mahasiswa (Objek Dinamis): {len(data_mahasiswa)}")


def tambah_data_mahasiswa():
    """Mengambil input, memvalidasi, dan membuat objek Mahasiswa baru (Variabel Dinamis)."""
    
    nim_input = entry_nim.get().strip()
    nama_input = entry_nama.get().strip()
    ipk_input_str = entry_ipk.get().strip()
    
    if not all([nim_input, nama_input, ipk_input_str]):
        messagebox.showerror("Error Input", "Semua kolom wajib diisi.")
        return

    try:
        # Validasi dan Konversi IPK ke Float
        ipk_float = float(ipk_input_str)
        if not (0.00 <= ipk_float <= 4.00):
            messagebox.showerror("Error Input", "IPK harus berupa angka desimal antara 0.00 dan 4.00.")
            return
        
        # --- Membuat Objek Mahasiswa Baru ---
        mahasiswa_baru = Mahasiswa(nim_input, nama_input, ipk_float)
        
        data_mahasiswa.append(mahasiswa_baru)

        # Bersihkan input dan tampilkan data
        entry_nim.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        entry_ipk.delete(0, tk.END)
        entry_nim.focus_set()
        
        tampilkan_data_mahasiswa()

    except ValueError:
        messagebox.showerror("Error Tipe Data", "IPK harus diisi dengan angka desimal (Float).")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return

# --- 3. Konfigurasi Jendela Aplikasi (Tkinter GUI) ---
root = tk.Tk()
root.title(f"Konsep Variabel Dinamis (Instance Variable)")
root.geometry("800x500")
root.configure(bg="#F0FFFF") 

## 🏷️ Judul
tk.Label(root, text=f"KONSEP VARIABEL DINAMIS PADA DATA MAHASISWA ({Mahasiswa.NAMA_UNIVERSITAS})", 
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

# Input IPK (Variabel Dinamis/Instans)
tk.Label(frame_input, text="IPK (Float 0.00-4.00):", bg="#E0FFFF").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_ipk = tk.Entry(frame_input, width=15)
entry_ipk.grid(row=1, column=1, padx=5, pady=5)

# Tombol Tambah
tk.Button(frame_input, text="Tambahkan Mahasiswa", command=tambah_data_mahasiswa, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, rowspan=2, padx=15, sticky="nsew")

# --- Garis Pemisah ---
tk.Frame(root, height=1, width=750, bg="grey").pack(pady=10)

## 📊 Label Output Total
label_total_data = tk.Label(root, text=f"Total Data Mahasiswa (Objek Dinamis): 0", 
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
tree = ttk.Treeview(frame_tabel, columns=("No", "NIM", "Nama", "IPK", "Univ"), show='headings')
tree.pack(fill="both", expand=True)

# Definisi Judul Kolom
tree.heading("No", text="No.", anchor=tk.CENTER)
tree.heading("NIM", text="NIM (Dinamis)", anchor=tk.CENTER)
tree.heading("Nama", text="Nama (Dinamis)", anchor=tk.CENTER)
tree.heading("IPK", text="IPK (Dinamis)", anchor=tk.CENTER)
tree.heading("Univ", text="Universitas (Statis)", anchor=tk.CENTER) 

# Lebar Kolom
tree.column("No", width=50, anchor=tk.CENTER)
tree.column("NIM", width=120, anchor=tk.CENTER)
tree.column("Nama", width=200, anchor=tk.W)
tree.column("IPK", width=120, anchor=tk.CENTER)
tree.column("Univ", width=200, anchor=tk.CENTER)


# Jalankan aplikasi
root.mainloop()