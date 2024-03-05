from pdfrw import PdfReader, PdfWriter, PageMerge
import img2pdf
import io
import os
import glob

def add_signature_to_pdfs(signature_path, documents_folder='documents'):
    # Find all PDF files in the documents folder
    pdf_paths = glob.glob(f"{documents_folder}/*.pdf")

    for pdf_path in pdf_paths:
        # Open the PDF and the signature image
        pdf = PdfReader(pdf_path)

        # Convert the signature image to PDF Bytes
        signature_pdf_bytes = img2pdf.convert(signature_path)

        # Convert the bytes to a PDF page
        signature_pdf = PdfReader(io.BytesIO(signature_pdf_bytes)).pages[0]

        # Create a new PageMerge object for the signature
        signature_page = PageMerge().add(signature_pdf)[0]
        signature_page.scale(0.5, 0.5)  # Reduce the size by 50%
        signature_page.x = 297 - signature_page.w / 2
        signature_page.y = 421 - signature_page.h / 2

        # Merge the signature onto the desired page
        merger = PageMerge(pdf.pages[0])
        merger.add(signature_page).render()

        # Create the "results" folder if it doesn't exist
        os.makedirs('results', exist_ok=True)

        # Extract the filename from the PDF path
        filename = os.path.basename(pdf_path)

        # Create the output path
        output_path = f"results/signed_{filename}"

        # Write the output to a new PDF file
        PdfWriter().write(output_path, pdf)

# Use the function
add_signature_to_pdfs('signatures/signature.png')