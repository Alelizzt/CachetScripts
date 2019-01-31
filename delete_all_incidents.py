#!/usr/bin/python3
import requests
import json
from component_config import *

incidents = int(input("Id of last incident: "))
incident = 1
while incidents > 0:
  url = "{}/incidents/{}".format(CACHET_API_URL, incident)
  headers = {
      "X-Cachet-Token": "{}".format(CACHET_TOKEN),
      "Content-Type": "application/json"
  } 
  response = requests.delete(url, headers=headers)
  incident += 1
  incidents -= 1
print("All incidents deleted!")
