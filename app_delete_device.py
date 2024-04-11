import csv
import grpc
from chirpstack_api import api

# Fonction pour lister les applications
def list_application(client, auth_token):
    req = api.GetApplicationRequest()
    
    resp = client.Get(req, metadata=auth_token)
    return resp

# Fonction pour lister les devices
def list_devices(client, auth_token):
    req = api.ListDevicesRequest()

    resp = client.List(req, metadata=auth_token)
    return resp

# Fonction pour créer un dispositif avec les clés spécifiées (inchangée)
def delete_device(client, dev_name, auth_token):
    null

if __name__ == "__main__":
    server = "192.168.170.72:8080"
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJhODk3MGI1LTRiZDYtNGE0OC1iZDgyLWFmNjk5OWExMmZkMSIsInR5cCI6ImtleSJ9.Rm4ERWTExi6X9jNsdqMADwTN0mSwsf9VToK4-NcGvpI"
    
    # Connectez-vous au serveur ChirpStack
    channel = grpc.insecure_channel(server)
    client = api.DeviceServiceStub(channel)
    auth_token = [("authorization", "Bearer %s" % api_token)]
    
    applications = list_application(client, auth_token)
    print('liste des application')
    print('---------------------')
    for application in applications.application:
        print(f'{application.name}')
    
    #devices = list_devices(client, auth_token)
    #print(f"ID | Dev EUI           | name")
    #print(f"-----------------------------")
    #device_id=0
    #for device in devices:
        #print(f"{device_id} | {device.dev_eui} | {device.name}")
