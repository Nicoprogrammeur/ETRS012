import os
import sys

import grpc
from chirpstack_api import api

# lire fichier CSV et récupérer information
import csv
file = open('test.csv')
csvreader = csv.reader(file)

rows = []
devices = []
nombre_device = 0
with open("test.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        nombre_device=nombre_device+1
        #rows.append(row)
        devices.append(nombre_device)
        devices.append(row)
#print(header)
#print(rows)
print(devices)


# Configuration.

# This must point to the API interface.
server = "192.168.170.72:8080"

# The API token (retrieved using the web-interface).
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJhODk3MGI1LTRiZDYtNGE0OC1iZDgyLWFmNjk5OWExMmZkMSIsInR5cCI6ImtleSJ9.Rm4ERWTExi6X9jNsdqMADwTN0mSwsf9VToK4-NcGvpI"

if __name__ == "__main__":
  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % api_token)]
  
  for device in devices:
    d_name=device
    #print(type(device))
    if str(type(d_name)) == "<class 'list'>":
        #for valeur in range(len(d_name)):
            #print(d_name[valeur])
        dev_addr = device[0]
        app_key = device[1]
        appskey = device[2]
        netskey = device[3]
        app_eui = device[4]
        
        req = api.CreateDeviceKeysRequest()
        req.device_keys.dev_eui = dev_addr
        req.device_keys.nwk_key = netskey
        req.device_keys.app_key = app_eui
        
        # Créez le dispositif en utilisant les clés spécifiées
        resp = client.Create(req)
           
        # Affichez l'ID du dispositif créé
        print("Dispositif créé avec l'ID:", resp.id)
    #print(d_name)
    
    
    
# Construct request.
#req = api.EnqueueDeviceQueueItemRequest()
#req.queue_item.confirmed = False
#req.queue_item.data = bytes([0x01, 0x02, 0x03])
#req.queue_item.dev_eui = dev_eui
#req.queue_item.f_port = 10

#resp = client.Enqueue(req, metadata=auth_token)

# Print the downlink id
#print(resp.id)

