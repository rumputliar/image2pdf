import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

def convert_images_to_pdf(directory):
    log_file = open('log.txt', 'a')
    total_images = 0
    processed_images = 0
    pdf_file_paths = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                total_images += 1

                # Create PDF directory if not exists
                pdf_dir = os.path.join(root, 'PDFs')
                os.makedirs(pdf_dir, exist_ok=True)

                # Create PDF file with the same name as the image
                pdf_path = os.path.join(pdf_dir, f"{os.path.splitext(file)[0]}.pdf")
                pdf_file_paths.append(pdf_path)

                # Convert image to PDF
                img = Image.open(file_path)

                # Check and resize image if needed
                if img.size[0] > letter[0] or img.size[1] > letter[1]:
                    img.thumbnail(letter)

                img.save(pdf_path, "PDF")
                processed_images += 1

                # Pause for 1 second after each conversion
                time.sleep(1)

                # Display progress percentage
                progress_percentage = (processed_images / total_images) * 100
                print(f"\rProgress: {progress_percentage:.2f}%", end='', flush=True)

                # If more than 100 images, pause for 7 seconds after every 100 images
                if processed_images % 100 == 0 and processed_images > 0:
                    print("\nPausing for 7 seconds...")
                    time.sleep(3)

    # Combine PDF files into a single PDF named after the directory
    combined_pdf_path = os.path.join(directory, f"{os.path.basename(directory)}.pdf")
    merge_pdfs(pdf_file_paths, combined_pdf_path)

    log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: Converted {processed_images} images to PDF in {directory}\n")
    log_file.write(f"Combined PDF saved at: {combined_pdf_path}\n")
    log_file.close()
    print(f"\nConversion completed. Check log.txt for details.")
    return

def merge_pdfs(pdf_files, output_path):
    from PyPDF2 import PdfWriter, PdfFileReader

    pdf_writer = PdfWriter()

    for pdf_file in pdf_files:
        pdf_reader = PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    # Input directory from the user
    input_directory = input("Enter the starting directory path: ")

    # Check if the input directory exists
    if os.path.exists(input_directory):
        convert_images_to_pdf(input_directory)
    else:
        print("Directory not found.")