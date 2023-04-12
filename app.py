import uvicorn
import os.path
import shutil
import wget

from fastapi import FastAPI

from routers import root_router, excel_to_csv_router, image_to_text_router

if not os.path.exists("/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata"):
    rus_traindata_file_url = "https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/master/rus.traineddata"
    file_name = wget.download(rus_traindata_file_url)
    shutil.move(file_name, "/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/")

# Metadata for the swagger documentation for each endpoint
tags_metadata = [
    {
        "name": "Excel to CSV",
        "description": "All endpoints related to Exams Questions answers"
    },
    {
        "name": "Root",
        "description": "Root endpoint"
    }
]

# API description
description = "API for Excel to CSV & OCR"

# FastAPI initialization and metadata for the documentation
app = FastAPI(
    root_path="/",
    title="PROJECT APIs",
    description=description,
    version="0.1.0",
    contact={
        "name": "Usama Tahir",
        "email": "usamatahir717@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "hhtps://www.apache.org/license/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

# Include routers
# router to root endpoint
app.include_router(root_router.router)  # for root

# router for ExcelTOCSV
app.include_router(excel_to_csv_router.router)
app.include_router(image_to_text_router.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
