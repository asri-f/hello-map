import pandas as pd

# iseng aja biar bisa save
# Baca file asli
df = pd.read_csv("eq5.csv")

# Pilih kolom yang dibutuhkan
df_singkat = df[["time", "latitude", "longitude", "mag", "depth", "place"]]

# Simpan sebagai CSV baru
df_singkat.to_csv("eq_singkat.csv", index=False)
print("CSV versi singkat berhasil disimpan sebagai 'eq_singkat.csv'")
