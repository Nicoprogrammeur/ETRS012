# ETRS012

## Objectif
Mettre en place un mécanisme qui permet de :
```
- récupérer les identifiants d'un device
- stocker les identifiants dans un fichier formaté en csv
- ajouter un device dans le chirpstack avec les idenetifiants stockés dans le fichier csv
- supprimer un device sans se connecter directement dans le serveur chirpstack
- récupérer les données d'un device et les mettre dans un fichier formaté en csv  
```
 
## Etape 1
Numériser ces identifiants via un outil de reconnaissance optique de caractères (OCR) puis les stocker dans un fichier formaté en CSV.

## Prérequis
On a besoin d'installer plusieurs packages Python qui gèrent différentes parties de la fonctionnalité.<br/>
Voici les packages nécessaires et leurs fonctions :
#### - OpenCV (cv2) 
Utilisé pour manipuler les images et détecter les QR codes.
#### - Pillow (PIL)
Utilisé pour manipuler les images d'une manière qui est compatible avec pytesseract pour la reconnaissance optique de caractères (OCR).
#### - Pytesseract
Utilisé pour extraire du texte des images.<br/>
Note: pytesseract nécessite que Tesseract-OCR soit installé sur votre machine.
#### - csv
Ce module est déjà inclus dans la bibliothèque standard Python, donc aucune installation supplémentaire n'est nécessaire pour gérer les fichiers CSV.
#### - os
Ce module fait également partie de la bibliothèque standard Python et est utilisé pour interagir avec le système d'exploitation, comme vérifier l'existence des fichiers.<br/>
La commande ci-dessous permet d'installer les packages nécessaires
```
pip install opencv-python Pillow pytesseract
```
## Deux moyens de récupérer les identifiants d'un device dans un fichier d'extensions csv
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
## Etape 3
Réaliser l’opération inverse, c’est-à-dire récupérer dans un fichier formaté toutes les
informations des devices associés à une application.

