from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import uuid
import os
from model import run_inference

app = FastAPI()

# CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion besser auf spezifische Domains beschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ordner für gespeicherte Bilder bereitstellen
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()

    # Datei in ein OpenCV-Bild umwandeln
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return JSONResponse(content={"error": "Bild konnte nicht geladen werden."}, status_code=400)

    # Inferenz durchführen
    result_img, boxes = run_inference(img)

    # Zufälligen Dateinamen generieren
    filename = f"{uuid.uuid4().hex}.jpg"
    save_path = os.path.join("images", filename)

    # Ergebnisbild speichern
    cv2.imwrite(save_path, result_img)

    # URL zur gespeicherten Datei zurückgeben
    image_url = f"/images/{filename}"

    return {
        "filename": file.filename,
        "detections": boxes,
        "image_url": image_url
    }
