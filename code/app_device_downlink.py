import csv
import grpc
from chirpstack_api import api
import info_api

# Fonction pour afficher les devices de l'applications
def read_device(client, dev_eui, auth_token):
  # Construct request.
  req = api.Device(dev_eui=dev_eui)

  resp = client.Get(req, metadata=auth_token)

  # Print the downlink name and description
  if resp.device.description:
    print(f"{resp.device.name:10} | {dev_eui} | {resp.device.description}")
  else:
    print(f"{resp.device.name:10} | {dev_eui}")
  
def info_device(client, dev_eui, auth_token):
  # Construct request.
  req = api.Device(dev_eui=dev_eui)

  resp = client.Get(req, metadata=auth_token)
  
  print(f"description: {resp.device.description}")
  print(f"ApplicationId: {resp.device.application_id}")
  print(f"DeviceProfileId: {resp.device.device_profile_id}")
  print(f"Is disabled: {resp.device.is_disabled}")
  print(f"Join EUI: {resp.device.join_eui}")
  
  print(f"created_at: {resp.created_at}")
  print(f"updated_at: {resp.updated_at}")
  print(f"last_seen_at: {resp.last_seen_at}")
  
  print(f"margin: {resp.device_status.margin}")
  print(f"external: {resp.device_status.external_power_source}")
  print(f"battery: {resp.device_status.battery_level}")
  
  print(f"class_enabled: {resp.class_enabled}")
  
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
  # Configuration.
  # This must point to the API interface.
  server = "192.168.170.72:8080"

  # The API token (retrieved using the web-interface).
  # info_api.py -> api_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % info_api.api_token)]
  
  # Lisez le fichier CSV et créez les dispositifs
  with open("donnees_extraites.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Ignorez la première ligne (entête)
        
        print('list device')
        print('--------------------------------------------')
        
        for row in csvreader:
            dev_eui = row[5]
            
            if device_exists(client, dev_eui, auth_token):
                # Créez le dispositif en utilisant les clés spécifiées
                resp = read_device(client, dev_eui, auth_token)
