import csv
import grpc
from chirpstack_api import api

# Configuration.
server = "192.168.170.72:8090"
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJhODk3MGI1LTRiZDYtNGE0OC1iZDgyLWFmNjk5OWExMmZkMSIsInR5cCI6ImtleSJ9.Rm4ERWTExi6X9jNsdqMADwTN0mSwsf9VToK4-NcGvpI"

applicationId = "edf7601d-444b-425f-bf47-c7316e536b2c"
deviceProfileId = "0f6c9945-8d09-4a2f-b8a4-b3c3067f6b7d"


# Fonction pour créer un dispositif avec les clés spécifiées
def create_device(client, dev_eui, app_id, dev_id, dev_name):
    req = api.CreateDeviceRequest()
    req.device.dev_eui = dev_eui
    req.device.application_id = app_id
    req.device.device_profile_id = dev_id
    
    name = "device" + str(dev_name)
    req.device.name = name
    # Ajoutez d'autres attributs du dispositif au besoin
    # Par exemple: req.device.name = "Nom du dispositif"
    
    # Envoie de la requête de création du dispositif
    resp = client.Create(req)
    return resp

if __name__ == "__main__":
    # Connectez-vous au serveur ChirpStack
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    
    # Définissez les métadonnées d'authentification
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    # Lisez le fichier CSV et créez les dispositifs
    with open("test.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Ignorez la première ligne (entête)
        
        dev_name = 0
        
        for row in csvreader:
            dev_name = dev_name + 1
            dev_addr = row[0]
            app_key = row[1]
            appskey = row[2]
            nwkskey = row[3]
            app_eui = row[4]
            dev_eui = row[5]
            
            # Créez le dispositif en utilisant les clés spécifiées
            resp = create_device(client, dev_eui, applicationId, deviceProfileId, dev_name)
            
            # Affichez l'ID du dispositif créé
            print("Dispositif créé avec l'ID:", resp.id)