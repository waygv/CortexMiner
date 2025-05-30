import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='pdfminer')

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF using PyMuPDF (fitz)."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n\n"
    return text

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF using pdfplumber."""
    tables_list = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables or []:
                clean_table = [[cell if cell else "" for cell in row] for row in table]
                df = pd.DataFrame(clean_table)
                tables_list.append(df)
    return tables_list

def save_extracted_data(pdf_path, text, tables_list):
    """Save extracted text to a .txt file and tables to a .csv file."""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    text_file = f"{base_name}_content.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)

    csv_file = f"{base_name}_tables.csv"
    if tables_list:
        final_df = pd.concat(tables_list, ignore_index=True)
        final_df.to_csv(csv_file, index=False)
    else:
        pd.DataFrame().to_csv(csv_file, index=False)

    print("\n📂 Extracted Files:")
    print(f"📜 Text File: {os.path.abspath(text_file)}")
    print(f"📊 Tables File: {os.path.abspath(csv_file)}")
    return text_file, csv_file

def process_pdf_file(pdf_path):
    """Main function to process a PDF file and return results."""
    if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith(".pdf"):
        raise FileNotFoundError("❌ No valid PDF file found at the provided path.")

    print(f"✅ Processing: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    tables = extract_tables_from_pdf(pdf_path)
    text_file, csv_file = save_extracted_data(pdf_path, text, tables)

    return {
        "text_file": text_file,
        "tables_file": csv_file,
        "text_preview": text[:500],  # First 500 characters
        "num_tables": len(tables)
    }

# Optional example usage
# if __name__ == "__main__":
#     pdf_path = r"C:\Users\vinay\OneDrive\Desktop\CortexMiner\CortexMiner\AccountingFinancialStatements[1].pdf"
    
#     try:
#         result = process_pdf_file(pdf_path)

#         print(f"\nText saved to: {result['text_file']}")
#         print(f"Tables saved to: {result['tables_file']}")
#         print(f"Number of tables found: {result['num_tables']}")
#         print(f"Text Preview:\n{result['text_preview']}")
#     except Exception as e:
#         print(f"❌ Error: {e}")
