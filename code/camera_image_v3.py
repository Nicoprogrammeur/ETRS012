import cv2
import pytesseract
import re
from PIL import Image
import csv
import os

# Il faut absolument avoir un répertoire "img" avec toutes les images dedans

def lister_fichiers_recursivement(repertoire):
    for racine, repertoires, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            print(f'--------------------------')
            print(os.path.join(racine, fichier))
            
            # Chemin vers l'image contenant le texte imprimé et le QR code
            image_path = os.path.join(racine, fichier)
            
            # Chemin du fichier CSV où les données seront sauvegardées
            csv_path = 'donnees_extraites.csv'
            
            # Charger l'image du QR code avec OpenCV
            image = cv2.imread(image_path)
            
            # Utiliser PIL pour convertir l'image en mode compatible avec pytesseract
            image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Utiliser pytesseract pour obtenir le texte imprimé
            extracted_text = pytesseract.image_to_string(image_pil)
            
            print(f'{extracted_text}\n\n')
            
            # Définir les expressions régulières pour les différents champs
            devaddr_regex = r'DEV ADDR: ([A-F0-9]+)'
            appkey_regex = r'APP KEY: ([A-F0-9]+)'
            appskey_regex = r'APPSKEY: ([A-F0-9]+)'
            netskey_regex = r'NETSKEY: ([A-F0-9]+)'
            appeui_regex = r'\b(?:APP\s?EUI)\s*:\s*([A-F0-9_]+)'
            deveui_regex = r'\b(?:DEV\s?EUI)\s*:\s*([A-F0-9_]+)'
            
            #regex de fou
            #devaddr_regex = r'\b(?:DEV\s?ADDR)\s*:\s*([A-F0-9_\sS£]*)'
            #appkey_regex = r'\b(?:APP\s?KEY)\s*:\s*([A-F0-9_\sS£]*)'
            #appskey_regex = r'\b(?:APPSKEY)\s*:\s*([A-F0-9_\sS£]*)'
            #netskey_regex = r'\b(?:NETSKEY)\s*:\s*([A-F0-9_\sS£]*)'
            #appeui_regex = r'\b(?:APP\s?EUI)\s*:\s*([A-F0-9_\sS£]*)'
            #deveui_regex = r'\b(?:DEV\s?EUI)\s*:\s*([A-F0-9_\sS£]*)'

            # Chercher les données dans le texte extrait
            devaddr_match = re.search(devaddr_regex, extracted_text)
            appkey_match = re.search(appkey_regex, extracted_text)
            appskey_match = re.search(appskey_regex, extracted_text)
            netskey_match = re.search(netskey_regex, extracted_text)
            appeui_match = re.search(appeui_regex, extracted_text)
            deveui_match = re.search(deveui_regex, extracted_text)
            
            # Extraire et afficher les données si elles sont trouvées
            if devaddr_match:
                print("DEV ADDR:", devaddr_match.group(1))

            if appkey_match:
                print("APP KEY:", appkey_match.group(1))

            if appskey_match:
                print("APPSKEY:", appskey_match.group(1))

            if netskey_match:
                print("NETSKEY:", netskey_match.group(1))

            if appeui_match:
                print("APP EUI:", appeui_match.group(1))
                
            if deveui_match:
                print("DEV EUI:", deveui_match.group(1))
            
            # Vérifier si le fichier existe et s'il est vide
            file_exists = os.path.isfile(csv_path)
            write_header = not file_exists or os.stat(csv_path).st_size == 0
            
            # Ouvrir le fichier CSV en mode append
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Si le fichier est nouveau ou vide, écrire l'en-tête
                if write_header:
                    writer.writerow(['DEV ADDR', 'APP KEY', 'APPSKEY', 'NETSKEY', 'APP EUI', 'DEV EUI'])
                # Écrire les données extraites
                writer.writerow([
                    devaddr_match.group(1) if devaddr_match else '',
                    appkey_match.group(1) if appkey_match else '',
                    appskey_match.group(1) if appskey_match else '',
                    netskey_match.group(1) if netskey_match else '',
                    appeui_match.group(1) if appeui_match else '',
                    deveui_match.group(1) if deveui_match else '',
                    os.path.join(fichier)
                ])

if __name__ == "__main__":
    # Il faut absolument avoir un répertoire "img" avec toutes les images dedans
    lister_fichiers_recursivement('img')
    