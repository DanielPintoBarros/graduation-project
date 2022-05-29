from pyModbusTCP.client import ModbusClient
import requests
import json
import struct
import time



def readE1Register(port):
    client = ModbusClient(host="frade.crabdance.com", port=port)
    client.open()
    response = client.read_input_registers(reg_addr=0, reg_nb=36)
    data_json = {
        "vrms": struct.unpack('>f', response[1].to_bytes(2, 'big') + response[0].to_bytes(2,'big'))[0],
        "irms": struct.unpack('>f', response[3].to_bytes(2, 'big') + response[2].to_bytes(2,'big'))[0],
        "w": struct.unpack('>f', response[5].to_bytes(2, 'big') + response[4].to_bytes(2,'big'))[0],
        "va": struct.unpack('>f', response[7].to_bytes(2, 'big') + response[6].to_bytes(2,'big'))[0],
        "fp": struct.unpack('>f', response[9].to_bytes(2, 'big') + response[8].to_bytes(2,'big'))[0],
        "E1": struct.unpack('>f', response[11].to_bytes(2, 'big') + response[10].to_bytes(2,'big'))[0]
    }
    client.close()
    return data_json

def readE2Register(port):
    client = ModbusClient(host="frade.crabdance.com", port=port)
    client.open()
    response = client.read_input_registers(reg_addr=0, reg_nb=36)
    data_json = {
        "vrms1": struct.unpack('>f', response[1].to_bytes(2, 'big') + response[0].to_bytes(2,'big'))[0],
        "irms1": struct.unpack('>f', response[3].to_bytes(2, 'big') + response[2].to_bytes(2,'big'))[0],
        "w1": struct.unpack('>f', response[5].to_bytes(2, 'big') + response[4].to_bytes(2,'big'))[0],
        "va1": struct.unpack('>f', response[7].to_bytes(2, 'big') + response[6].to_bytes(2,'big'))[0],
        "fp1": struct.unpack('>f', response[9].to_bytes(2, 'big') + response[8].to_bytes(2,'big'))[0],
        "E1": struct.unpack('>f', response[11].to_bytes(2, 'big') + response[10].to_bytes(2,'big'))[0],
        "vrms2": struct.unpack('>f', response[13].to_bytes(2, 'big') + response[12].to_bytes(2,'big'))[0],
        "irms2": struct.unpack('>f', response[15].to_bytes(2, 'big') + response[14].to_bytes(2,'big'))[0],
        "w2": struct.unpack('>f', response[17].to_bytes(2, 'big') + response[16].to_bytes(2,'big'))[0],
        "va2": struct.unpack('>f', response[19].to_bytes(2, 'big') + response[18].to_bytes(2,'big'))[0],
        "fp2": struct.unpack('>f', response[21].to_bytes(2, 'big') + response[20].to_bytes(2,'big'))[0],
        "E2": struct.unpack('>f', response[23].to_bytes(2, 'big') + response[22].to_bytes(2,'big'))[0]
    }
    client.close()
    return data_json

def readE3Register(port):
    client = ModbusClient(host="frade.crabdance.com", port=port)
    client.open()
    response = client.read_input_registers(reg_addr=0, reg_nb=36)
    data_json = {
        "vrms1": struct.unpack('>f', response[1].to_bytes(2, 'big') + response[0].to_bytes(2,'big'))[0],
        "irms1": struct.unpack('>f', response[3].to_bytes(2, 'big') + response[2].to_bytes(2,'big'))[0],
        "w1": struct.unpack('>f', response[5].to_bytes(2, 'big') + response[4].to_bytes(2,'big'))[0],
        "va1": struct.unpack('>f', response[7].to_bytes(2, 'big') + response[6].to_bytes(2,'big'))[0],
        "fp1": struct.unpack('>f', response[9].to_bytes(2, 'big') + response[8].to_bytes(2,'big'))[0],
        "E1": struct.unpack('>f', response[11].to_bytes(2, 'big') + response[10].to_bytes(2,'big'))[0],
        "vrms2": struct.unpack('>f', response[13].to_bytes(2, 'big') + response[12].to_bytes(2,'big'))[0],
        "irms2": struct.unpack('>f', response[15].to_bytes(2, 'big') + response[14].to_bytes(2,'big'))[0],
        "w2": struct.unpack('>f', response[17].to_bytes(2, 'big') + response[16].to_bytes(2,'big'))[0],
        "va2": struct.unpack('>f', response[19].to_bytes(2, 'big') + response[18].to_bytes(2,'big'))[0],
        "fp2": struct.unpack('>f', response[21].to_bytes(2, 'big') + response[20].to_bytes(2,'big'))[0],
        "E2": struct.unpack('>f', response[23].to_bytes(2, 'big') + response[22].to_bytes(2,'big'))[0],
        "vrms3": struct.unpack('>f', response[25].to_bytes(2, 'big') + response[24].to_bytes(2,'big'))[0],
        "irms3": struct.unpack('>f', response[27].to_bytes(2, 'big') + response[26].to_bytes(2,'big'))[0],
        "w3": struct.unpack('>f', response[29].to_bytes(2, 'big') + response[28].to_bytes(2,'big'))[0],
        "va3": struct.unpack('>f', response[31].to_bytes(2, 'big') + response[30].to_bytes(2,'big'))[0],
        "fp3": struct.unpack('>f', response[33].to_bytes(2, 'big') + response[32].to_bytes(2,'big'))[0],
        "E3": struct.unpack('>f', response[35].to_bytes(2, 'big') + response[34].to_bytes(2,'big'))[0]
    }
    client.close()
    return data_json

def readWRegister(port):
    client = ModbusClient(host="frade.crabdance.com", port=port)
    client.open()
    response = client.read_input_registers(reg_addr=0, reg_nb=36)
    data_json = {
        "value": struct.unpack('>f', response[1].to_bytes(2, 'big') + response[0].to_bytes(2,'big'))[0]
    }
    client.close()
    return data_json

def getModbusRegisters():
    request = requests.post(
        url="http://api-client:5000/login",
        headers={"content-type": "application/json"},
        data= json.dumps({
            "email": "modbus",
            "password": "modbus"
        })
    )
    access_token = request.json()["access_token"]
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    r = requests.get('http://api-client:5000/registers/modbusOn', headers=headers)
    return r.json()["registers"]

def sendMeassures(register):
    url = 'http://api-client:5000/meassure'
    request = requests.post(
        url="http://api-client:5000/login",
        headers={"content-type": "application/json"},
        data= json.dumps({
            "email": register["user"]["email"],
            "password": register["user"]["password"]
        })
    )
    access_token = request.json()["access_token"]
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    if register["register_type"] == "ENERGY1":
        payload = readE1Register(register["modbus_port"])
    elif  register["register_type"] == "ENERGY2":
        payload = readE2Register(register["modbus_port"])
    elif  register["register_type"] == "ENERGY3":
        payload = readE3Register(register["modbus_port"])
    elif  register["register_type"] == "WATER":
        payload = readWRegister(register["modbus_port"])
    return requests.post(url=url, data=json.dumps(payload), headers=headers)

while True:
    try:
        time.sleep(7)
        registers = getModbusRegisters()
        for register in registers:
            response = sendMeassures(register)
    except:
        print("Shuting Down!")
