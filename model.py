from ultralytics import YOLO
import numpy as np
import cv2

# Vortrainiertes YOLOv5-Modell laden (einmalig beim Start)
model = YOLO("yolov5s.pt")  # Du kannst auch yolov8n.pt verwenden

def run_inference(image: np.ndarray):
    # OpenCV (BGR) → RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Inferenz ausführen
    results = model(rgb)[0]

    boxes = []
    for r in results.boxes:
        x1, y1, x2, y2 = map(int, r.xyxy[0].tolist())
        conf = float(r.conf[0])
        cls = int(r.cls[0])
        label = model.names[cls]

        boxes.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": [x1, y1, x2, y2]
        })

        # Bounding Box + Text zeichnen
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return image, boxes
