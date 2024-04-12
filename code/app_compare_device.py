import csv
import grpc
from chirpstack_api import api
import info_api

# Fonction pour vérifier si un dispositif existe déjà
def device_exists(client, dev_eui, auth_token):
	
    try:
        req = api.GetDeviceRequest(dev_eui = dev_eui)
        client.Get(req, metadata=auth_token)
        return True  # Le dispositif existe
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return False  # Le dispositif n'existe pas
        else:
            raise  # Répercute d'autres exceptions

# Fonction pour créer un dispositif avec les clés spécifiées (inchangée)
def create_device(client, dev_eui, app_id, dev_id, dev_name, auth_token):
    req = api.CreateDeviceRequest()
    req.device.dev_eui = dev_eui
    req.device.application_id = app_id
    req.device.device_profile_id = dev_id
    req.device.name = dev_name
    # Envoie de la requête de création du dispositif
    resp = client.Create(req, metadata=auth_token)
    return resp

if __name__ == "__main__":
    server = "192.168.170.72:8080"
    # Connectez-vous au serveur ChirpStack
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    auth_token = [("authorization", "Bearer %s" % info_api.api_token)]

    # Lisez le fichier CSV et créez ou vérifiez les dispositifs
    with open("donnees_extraites.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # Ignorez la première ligne (entête)

        for row in csvreader:
            dev_eui = row[5]

            #print(f"{dev_eui}")

            if device_exists(client, dev_eui, auth_token):
                print(f"Le dispositif avec le dev_eui {dev_eui} existe déjà.")
            else:
                #dev_addr = row[0]
                # Créez le dispositif en utilisant les clés spécifiées
                #resp = create_device(client, dev_eui, info_api.applicationId, info_api.deviceProfileId, dev_addr, auth_token)
                # Affichez l'ID du dispositif créé
                print(f"Le dispositif avec le dev_eui {dev_eui} n'existe pas dans l'application")