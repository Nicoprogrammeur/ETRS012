# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:58:51 2024

@author: user
"""

import cv2
import pytesseract
from PIL import Image
import numpy as np
import csv
import os
import re

# Chemin du fichier CSV où les données seront sauvegardées
csv_path = 'donnees_extraites.csv'

# Configurez le chemin vers Tesseract-OCR si nécessaire
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera capture failed")
        break

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):  # Press the space bar to process the current frame
        # Détecter et décoder le QR code
        data, bbox, _ = detector.detectAndDecode(frame)
        deveui_qr = data if bbox is not None else ''

        # Convertir l'image capturée pour pytesseract
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        extracted_text = pytesseract.image_to_string(Image.fromarray(img_rgb))
        print("Texte extrait :")
        print(extracted_text)

        # Utiliser les expressions régulières pour extraire les données
        devaddr_match = re.search(r'DEV ADDR:\s*(\w+)', extracted_text)
        appkey_match = re.search(r'APP KEY:\s*([A-F0-9]+)', extracted_text)
        appskey_match = re.search(r'APPSKEY:\s*([A-F0-9]+)', extracted_text)
        netskey_match = re.search(r'NETSKEY:\s*([A-F0-9]+)', extracted_text)
        appeui_match = re.search(r'APP EUI:\s*([A-F0-9]+)', extracted_text)

        # Vérifier si le fichier CSV existe et est vide
        file_exists = os.path.isfile(csv_path)
        write_header = not file_exists or os.stat(csv_path).st_size == 0

        # Ouvrir le fichier CSV en mode append
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(['DEV ADDR', 'APP KEY', 'APPSKEY', 'NETSKEY', 'APP EUI', 'DEV EUI'])
            writer.writerow([
                devaddr_match.group(1) if devaddr_match else '',
                appkey_match.group(1) if appkey_match else '',
                appskey_match.group(1) if appskey_match else '',
                netskey_match.group(1) if netskey_match else '',
                appeui_match.group(1) if appeui_match else '',
                deveui_qr
            ])

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
