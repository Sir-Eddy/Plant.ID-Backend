from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import cv2
import uuid
import os
from model import run_inference

app = FastAPI()

# Bilder unter /images/ verfügbar machen
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return JSONResponse(content={"error": "Bild konnte nicht geladen werden."}, status_code=400)

    # Inferenz durchführen
    result_img, boxes = run_inference(img)

    # Zufälligen Dateinamen generieren
    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join("images", filename)

    # Bild speichern
    cv2.imwrite(save_path, result_img)

    # URL zur gespeicherten Datei generieren
    image_url = f"/images/{filename}"

    return {
        "filename": file.filename,
        "detections": boxes,
        "image_url": image_url
    }
