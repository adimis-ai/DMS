from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse
import PyPDF2
import pytesseract
import mysql.connector
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import PIL
from pdf2image import convert_from_path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_pdf_text(pdf_file):
    # convert pdf to image
    pages = convert_from_path(pdf_file)
    text = ""
    for page in pages:
        # convert image to text using pytesseract
        image = page.convert("L")
        text += pytesseract.image_to_string(image)
    return text

## MY SQL TABLE FOR DATABASE: detasys ##
#mysql> CREATE TABLE files (
#    ->     id INT AUTO_INCREMENT PRIMARY KEY,
#    ->     file_name VARCHAR(255) NOT NULL,
#    ->     file_path VARCHAR(255) NOT NULL,
#    ->     file_content TEXT NOT NULL,
#    ->     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#    -> );

@app.post("/files/")
async def create_file(file: UploadFile):
    file_name = file.filename
    file_path = "./uploads/" + file_name

    with open(file_path, 'wb') as f:
        file_data = await file.read()
        f.write(file_data)

    # extract text from the pdf, image, or word file
    if file_name.endswith('.pdf'):
        file_content = extract_pdf_text(file_path)

    elif file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        # pytesseract to extract text
        file_content = pytesseract.image_to_string(file_path)

    else:
        return {"error": "unsupported file type"}
    
    # store the file and extracted text in the database
    conn = mysql.connector.connect(
        host="localhost",  
        user="Adimis",  
        password="Admin@98", 
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "INSERT INTO files (file_name, file_path, file_content) VALUES (%s, %s, %s)"
    val = (file_name, file_path, file_content)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"file_name": file_name}

@app.get("/get_files/")
def read_files():
    # fetch the list of documents from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "SELECT * FROM files"
    cursor.execute(sql)
    files = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # return the list of documents
    return {"files": files}

@app.get("/get_files/{file_id}")
def download_file(file_id: int):
    # fetch the requested file from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "SELECT file_path, file_name FROM files WHERE id = %s"
    val = (file_id,)
    cursor.execute(sql, val)
    file = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if file is None:
        return {"error": "file not found"}

    # return the requested file
    file_path, file_name = file
    try:
        return FileResponse(
            file_path, 
            media_type="application/octet-stream", 
            headers=
            {
                "Content-Disposition": f"attachment; filename={file_name}"
            }
        )
    except FileNotFoundError:
        return {"error": "file not found"}


# ADD ROUTE TO DELETE A DOCUMENT
@app.delete("/delete_files/{file_id}")
def delete_file(file_id: int):
    # fetch the requested file from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "SELECT file_path, file_name FROM files WHERE id = %s"
    val = (file_id,)
    cursor.execute(sql, val)
    file = cursor.fetchone()
    cursor.close()
    conn.close()
    if file is None:
        return {"error": "file not found"}

    file_path, file_name = file

    # delete the file from the uploads folder
    try:
        os.remove(file_path)
    except FileNotFoundError:
        return {"error": "file not found"}

    # delete the record from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "DELETE FROM files WHERE id = %s"
    val = (file_id,)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "file deleted"}

@app.post("/search/")
def search_files(query: str):
    # fetch the list of documents from the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
    )
    cursor = conn.cursor()
    sql = "SELECT id, file_content FROM files"
    cursor.execute(sql)
    files = cursor.fetchall()
    cursor.close()
    conn.close()

    # similarity search
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([file[1] for file in files])
    query_tfidf = vectorizer.transform([query])
    similarity = cosine_similarity(query_tfidf, tfidf)
    most_similar = sorted(enumerate(similarity[0]), key=lambda x: x[1], reverse=True)[:2]

    # fetch the complete information for each file
    results = []
    for index, sim in most_similar:
        file_id = files[index][0]
        conn = mysql.connector.connect(
        host="localhost",
        user="Adimis",
        password="Admin@98",
        database="detasys"
        )
        cursor = conn.cursor()
        sql = "SELECT id, file_name, file_path, file_content, created_at FROM files WHERE id = %s"
        val = (file_id,)
        cursor.execute(sql, val)
        file = cursor.fetchone()
        results.append({"id": file[0], "file_name": file[1], "file_path": file[2], "file_content": file[3], "created_at": file[4], "similarity": sim})
        cursor.close()
    conn.close()

    return {"files": results}