import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tqdm import tqdm
import time

def convert_images_to_pdf(image_folder, output_folder):
    # Membuat subfolder untuk menyimpan file PDF
    pdf_folder = os.path.join(output_folder, "PDFs")
    os.makedirs(pdf_folder, exist_ok=True)

    # Mendapatkan semua file gambar dalam folder
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Menghitung total gambar
    total_images = len(image_files)

    # Menentukan jumlah gambar per batch (50 gambar)
    batch_size = 50
    num_batches = (total_images + batch_size - 1) // batch_size

    for batch_num in range(num_batches):
        start_index = batch_num * batch_size
        end_index = min((batch_num + 1) * batch_size, total_images)
        batch_images = image_files[start_index:end_index]

        # Membuat file PDF untuk setiap batch
        pdf_filename = os.path.join(pdf_folder, f"{image_folder}_{batch_num + 1}.pdf")
        pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

        for i, image_file in enumerate(tqdm(batch_images, desc=f"Converting Batch {batch_num + 1}", unit="image")):
            image_path = os.path.join(image_folder, image_file)
            image = Image.open(image_path)

            # Mengonversi gambar ke PDF
            pdf_canvas.setPageSize((image.width, image.height))
            pdf_canvas.drawInlineImage(image, 0, 0, width=image.width, height=image.height)
            pdf_canvas.showPage()

            # Menunggu 1 detik setiap proses konversi gambar
            time.sleep(1)

        # Menutup file PDF setelah selesai batch
        pdf_canvas.save()

        # Menunggu 7 detik sebelum menggabungkan file PDF
        print(f"\nWaiting for 7 seconds before merging PDFs...")
        for remaining_time in reversed(range(7)):
            print(f"Merging in {remaining_time} seconds...", end="\r")
            time.sleep(1)

    # Menggabungkan semua file PDF menjadi satu file
    merged_pdf_filename = os.path.join(output_folder, f"{image_folder}_merged.pdf")
    merge_pdfs(pdf_folder, merged_pdf_filename)

def merge_pdfs(input_folder, output_filename):
    from PyPDF2 import PdfWriter, PdfReader

    pdf_writer = PdfWriter()

    # Menggabungkan semua file PDF dalam folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    pdf_files.sort()

    for pdf_file in tqdm(pdf_files, desc="Merging PDFs", unit="file"):
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_reader = PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.addPage(page)

        # Menunggu 1 detik setiap proses menggabungkan file PDF
        time.sleep(1)

    # Menyimpan file PDF hasil penggabungan
    with open(output_filename, 'wb') as output_file:
        pdf_writer.write(output_file)

if __name__ == "__main__":
    # Ganti path_folder_gambar dengan path folder gambar yang ingin Anda konversi
    path_folder_gambar = r"F:\Project\12-01-24\Foto\14. Kec_Jatirejo\Sumengko"

    convert_images_to_pdf(path_folder_gambar, os.path.dirname(path_folder_gambar))