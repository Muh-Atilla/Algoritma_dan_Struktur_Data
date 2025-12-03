import tkinter as tk
from tkinter import ttk
from tkinter import END
from tkinter import messagebox

# ===============================================
# 1. DEFINISI STRUKTUR DATA (LINKED LIST)
# ===============================================

# Kelas Node (Struktur Item Pesanan)
class Node:
    """Struktur Node: Berisi Data Barang, Kuantitas, dan Pointer."""
    def __init__(self, id_barang, nama_barang, harga, jumlah):
        # Bagian Data (Struktur Item Pesanan)
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.harga = harga
        self.jumlah = jumlah # Kuantitas/Jumlah Barang
        # Bagian Pointer/Link
        self.next = None 

# Kelas Linked List (Struktur Daftar Pesanan)
class PesananList:
    """Struktur Pengelola yang berisi Head (Node pertama)."""
    def __init__(self):
        self.head = None 

    def is_empty(self):
        """Cek apakah list pesanan kosong."""
        return self.head is None
        
    def find_node(self, id_barang):
        """Mencari Node berdasarkan ID Barang dan mengembalikan Node jika ditemukan."""
        current = self.head
        while current:
            if current.id_barang == id_barang:
                return current
            current = current.next
        return None

    def add_to_pesanan(self, id_barang, nama_barang, harga, jumlah):
        """Menambahkan Node baru atau Mengupdate jumlah jika barang sudah ada."""
        
        existing_node = self.find_node(id_barang)
        
        if existing_node:
            # Barang sudah ada, hanya update kuantitas (Operasi UPDATE)
            existing_node.jumlah += jumlah
            return True, f"🔄 Kuantitas {nama_barang} di pesanan diupdate. Total: {existing_node.jumlah}"
        else:
            # Barang baru, buat Node baru dan tambahkan di akhir (Operasi INSERT)
            new_node = Node(id_barang, nama_barang, harga, jumlah)
            
            if self.is_empty():
                self.head = new_node
            else:
                last_node = self.head
                while last_node.next:
                    last_node = last_node.next
                last_node.next = new_node
                
            return True, f"✅ {nama_barang} berhasil ditambahkan ke pesanan ({jumlah} unit)."

    def delete_by_id(self, id_barang):
        """Menghapus Node berdasarkan ID Barang (Batalkan pesanan item)."""
        current = self.head
        prev = None

        if current and current.id_barang == id_barang:
            self.head = current.next 
            return True

        while current and current.id_barang != id_barang:
            prev = current
            current = current.next

        if current is None:
            return False

        # Node ditemukan dan dihapus
        prev.next = current.next
        return True

    def calculate_total(self):
        """Menghitung total biaya dari semua item pesanan."""
        total = 0
        current = self.head
        while current:
            total += (current.harga * current.jumlah)
            current = current.next
        return total

    def display_data(self):
        """Mengambil data semua Node dalam bentuk list."""
        elements = []
        current = self.head
        while current:
            elements.append({
                "id_barang": current.id_barang,
                "nama_barang": current.nama_barang,
                "harga": current.harga,
                "jumlah": current.jumlah,
                "sub_total": current.harga * current.jumlah
            })
            current = current.next
        return elements

# Inisialisasi Linked List Daftar Pesanan
daftar_pesanan = PesananList()


# --- 2. LOGIKA GUI (Handler Tombol) ---

def tampilkan_data_list():
    """Memperbarui Treeview dengan data dari Linked List."""
    
    for item in tree.get_children():
        tree.delete(item)

    data_list = daftar_pesanan.display_data()
    total_biaya = daftar_pesanan.calculate_total()

    if not data_list:
        label_status.config(text="Daftar Pesanan kosong. Total: Rp 0", fg="#8B0000")
        return

    # Tampilkan seluruh list
    for i, data in enumerate(data_list):
        posisi = f"Item {i + 1}"

        tree.insert('', 'end', values=(
            posisi, 
            data['id_barang'],
            data['nama_barang'],
            data['jumlah'],
            f"Rp {data['harga']:,}", 
            f"Rp {data['sub_total']:,}"
        ))
        
    label_status.config(text=f"Total Item: {len(data_list)}. TOTAL BIAYA PESANAN: Rp {total_biaya:,}", 
                        fg="#004D40", font=("Arial", 11, "bold"))

def tampilkan_notifikasi(pesan, sukses=False):
    """Menampilkan pesan status atau error."""
    warna = "red" if not sukses else "green"
    label_error_feedback.config(text=pesan, fg=warna, font=("Arial", 10, "bold"))

def hapus_notifikasi():
    """Menghapus pesan error/status."""
    label_error_feedback.config(text="", fg="red")

def validate_input(mode='insert'):
    """Validasi input dasar."""
    id_input = entry_id.get().strip()
    
    if mode == 'insert':
        nama_input = entry_nama.get().strip()
        harga_input = entry_harga.get().strip()
        jumlah_input = entry_jumlah.get().strip()

        if not all([id_input, nama_input, harga_input, jumlah_input]):
            tampilkan_notifikasi("Gagal: ID, Nama, Harga, dan Jumlah wajib diisi.")
            return None, None, None, None
        try:
            harga_int = int(harga_input)
            jumlah_int = int(jumlah_input)
            if harga_int <= 0 or jumlah_int <= 0:
                 tampilkan_notifikasi("Gagal: Harga dan Jumlah harus positif.")
                 return None, None, None, None
            return id_input, nama_input, harga_int, jumlah_int
        except ValueError:
            tampilkan_notifikasi("Gagal: Harga dan Jumlah harus berupa angka.")
            return None, None, None, None
    
    elif mode == 'delete' or mode == 'check':
        if not id_input:
            tampilkan_notifikasi("Gagal: ID wajib diisi untuk operasi ini.")
            return None
        return id_input

def handle_tambah_pesanan():
    """Tombol TAMBAH KE PESANAN (Insert/Update)."""
    hapus_notifikasi()
    id_barang, nama_barang, harga, jumlah = validate_input(mode='insert')
    if id_barang is None: return

    sukses, pesan = daftar_pesanan.add_to_pesanan(id_barang, nama_barang, harga, jumlah)
    
    if sukses:
        tampilkan_notifikasi(pesan, True)
        entry_id.delete(0, END)
        entry_nama.delete(0, END)
        entry_harga.delete(0, END)
        entry_jumlah.delete(0, END)
        tampilkan_data_list()

def handle_hapus_pesanan():
    """Tombol HAPUS DARI PESANAN (Delete by ID)."""
    hapus_notifikasi()
    id_input = validate_input(mode='delete')

    if id_input is None: return

    sukses = daftar_pesanan.delete_by_id(id_input)
    
    if sukses:
        tampilkan_notifikasi(f"✅ Item ID {id_input} berhasil dibatalkan/dihapus dari pesanan.", True)
        entry_id.delete(0, END)
        tampilkan_data_list()
    else:
        tampilkan_notifikasi(f"❌ Gagal Hapus! ID Barang {id_input} tidak ditemukan di pesanan.", False)
        
# ===============================================
# 3. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
# PERUBAHAN JUDUL
root.title(f"Perancangan Struktur - Linked List Toko Sumber Takwa") 
root.geometry("1000x650") 
root.configure(bg="#F0FFFF") 

## 🏷️ Judul Konsep
# PERUBAHAN HEADER
tk.Label(root, text=f"PERANCANGAN STRUKTUR: DAFTAR PESANAN TOKO SUMBER TAKWA", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 14, "bold")).pack(pady=10)

# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Input Item Pesanan:", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=8, sticky="w", pady=5)
         
tk.Label(frame_input, text="ID Barang:", bg="#E0FFFF").grid(row=1, column=0, sticky="w", padx=5)
entry_id = tk.Entry(frame_input, width=12)
entry_id.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="Nama:", bg="#E0FFFF").grid(row=1, column=2, sticky="w", padx=5)
entry_nama = tk.Entry(frame_input, width=20)
entry_nama.grid(row=1, column=3, padx=5)

tk.Label(frame_input, text="Harga/Unit:", bg="#E0FFFF").grid(row=1, column=4, sticky="w", padx=5)
entry_harga = tk.Entry(frame_input, width=12)
entry_harga.grid(row=1, column=5, padx=5)

tk.Label(frame_input, text="Jumlah:", bg="#E0FFFF").grid(row=1, column=6, sticky="w", padx=5)
entry_jumlah = tk.Entry(frame_input, width=10)
entry_jumlah.grid(row=1, column=7, padx=5)


# --- Label Feedback Error Khusus ---
label_error_feedback = tk.Label(frame_input, text="Siap menerima pesanan baru.", bg="#E0FFFF", fg="blue")
label_error_feedback.grid(row=2, column=0, columnspan=8, pady=5)

# Tombol Operasi Utama
frame_tombol = tk.Frame(frame_input, bg="#E0FFFF")
frame_tombol.grid(row=3, column=0, columnspan=8, pady=10, sticky="nsew")

# 1. TAMBAH KE PESANAN (Insert/Update)
tk.Button(frame_tombol, text="TAMBAH / UPDATE PESANAN", command=handle_tambah_pesanan, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
          
# 2. HAPUS DARI PESANAN (Delete)
tk.Button(frame_tombol, text="BATALKAN ITEM (Hapus ID)", command=handle_hapus_pesanan, 
          bg="#B22222", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
          
# --- Status & Tabel ---

tk.Frame(root, height=1, width=950, bg="grey").pack(pady=10)

label_status = tk.Label(root, text="Daftar Pesanan kosong. Total: Rp 0", 
                            bg="#F0FFFF", fg="#8B0000", font=("Arial", 11, "bold"))
label_status.pack(pady=5)

frame_tabel = tk.Frame(root)
frame_tabel.pack(padx=20, pady=10, fill="both", expand=True)

# Konfigurasi Treeview
tree = ttk.Treeview(frame_tabel, columns=("Posisi", "ID", "Nama Barang", "Jumlah", "Harga Unit", "Sub Total"), show='headings') 
tree.pack(fill="both", expand=True)

tree.heading("Posisi", text="No. Item", anchor=tk.CENTER)
tree.heading("ID", text="ID Barang", anchor=tk.CENTER)
tree.heading("Nama Barang", text="Nama Barang", anchor=tk.CENTER)
tree.heading("Jumlah", text="Jumlah", anchor=tk.CENTER)
tree.heading("Harga Unit", text="Harga Unit", anchor=tk.CENTER)
tree.heading("Sub Total", text="Sub Total", anchor=tk.CENTER)

tree.column("Posisi", width=80, anchor=tk.CENTER)
tree.column("ID", width=100, anchor=tk.CENTER)
tree.column("Nama Barang", width=250, anchor=tk.W)
tree.column("Jumlah", width=80, anchor=tk.CENTER)
tree.column("Harga Unit", width=120, anchor=tk.E)
tree.column("Sub Total", width=150, anchor=tk.E)

tampilkan_data_list()
root.mainloop()