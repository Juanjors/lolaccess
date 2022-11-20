# This is a sample Python script.
# coding=utf-8
import os
from commands import *
import requests
import base64

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


def getCurrentUser():
    riot_data = getPortAndPassword();
    print('token ' + riot_data.token, 'port ' + riot_data.port)
    header = {"Authorization": f"Basic {riot_data.authentication_string}"}
    response = requests.get(
    f"https://127.0.0.1:{riot_data.port}/lol-summoner/v1/current-summoner",
    headers=header, verify=False)
    print(response.status_code)
    print(response.json())



getCurrentUser()