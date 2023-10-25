import json
from os import path
def loadJson(file_path):
    data=None
    try:
        with open(file_path,'r') as file:
            data=json.load(file)
    except FileNotFoundError:
        print(f"No se encuentra el archivo data.")
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo Json: {e}")
    finally:
        return data
def writeJson(data,file_path):

    with open(f"{file_path}","w") as outFile:
        outFile.write(json.dumps(data, indent=4))