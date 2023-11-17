from fastapi import FastAPI,  UploadFile, File, Header
from fastapi.responses import FileResponse, StreamingResponse, Response
import pdfkit

import aiofiles
from text_classification import text_classification
from mainFile import *

app = FastAPI()

@app.get("/")
async def check():
    return {"message": "Hello World"}

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    file_names = [file.filename for file in files]
    print("file_names:",file_names)
    return {"filenames": [file.filename for file in files]}

@app.post("/process")
async def process(
                        files: list[UploadFile],
                        trich_yeu: str = Header(None),
                        sokyhieu: str = Header(None),
                    ):
    result = 0
    info = {"số ký hiệu":"20938/QD-BTNMT", "trích yếu":""}

    #file = [file for file in files if file.filename == "2938-qd-btnmt_Signed.pdf"][0]
    #print("file_origin:",file.filename)

    file_names = [file.filename for file in files]
    print("file_names:",file_names)

    Files = []
    for file in files:
        path = f"output/{file.filename}"
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)  # async write
        Files.append(path)

    text, file_name = getMainFile(Files, info)
    print("mainfile_name:",file_name)
    #with open("ocr.txt", "w") as output_file:
    #    output_file.write(text)

    

    if text != "" and text is not None:
        macongviec, dvcc, ndcv, sanpham, phutrach, thuchien, phoihop = text_classification(text)
    else:
        return {"result": 1}

    
    with open("source_files/2938-qd-btnmt_Signed.pdf", "rb") as f:
        pdf_bytes = f.read()

    headers = {"result": result,
            "macongviec": macongviec,
            "donvichucchi": dvcc,
            "noidungcongviec": ndcv,
            "sanpham": sanpham,
            "phutrach": phutrach,
            "thuchien": thuchien,
            "phoihop": phoihop}
    
    headers = {"Content-Disposition": "inline; filename=2938-qd-btnmt_Signed.pdf"}

    response = Response(pdf_bytes, media_type="application/pdf", headers=headers)

    # Return the Response object
    return response
    return {"result": result,
            "macongviec": macongviec,
            "donvichucchi": dvcc,
            "noidungcongviec": ndcv,
            "sanpham": sanpham,
            "phutrach": phutrach,
            "thuchien": thuchien,
            "phoihop": phoihop,
            "response":response}
    

    pdf_content = pdfkit.from_file("source_files/2938-qd-btnmt_Signed.pdf", "out.pdf")
    return {"result": result,
            "macongviec": macongviec,
            "donvichucchi": dvcc,
            "noidungcongviec": ndcv,
            "sanpham": sanpham,
            "phutrach": phutrach,
            "thuchien": thuchien,
            "phoihop": phoihop,
            "pdf_content": pdf_content}

if __name__ == "__main__":
    video = "video/face_video.mp4"

