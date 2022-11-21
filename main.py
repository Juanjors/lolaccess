# This is a sample Python script.
# coding=utf-8
import os
from commands import *
import requests
import base64
import json
import random
class RiotData:
    def __init__(self, token, port):
        self.token = token
        self.port = port
        self.authentication_string = base64.standard_b64encode(bytes(f"riot:{token}", 'utf-8')).decode('utf-8')

TOKEN_CONST = '--remoting-auth-token'
PORT_CONST = '--app-port'

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def getPortAndPassword():
    result = exec_command("wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline")
    result = result[result.index(TOKEN_CONST) + len(TOKEN_CONST) + 1: len(result)]
    token = result[0: result.index('"')]
    result = result[result.index(PORT_CONST) + len(PORT_CONST) + 1: len(result)]
    port = result[0: result.index('"')]
    return RiotData(token, port)


#Pickea un campeón random elegible mientras estas en blind queue y lo selecciona
def pickRandomChampion():
    riot_data = getPortAndPassword();
    print('token ' + riot_data.token, 'port ' + riot_data.port)
    header = {"Authorization": f"Basic {riot_data.authentication_string}"}
    response = requests.get(
    f"https://127.0.0.1:{riot_data.port}/lol-champ-select/v1/pickable-champion-ids",
    headers=header, verify=False)
    pickable_champions = json.loads(response.content)
    print(pickable_champions)
    #Pickeamos un campeón aleatorio de los que tenemos
    body = {}
    body['championId'] = pickable_champions[random.randint(0, len(pickable_champions))];
    print(requests.patch(f"https://127.0.0.1:{riot_data.port}/lol-champ-select/v1/session/actions/1/", json.dumps(body), headers=header, verify=False))
    requests.post(f"https://127.0.0.1:{riot_data.port}/lol-champ-select/v1/session/actions/1/complete", headers=header, verify=False)


pickRandomChampion()