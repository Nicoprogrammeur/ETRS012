import csv
import grpc
from chirpstack_api import api
import info_api

# Fonction pour supprimer un device de l'applications
def delete_device(client, auth_token, device):
    req = api.DeleteDeviceRequest(dev_eui=device)
    resp = client.Delete(req, metadata=auth_token)
    return resp
    
# Fonction pour afficher les devices de l'applications
def read_device(client, dev_eui, auth_token):
    # Construct request.
    req = api.Device(dev_eui=dev_eui)

    resp = client.Get(req, metadata=auth_token)

    # Print the downlink name
    print(f"{resp.device.name:10} | {dev_eui}")

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

if __name__ == "__main__":
    server = "192.168.170.72:8080"
    
    # Connectez-vous au serveur ChirpStack
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    auth_token = [("authorization", "Bearer %s" % info_api.api_token)]
    
    # Lisez le fichier CSV
    with open("donnees_extraites.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Ignorez la première ligne (entête)
        
        print(f'liste des devices')
        print("-------------------------------")
        
        for row in csvreader:
            dev_eui = row[5]
            
            if device_exists(client, dev_eui, auth_token):
                #Afficher le device
                resp = read_device(client, dev_eui, auth_token)
    
    # Supprimez le device choisie
    del_dev_eui = input("\nIndiquer le dev_eui à effacer: ")
    
    if device_exists(client, del_dev_eui, auth_token):
        delete_device(client, auth_token, del_dev_eui)
        
        print(f"\nLe dispositif avec le dev_eui {del_dev_eui} à été supprimer.")
    else:
        print(f"Le dispositif avec le dev_eui {del_dev_eui} n'existe pas dans l'application.")

