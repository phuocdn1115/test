from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import fitz
app = FastAPI()
def extract_text_from_pdf(pdf_content):
    # Use PyMuPDF to extract text from the PDF content
    pdf_document = fitz.open("pdf", pdf_content)
    text = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text()
    pdf_document.close()
    return text

@app.post("/process")
async def get_model(file: UploadFile):
    headers = {"result": "result",
               "macongviec": "macongviec",
               "donvichucchi": "dvcc",
               "noidungcongviec": "ndcv",
               "sanpham": "sanpham",
               "phutrach": "phutrach",
               "thuchien": "thuchien",
               "phoihop": "Phối hợp"}

    # return Response(file, media_type="application/pdf",  headers = headers)
    with open(f"source_files/{file.filename}", "rb") as f:
        pdf_bytes = f.read()

    encoded_pdf = extract_text_from_pdf(pdf_bytes)
    return JSONResponse(content={"pdf_content": encoded_pdf}, media_type="text",headers=headers)
