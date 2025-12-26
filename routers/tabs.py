from fastapi import APIRouter,  File, UploadFile, HTTPException
from services.ocr_service import extract_text_from_image

router = APIRouter(prefix='/tabs', tags=['Tabs'])

@router.post('/process')
async def process_tab(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='El archivo debe ser una imagen')
    
    try:
        image_bytes = await file.read() #lee los bytes del archivo subido

        extracted_text = extract_text_from_image(image_bytes)

        return{
            'filename': file.filename,
            'detected_text': extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error procesando la imagen')