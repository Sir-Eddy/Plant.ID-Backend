# 🌿 Plant Identifier – Backend

Ein einfaches Backend zur automatischen Erkennung von Pflanzen (insbesondere Unkraut) auf Bildern mithilfe eines YOLOv11-Modells.  
Das System nimmt ein Bild vom Frontend entgegen, erkennt darauf Pflanzen, markiert sie farblich und gibt das Ergebnisbild sowie die Koordinaten der erkannten Objekte zurück.

---

## 🚀 Features

- REST-API zur Analyse von Bildern
- Objekterkennung mit einem PyTorch-Modell (YOLOv11)
- Farbliche Markierung der erkannten Objekte mittels OpenCV
- Rückgabe des Ergebnisbildes als URL
- Übergabe der erkannten Objektkoordinaten im JSON-Format

---

## 🖥 Server starten

Stelle sicher, dass alle Abhängigkeiten installiert sind. Dann kann der Server wie folgt gestartet werden:

```bash
uvicorn main:app --reload
````

Die Anwendung läuft anschließend unter:

[http://localhost:8000](http://localhost:8000)

---

## 🔬 Testen der API im Browser

FastAPI stellt automatisch eine interaktive API-Dokumentation bereit.
Diese ist erreichbar unter:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

Hier kann ein Bild hochgeladen und die Erkennung getestet werden.

---

## 🧪 Beispiel-Antwort

```json
{
  "filename": "bild.jpg",
  "detections": [
    {
      "label": "unkraut",
      "confidence": 0.87,
      "box": [123, 45, 234, 120]
    }
  ],
  "image_url": "/images/abc123.jpg"
}
```

---

## ⚙️ Voraussetzungen

* Python 3.10 oder neuer
* Installierte Abhängigkeiten (siehe `requirements.txt`)

---

## 📁 Projektstruktur (Auszug)

```
.
├── main.py           # API-Endpunkt
├── model.py          # Inferenzlogik mit YOLOv11
├── images/           # Ergebnisbilder mit Markierungen
├── weights/          # YOLO-Modell (.pt)
├── requirements.txt
└── README.md
```
