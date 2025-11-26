# ============================
#        BAGIAN LIST
# ============================

# List adalah struktur data yang dapat diubah (mutable)
my_list = [1, 2, 3]
print("List awal:", my_list)

# Menambah elemen ke dalam list
my_list.append(4)
print("List setelah ditambah:", my_list)

# Mengubah elemen list
my_list[0] = 10
print("List setelah diubah elemen pertama:", my_list)


# ============================
#       BAGIAN TUPLE
# ============================

# Tuple adalah struktur data yang tidak dapat diubah (immutable)
my_tuple = (1, 2, 3)
print("\nTuple awal:", my_tuple)

# Tuple tidak bisa diubah, sehingga tidak bisa menggunakan .append()
# Jika baris ini dijalankan, akan menghasilkan ERR0R:
# my_tuple.append(4)

# Tetapi tuple bisa diakses elemennya
print("Elemen tuple indeks 1:", my_tuple[1])