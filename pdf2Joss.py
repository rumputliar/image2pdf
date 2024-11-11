import os
from PIL import Image
from reportlab.pdfgen import canvas
import time

def create_pdf(images, output_folder, pdf_name):
    pdf_path = os.path.join(output_folder, f"{pdf_name}.pdf")
    c = canvas.Canvas(pdf_path)

    for i, image_path in enumerate(images, start=1):
        img = Image.open(image_path)
        width, height = img.size

        # Menambahkan halaman baru ke PDF untuk setiap gambar
        c.setPageSize((width, height))
        c.drawInlineImage(img, 0, 0, width, height)
        c.showPage()

        # Tampilkan prosentase konversi horizontal
        progress_percentage = (i / len(images)) * 100
        progress_bar = "#" * int(progress_percentage / 2)
        print(f"Proses konversi: [{progress_bar:<50}] {progress_percentage:.2f}%", end='\r')

        # Jeda waktu 2 detik setiap proses konversi gambar
        time.sleep(2)

    c.save()

def convert_images_to_pdf(folder_path):
    # Membuat folder "hasil" jika belum ada
    output_folder = os.path.join(folder_path, "hasil")
    os.makedirs(output_folder, exist_ok=True)

    # Mendapatkan semua file gambar dalam folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Menyusun daftar path lengkap gambar
    image_paths = [os.path.join(folder_path, image_file) for image_file in image_files]

    # Membagi gambar menjadi kelompok berdasarkan jumlah (dalam kasus ini, kelipatan 300)
    grouped_images = [image_paths[i:i+300] for i in range(0, len(image_paths), 300)]

    for i, image_group in enumerate(grouped_images, start=1):
        pdf_name = f"{os.path.basename(folder_path)}_{i}"

        # Buat PDF dari kelompok gambar
        create_pdf(image_group, output_folder, pdf_name)

        # Jeda waktu 10 detik setiap setelah memproses 300 gambar ke PDF
        if i % 2 == 0 and i < len(grouped_images):
            print("\nMenunggu 7 detik...")
            for countdown in range(7, 0, -1):
                print(f"{countdown} detik tersisa...", end='\r')
                time.sleep(1)
            print("\n")

if __name__ == "__main__":
    # Ganti path_folder_gambar dengan path folder gambar yang ingin Anda konversi
    path_folder_gambar = r"F:\Project\12-01-24\Foto\05. Kec_Ngoro\Watesnegoro"

    convert_images_to_pdf(path_folder_gambar)