import tkinter as tk
from tkinter import END, messagebox

# ===============================================
# 1. ALGORITMA SHELL SORT (DIMODIFIKASI UNTUK PASANGAN)
# ===============================================

def shell_sort_pairs(data):
    """
    Shell Sort diimplementasikan untuk mengurutkan pasangan (index_modifikasi, karakter).
    Ini adalah fungsi pengurutan standar.
    """
    n = len(data)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            # Key adalah pasangan (indeks_modifikasi, karakter)
            key = data[i]
            j = i
            
            # Bandingkan berdasarkan indeks_modifikasi (elemen pertama di pasangan)
            while j >= gap and data[j - gap][0] > key[0]:
                data[j] = data[j - gap]
                j -= gap
            
            data[j] = key
        
        gap //= 2
    
    return data

# ===============================================
# 2. ALGORITMA UTAMA (MENGGUNAKAN SHELL SORT)
# ===============================================

def add_spaces_via_shell_sort(text):
    """
    Mengubah masalah penambahan spasi menjadi masalah pengurutan
    agar Shell Sort dapat digunakan.
    
    1. Parsing: Konversi teks menjadi daftar pasangan (posisi_target, karakter).
    2. Modifikasi Indeks: Tambahkan '0.1' ke posisi target untuk huruf kapital
       (sehingga spasi disisipkan setelahnya).
    3. Sortir: Gunakan Shell Sort untuk mengurutkan ulang.
    4. Rekonstruksi: Gabungkan karakter yang telah diurutkan.
    """
    if not text:
        return ""
    
    pairs = []
    
    # --- Tahap 1 & 2: Parsing dan Modifikasi Indeks ---
    # Kita menggunakan float untuk indeks agar bisa "menyisipkan" spasi.
    current_index = 0.0
    
    for char in text:
        # Jika huruf kapital dan bukan karakter pertama, tambahkan spasi sebelumnya.
        # Kita lakukan ini dengan memberikan indeks yang lebih rendah kepada spasi.
        if char.isupper() and current_index > 0.5:
            # Masukkan spasi di posisi tepat sebelum huruf kapital
            pairs.append((current_index - 0.1, ' ')) # Spasi mendapat prioritas indeks lebih rendah
            
        pairs.append((current_index, char))
        
        # Pindahkan indeks ke posisi berikutnya
        current_index += 1.0
        
    # --- Tahap 3: Sortir ---
    # Shell Sort akan mengurutkan semua karakter dan spasi berdasarkan posisi_target mereka.
    sorted_pairs = shell_sort_pairs(pairs)
    
    # --- Tahap 4: Rekonstruksi ---
    result = "".join([char for (index, char) in sorted_pairs if char != ' ' or index % 1 != 0.0])
    
    # Hapus spasi di awal jika ada
    return result.strip()


# --- 3. LOGIKA GUI (Handler Tombol) ---

def handle_process():
    """Menangani tombol proses dan menampilkan hasil."""
    
    input_text = entry_input.get().strip()
    
    if not input_text:
        messagebox.showwarning("Input Kosong", "Masukkan teks tanpa spasi terlebih dahulu.")
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, END)
        text_output.config(state=tk.DISABLED)
        return
        
    # Panggil algoritma yang menggunakan Shell Sort
    spaced_text = add_spaces_via_shell_sort(input_text)
    
    # Tampilkan hasil
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, END)
    text_output.insert(END, spaced_text)
    text_output.config(state=tk.DISABLED)
    
    label_status.config(text="✅ Pemrosesan Selesai menggunakan Shell Sort.", fg="green")
    

# ===============================================
# 4. KONFIGURASI TKINTER GUI
# ===============================================

root = tk.Tk()
root.title("Spasi Otomatis Menggunakan Shell Sort")
root.geometry("700x450")
root.configure(bg="#F0FFFF")

## 🏷️ Judul
tk.Label(root, text="🐚 ALGORITMA SPASI OTOMATIS (Menggunakan Shell Sort)", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Prinsip: Data dikonversi menjadi pasangan (Posisi Target, Karakter). Spasi diberi Posisi Target yang spesifik. Shell Sort mengurutkan ulang.", 
         bg="#F0FFFF", fg="black", font=("Arial", 10)).pack(pady=5)
         
# --- Frame Input ---
frame_input = tk.Frame(root, bg="#E0FFFF", padx=15, pady=15, bd=2, relief=tk.GROOVE)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Input Tanpa Spasi:", 
         bg="#E0FFFF", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)

entry_input = tk.Entry(frame_input, width=50)
entry_input.grid(row=0, column=1, padx=5, pady=5)
entry_input.insert(END, "IniAdalahContohAlgoritmaShellSort") # Contoh default

# Tombol Proses
tk.Button(frame_input, text="PROSES (Tambah Spasi)", command=handle_process, 
          bg="#4682B4", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10)


# Label Status
label_status = tk.Label(root, text="Tekan PROSES untuk menjalankan algoritma unik ini.", 
                            bg="#F0FFFF", fg="#004D40", font=("Arial", 11, "bold"))
label_status.pack(pady=10)

# --- Output ---
tk.Label(root, text="HASIL DENGAN SPASI OTOMATIS:", 
         bg="#F0FFFF", fg="#004D40", font=("Arial", 10, "bold")).pack(pady=5)

text_output = tk.Text(root, height=3, width=60, font=("Arial", 12), wrap=tk.WORD, bg="#FFFFFF")
text_output.pack(padx=20, pady=5)
text_output.insert(END, "Hasil akan muncul di sini...")
text_output.config(state=tk.DISABLED) # Membuat teks box read-only

root.mainloop()