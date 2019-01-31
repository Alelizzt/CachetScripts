#!/usr/bin/python3
import requests
import json
from component_config import *

# @link: https://docs.cachethq.io/docs/incident-statuses
Scheduled = 0 # This status is reserved for a scheduled status.
Investigating = 1 # You have reports of a problem and you're currently looking into them.
Identified = 2 # You've found the issue and you're working on a fix.
Watching = 3 # You've since deployed a fix and you're currently watching the situation.
Fixed = 4 # The fix has worked, you're happy to close the incident.

# @link: https://docs.cachethq.io/docs/component-statuses
Operational = 1 # The component is working.
Performance_Issues = 2 # The component is experiencing some slowness.
Partial_Outage = 3 # The component may not be working for everybody. This could be a geographical issue for example.
Major_Outage = 4 # The component is not working for anybody.


headers = {
    "X-Cachet-Token": "{}".format(CACHET_TOKEN),
    "Content-Type": "application/json"
}

def updateStatusIncident(status, message):
    url = "{}/incidents".format(CACHET_API_URL)
    payload = {
      "name": "Error with {}".format(COMPONENT_NAME), 
      "message": message,
      "status": status,
      "visible": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Generating Incident: ", response.text)

def updateStatusComponent(status):
    url = "{}/components/{}".format(CACHET_API_URL, COMPONENT_ID)
    payload = {
      "name": "{}".format(COMPONENT_NAME),
      "description": "{}".format(COMPONENT_DESCRIPTION),
      "status": status
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    print("Update component: ", response.text)

try:
  respponse = requests.get("{}".format(COMPONENT_URL))
  if respponse.status_code is 200:
    updateStatusComponent(Operational)
  else:
    updateStatusComponent(Partial_Outage)
    updateStatusIncident(Investigating, "Error {}".format(respponse.status_code))
except requests.HTTPError as error:
  updateStatusComponent(Major_Outage)  
  updateStatusIncident(Investigating, "HTTP error - {}".format(error))
except requests.exceptions.ConnectionError as con_error:
  print("Doesn't have Internet access! {}".format(conn_error))
  updateStatusComponent(Major_Outage)
except requests.exceptions.Timeout as time_error:
  updateStatusComponent(Major_Outage)
  updateStatusIncident(Investigating, "TimeOut Error {}".format(time_error))
except:
  updateStatusComponent(Major_Outage)
  updateStatusIncident(Investigating, "Unknown error [ CheckServerToResolve ]")
