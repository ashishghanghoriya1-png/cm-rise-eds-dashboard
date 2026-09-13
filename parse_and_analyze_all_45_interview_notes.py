import os
import sys
import io
import glob
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

dir_path = r"C:\Users\Peepul\OneDrive - Absolute Return For Kids\CMRise TPD Team's files - TPD - Knowledge Management System\Academic Year 2026-27\9. CPD EDS\2. Data\Interview Notes"

print(f"Reading all 45 qualitative interview files from:\n'{dir_path}'\n", flush=True)

# 1. Parse .docx files
docx_files = glob.glob(os.path.join(dir_path, "*.docx"))
print(f"Found {len(docx_files)} Word (.docx) transcript files.")

try:
    import docx
except ImportError:
    os.system("pip install python-docx pypdf pdfplumber")
    import docx

docx_data = []
for f in docx_files:
    try:
        doc = docx.Document(f)
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
        fname = os.path.basename(f)
        docx_data.append({"filename": fname, "text": full_text, "type": "docx"})
        print(f"  ✓ Read Word file: {fname} ({len(full_text)} chars)")
    except Exception as e:
        print(f"  ✗ Error reading {f}: {e}")

# 2. Parse .pdf files
pdf_files = glob.glob(os.path.join(dir_path, "*.pdf"))
print(f"\nFound {len(pdf_files)} PDF transcript files.")

try:
    import pypdf
except:
    os.system("pip install pypdf")
    import pypdf

pdf_data = []
for f in pdf_files:
    try:
        reader = pypdf.PdfReader(f)
        pages_text = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                pages_text.append(t)
        full_text = "\n".join(pages_text)
        fname = os.path.basename(f)
        pdf_data.append({"filename": fname, "text": full_text, "pages": len(reader.pages), "type": "pdf"})
        print(f"  ✓ Read PDF file: {fname} ({len(reader.pages)} pages, {len(full_text)} text chars)")
    except Exception as e:
        print(f"  ✗ Error reading {f}: {e}")

total_parsed = len(docx_data) + len(pdf_data)
print(f"\nTotal Parsed Transcript Files: {total_parsed} / {len(docx_files) + len(pdf_files)}")

# Build Master DataFrame of Interview Texts
all_records = docx_data + pdf_data
df_master_transcripts = pd.DataFrame(all_records)
df_master_transcripts.to_excel("statewide_master_qualitative_transcripts.xlsx", index=False)
print("Saved raw extracted transcript database to 'statewide_master_qualitative_transcripts.xlsx'!")
