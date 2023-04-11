from fastapi import APIRouter, UploadFile, File

from services.excel_to_csv import excel_to_csv

# Metadata for the swagger documentation
router = APIRouter(
    prefix="",
    tags=["ExcelTOCSV"]
)


# Include routers
@router.post("/excel_to_csv", summary="Endpoint for excel to csv converter")
def excel_to_csv_api(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        file_name = f"Data/{file.filename}"
        with open(file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    extracted_data = excel_to_csv(file_name)
    return str(extracted_data)
