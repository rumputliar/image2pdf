import os
from PyPDF2 import PdfReader, PdfWriter
import time

# Nama folder untuk file PDF
folder_file_pdf = r"F:\Project\12-01-24\Foto\03. Kec_Mojoanyar\Sumberjati\hasil"

# Nama folder untuk hasil
folder_hasil = "hasil"

# Buat folder hasil jika belum ada
if not os.path.exists(folder_hasil):
    os.makedirs(folder_hasil)

# Nama file gabungan
nama_file_gabungan = "file_gabungan_merger.pdf"

# Dapatkan semua file PDF dalam folder
file_inputs = [f for f in os.listdir(folder_file_pdf) if f.lower().endswith(".pdf")]

# Hitung jumlah file input
jumlah_file = len(file_inputs)

# Hitung persentase progres untuk setiap file
progres_per_file = 100 / jumlah_file

# Inisialisasi variabel progres
progres = 0

# Gabungkan file PDF
output_pdf = PdfWriter()
for i, file_input in enumerate(file_inputs):
    # Tampilkan progres horizontal
    progres += progres_per_file
    print(f"Proses Penggabungan: [{int(progres)}%]", end='\r')

    # Nama file output
    file_output = os.path.join(folder_hasil, f"{os.path.splitext(file_input)[0]}_merger.pdf")

    # Gunakan PyPDF2 untuk menggabungkan file PDF
    input_pdf = PdfReader(os.path.join(folder_file_pdf, file_input), "rb")
    for page_num in range(len(input_pdf.pages)):
        output_pdf.add_page(input_pdf.pages[page_num])

    # Jeda 2 detik
    time.sleep(2)

# Simpan file gabungan
with open(os.path.join(folder_hasil, nama_file_gabungan), "wb") as output_file:
    output_pdf.write(output_file)

# Tampilkan pesan berhasil
print("\nFile Berhasil Digabung Kak!")
