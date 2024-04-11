import os
import sys

import grpc
from chirpstack_api import api

# Configuration.

# This must point to the API interface.
server = "192.168.170.72:8080"

# The DevEUI for which you want to enqueue the downlink.
dev_eui = "A84041f6e182352a"

# The API token (retrieved using the web-interface).
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjJhODk3MGI1LTRiZDYtNGE0OC1iZDgyLWFmNjk5OWExMmZkMSIsInR5cCI6ImtleSJ9.Rm4ERWTExi6X9jNsdqMADwTN0mSwsf9VToK4-NcGvpI"

if __name__ == "__main__":
  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % api_token)]

  # Construct request.
  req = api.Device(dev_eui=dev_eui)

  resp = client.Get(req, metadata=auth_token)

  # Print the downlink id
  print(f"name: {resp.device.name}")
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