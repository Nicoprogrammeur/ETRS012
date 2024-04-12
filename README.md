# ETRS012: Grpc - chirpsatck

## Objectif
Mettre en place un mécanisme qui permet de :
```
- récupérer les identifiants d'un device et les stockés dans un fichier formaté en csv
- ajouter un device dans l'application chirpstack avec les idenetifiants stockés dans le fichier csv
- récupérer les données d'un device depuis l'application chirpstack et les mettre dans un fichier formaté en csv  
```
Ce mini-projet est subdivisé en 3 étapes
## Etape 1
Numériser ces identifiants via un outil de reconnaissance optique de caractères (OCR) puis les stocker dans un fichier formaté en CSV.
## Prérequis
On a besoin d'installer plusieurs packages Python qui gèrent différentes parties de la fonctionnalité.<br/>
Voici les packages nécessaires et leurs fonctions :
- OpenCV (cv2) 
Utilisé pour manipuler les images et détecter les QR codes.
- Pillow (PIL)
Utilisé pour manipuler les images d'une manière qui est compatible avec pytesseract pour la reconnaissance optique de caractères (OCR).
- Pytesseract
Utilisé pour extraire du texte des images.<br/>
Note: pytesseract nécessite que Tesseract-OCR soit installé sur votre machine.
- csv
Ce module est déjà inclus dans la bibliothèque standard Python, donc aucune installation supplémentaire n'est nécessaire pour gérer les fichiers CSV.
- os
Ce module fait également partie de la bibliothèque standard Python et est utilisé pour interagir avec le système d'exploitation, comme vérifier l'existence des fichiers.<br/>
La commande ci-dessous permet d'installer les packages nécessaires
```
pip install opencv-python Pillow pytesseract
```
## Deux moyens de récupérer les identifiants d'un device dans un fichier formaté en csv
### Extraire les identifiants du device depuis une image.
On utilise le code python **camera_image.py** pour extraire les identifiants d'un device et les mettre dans un fichier cvs.<br/>
Il faut renseigner dans le script python le chemin du répertoire où l'image est stockée et le chemin où on souhaite stocker le fichier csv.
```
# Chemin vers l'image contenant le texte imprimé et le QR code
image_path = 'test2.png'

# Chemin du fichier CSV où les données seront sauvegardées
csv_path = 'donnees_extraites.csv'
```
Le code récupère les informations suivantes et les mettre dans le fichier csv:
```
- devaddr
- appkey
- appskey
- netskey
- appeui
```
### Récupérer les identifiants du device avec une caméra et les stocker dans un fichier csv
Dans cette partie, on récupère les identifiants du device depuis une caméra et les stockées directement dans le  fichier csv.<br/>
On utilise le script **python camera_v3_15_20.py** pour lancer la caméra et de prendre une image directement avec la caméra.<br/>
Les données seront directement sauvegardées dans le fichier csv renseigné dans le script python.<br/>
Il faut renseigner le chemin où  on souhaite stocker le fichier csv.
```
# Chemin du fichier CSV où les données seront sauvegardées
csv_path = 'donnees_extraites.csv'
```
On récupère les mêmes données comme mentionné sur la **première partie**

## Etape 2
Ajouter automatiquement dans une application déclarée d’un Network Server privé, les devices via les API adéquates.
dans notre cas, nous travaillons pour enregistrer les device dans chirpstack
```
- https://www.chirpstack.io/docs/chirpstack/api/index.html
```
Pour enregister automatiquemet les devices dans le serveur chirpstack, on utilise le script python code/app_add_device.py.<br/>
pour cela, on a besoin de rennseigner dans le script python **code/app_add_device.py** les informations suivantes:
- l'adresse et le port du serveur chirpstack
- l'api_token
- les identifiants de l'application
- l'identifiant du profil du device
Ces informations sont à mettre à jour dans le script selon les besoins
```
server = "192.168.170.72:8080"
api_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
applicationId = "yyyyyyyy1111111111111222222222223333333333333333"
deviceProfileId = "zzzzzzzzzzzzzz1111111112222222223333333333333"
```
*NB:* L'**applicationId** et le **deviceProfileId** sont récupérables dans l'application chirpstack.
- le chemin du fichier csv où sont sauvegardés les identifiants des devices à enregistrer dans l'application.
```
    # Lisez le fichier CSV et créez les dispositifs
    with open("test.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Ignorez la première ligne (entête)
        
        for row in csvreader:
            dev_addr = row[0]
            app_key = row[1]
            appskey = row[2]
            nwkskey = row[3]
            app_eui = row[4]
            dev_eui = row[5]
        
            if device_exists(client, dev_eui, auth_token):
                print(f"Le dispositif avec le dev_eui {dev_eui} existe déjà.")
            else:
                dev_addr = row[0]
                # Créez le dispositif en utilisant les clés spécifiées
                resp = create_device(client, dev_eui, applicationId, deviceProfileId, dev_addr, auth_token)
                # Affichez l'ID du dispositif créé
                print(f"Dispositif créé avec le dev_eui: {dev_eui}")
```
Le script ci-dessus lit le fichier csv, récupère les identifiants des devices et les enregistre dans l'application.
## Etape 3
Réaliser l’opération inverse, c’est-à-dire récupérer dans un fichier formaté toutes les
informations des devices associés à une application.
Le script python **app_device_downlink.py** permet de récupérer les données d'un device depuis l'application.
Il faut renseigner l'adresse du serveur chirpstack , 



