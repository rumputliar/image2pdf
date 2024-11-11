import os
from PIL import Image
from fpdf import FPDF

def convert_images_to_pdf(folder_path):
    # Membuat folder "hasil" jika belum ada
    output_folder = os.path.join(folder_path, "hasil")
    os.makedirs(output_folder, exist_ok=True)

    # Mendapatkan semua file gambar dalam folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Melakukan konversi gambar ke PDF
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)

        # Membuat objek PDF
        pdf = FPDF()
        pdf.add_page()

        # Menggunakan nama folder sebagai nama file PDF
        pdf_output_path = os.path.join(output_folder, f"{os.path.basename(folder_path)}.pdf")

        # Menambahkan gambar ke PDF
        pdf.image(image_path, 10, 10, 190)

        # Menyimpan PDF
        pdf.output(pdf_output_path, "F")

if __name__ == "__main__":
    # Ganti path_folder_gambar dengan path folder gambar yang ingin Anda konversi
    path_folder_gambar = r"F:\Project\12-01-24\Foto\02. Kec_Kutorejo\Wonodadi"

    convert_images_to_pdf(path_folder_gambar)