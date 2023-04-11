from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException

from services import img_to_txt

# Metadata for the swagger documentation
router = APIRouter(
    prefix="",
    tags=["ImageToText"]
)


# Include routers
@router.post("/img_to_txt", summary="Endpoint for image to text converter")
def image_to_text(file: UploadFile = File(...)):
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_name = f"Data/{file.filename}"
    try:
        contents = file.file.read()
        with open(file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    extracted_data = img_to_txt.img_to_txt(file_name)
    return extracted_data
