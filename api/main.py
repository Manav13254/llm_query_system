import logging
import sys

# This MUST be the first two lines, before any other imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)

from fastapi import FastAPI
from api.routes import upload_pdf, upload_docx, upload_email

app = FastAPI()

app.include_router(upload_pdf.router)
app.include_router(upload_docx.router)
app.include_router(upload_email.router)
