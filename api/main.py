from fastapi import FastAPI
from api.routes import upload_pdf, upload_docx, upload_email

app = FastAPI()

app.include_router(upload_pdf.router)
app.include_router(upload_docx.router)
app.include_router(upload_email.router)
