import tkinter as tk
from tkinter import messagebox

# Variabel untuk menyimpan input saat ini dan hasil
current_input = ""
last_result = None

def clear_all():
    """Membersihkan tampilan dan mereset semua variabel."""
    global current_input, last_result
    current_input = ""
    last_result = None
    display_var.set("0")

def append_number(number):
    """Menambahkan angka ke input saat ini."""
    global current_input
    if current_input == "0" and number == "0":
        return # Hindari "00"
    if current_input == "0":
        current_input = number
    else:
        current_input += number
    display_var.set(current_input)

def append_operator(operator):
    """Menambahkan operator. Jika input sudah ada operator, ganti operatornya."""
    global current_input
    # Cek apakah karakter terakhir adalah operator. Jika ya, ganti operatornya.
    operators = ['+', '-', '*', '//', '%']
    if current_input and current_input[-1] in operators:
        current_input = current_input[:-1] + operator
    elif current_input:
        # Jika input tidak kosong, tambahkan operator
        current_input += operator
    else:
        # Jika input kosong, dan ada hasil sebelumnya, gunakan hasil tersebut
        global last_result
        if last_result is not None:
             current_input = str(last_result) + operator
        else:
            # Jika input kosong dan tidak ada hasil, operator tidak ditambahkan
            return
            
    display_var.set(current_input)

def calculate():
    """Menghitung ekspresi dalam input saat ini."""
    global current_input, last_result
    
    if not current_input:
        return

    try:
        # Mengganti operator pembagian bulat Python '//' agar dapat dievaluasi
        # dan memastikan pembagian modulus Python '%' ditangani dengan baik.
        # Catatan: eval() harus digunakan dengan hati-hati dalam aplikasi nyata, 
        # namun untuk kalkulator sederhana ini, ini adalah cara tercepat.
        expression = current_input.replace('//', '_//_').replace('%', '_%_')
        
        # Pisahkan ekspresi menjadi operan dan operator
        import re
        parts = re.split(r'([+\-*/%])', current_input)
        
        # Validasi sederhana: Pastikan ada setidaknya 3 bagian (angka1, operator, angka2)
        if len(parts) < 3 or parts[-1] == '':
             messagebox.showerror("Error", "Ekspresi tidak lengkap.")
             return

        # Ambil Angka 1, Operator, Angka 2 (hanya mendukung 1 operator sederhana)
        # Jika ingin mendukung rantai operasi, perlu parsing yang lebih kompleks.
        num1 = int(parts[0])
        op = parts[1]
        num2 = int(parts[2])

        result = 0
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/': # Perlakuan khusus untuk pembagian bulat
            if num2 == 0:
                messagebox.showerror("Error", "Pembagian dengan nol!")
                return
            result = num1 // num2
        elif op == '%':
            if num2 == 0:
                messagebox.showerror("Error", "Modulus dengan nol!")
                return
            result = num1 % num2
        
        # Jika berhasil, perbarui tampilan dan simpan hasil
        current_input = str(result)
        last_result = result
        display_var.set(str(result))
        
    except ValueError:
        messagebox.showerror("Error", "Input tidak valid.")
        clear_all()
    except Exception as e:
        # Tangani error lain, misal format ekspresi
        messagebox.showerror("Error", f"Kesalahan perhitungan: {e}")
        clear_all()


# --- Konfigurasi Jendela Utama ---
root = tk.Tk()
root.title("Kalkulator Klasik (Integer)")
root.resizable(False, False)
root.configure(bg="#F0F0F0") 

# 

# --- Variabel Tampilan ---
display_var = tk.StringVar(value="0")

# --- Tampilan Hasil ---
# Gunakan Entry untuk tampilan hasil yang lebih mirip kalkulator
display = tk.Entry(root, textvariable=display_var, 
                   font=('Arial', 24, 'bold'), bd=10, relief=tk.FLAT, 
                   justify='right', bg="#CCFFCC", fg="#333333")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# --- Tata Letak Tombol ---
# Daftar tombol: (teks, baris, kolom, fungsi)
buttons = [
    ('C', 1, 0, clear_all),
    ('%', 1, 1, lambda: append_operator('%')),
    ('//', 1, 2, lambda: append_operator('/')), # Gunakan '/' untuk tombol, tapi di fungsi calculate diperlakukan sebagai '//'
    ('*', 1, 3, lambda: append_operator('*')),
    ('7', 2, 0, lambda: append_number('7')),
    ('8', 2, 1, lambda: append_number('8')),
    ('9', 2, 2, lambda: append_number('9')),
    ('-', 2, 3, lambda: append_operator('-')),
    ('4', 3, 0, lambda: append_number('4')),
    ('5', 3, 1, lambda: append_number('5')),
    ('6', 3, 2, lambda: append_number('6')),
    ('+', 3, 3, lambda: append_operator('+')),
    ('1', 4, 0, lambda: append_number('1')),
    ('2', 4, 1, lambda: append_number('2')),
    ('3', 4, 2, lambda: append_number('3')),
    ('=', 4, 3, calculate), # Tombol '=' memicu perhitungan
    ('0', 5, 0, lambda: append_number('0')),
]

# Style tombol
button_style = {'font': ('Arial', 14, 'bold'), 'bd': 1, 'relief': tk.RAISED, 'padx': 20, 'pady': 20}
operator_style = {'bg': '#FF9800', 'fg': 'white', **button_style}
number_style = {'bg': '#FFFFFF', 'fg': 'black', **button_style}
clear_style = {'bg': '#F44336', 'fg': 'white', **button_style}
equal_style = {'bg': '#4CAF50', 'fg': 'white', **button_style}

# Membuat dan menempatkan tombol
for (text, row, col, command) in buttons:
    style = number_style
    if text in ('+', '-', '*', '//', '%'):
        style = operator_style
    elif text == 'C':
        style = clear_style
    elif text == '=':
        style = equal_style
        
    btn = tk.Button(root, text=text, command=command, **style)
    # Tombol 0 span 2 kolom agar terlihat seperti kalkulator biasa
    if text == '0':
        btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
    elif text == '=':
        btn.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=5, pady=5)
    else:
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Konfigurasi agar baris dan kolom beradaptasi saat resizing (meskipun resizable=False)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Jalankan aplikasi
root.mainloop()