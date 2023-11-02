import os
import sys
from flask import Flask, render_template, request, redirect, url_for,jsonify,json
from flask_cors import CORS,cross_origin
import models.printer_utils as utils
import models.json_utils as jsonUtils
import models.binary_utils as binUtils
from datetime import datetime
from subprocess import call
import base64
# Directorio Base
site_root=os.path.realpath(os.path.dirname(__file__))
# Directorio de la data
data_dir=os.path.join(site_root,'data','data.json')
# Cargar la data
data=jsonUtils.loadJson(data_dir)
# Directorio del buffer
buffer_dir=os.path.join(site_root,'temp','buffer.pdf')
# Directorio del PDFtoPrinter
printer_dir=os.path.join(site_root,'PDFtoPrinter.exe')

print(f"{'='*15}  {datetime.now()}  {'='*15}")
print(f"data {data}")   
print(f"buffer_dir {buffer_dir}")
print(f"printer_dir {printer_dir}")
print(f"{'='*30}")

app = Flask(__name__)
CORS(app)

# test_dir=os.path.join(site_root,'test','prueba1.pdf')
# test_binary=binUtils.PdfTobinary(test_dir)
# test_binary=binUtils.PdfTobinary("test/prueba2.pdf")
# test_binary=binUtils.PdfTobinary("test/prueba3.pdf")

# call nssm set itgrupo_printer_server AppRotateFiles 1
# call nssm set itgrupo_printer_server AppRotateOnline 1
# call nssm set itgrupo_printer_server AppRotateSeconds 86400
# call nssm set itgrupo_printer_server AppRotateBytes 1048576

def prepare_buffer(binary):
    global site_root,buffer_dir
    
    # actualiza el buffer (bin->pdf)
    print("Actualizando el buffer")
    binUtils.binaryToPdf(buffer_dir,binary)

@app.route("/")
def mainPage():
    global data
    actual_printers=utils.local_printer_list()
    
    return render_template(
        "index.html",
        report_list=data.keys(),
        print_list=actual_printers
    )


@app.route("/save_conf",methods=['POST'])
def saveConf():
    global data, data_dir
    """
    {
        'Factura': 'EPSON L355 Series', 
        'Cotizacion': 'Microsoft XPS Document Writer'
    }
    """

    data_form=request.get_json()
    data=data_form
    print("nueva data", data)
    
    jsonUtils.writeJson(data,data_dir)

    return jsonify({'mensaje': 'Los datos se han guardado correctamente'}) 

@app.route("/receive_message",methods=['POST'])
# @cross_origin(origin='*')
def receiveMessage():
    global data,printer_dir, buffer_dir
    data_from_odoo=request.get_json()
    print("mensaje recibido", request.get_json())
    # Si el mensaje no tiene esa estructura
    if not data_from_odoo.get('type') or not data_from_odoo.get('content'):
        return jsonify({'error': 'Error interno'})
    tipo=str(data_from_odoo.get('type'))
    content=data_from_odoo.get('content')
    

    if tipo == 'Factura':
        print(data)
        # Obtener binario del URL
        import requests
        response = requests.get(content)
        print(f"Consultando la URL de la Factura")
        pdf_binary_content = response.content
        print(f"Creando el buffer del binario")
        prepare_buffer(pdf_binary_content)
        print(f"Mandando a imprimir a {data['Factura']}")
        os.system(f'PDFtoPrinter temp\\buffer.pdf "{data["Factura"]}"')
        
        
    if tipo == 'Cotizacion':
        print(data)
        content = content.encode('utf-8')
        print(f"Decodificando el binario")
        content=base64.decodebytes(content)        
        print(f"Creando el buffer del binario")
        prepare_buffer(content)
        print(f"Mandando a imprimir a {data['Cotizacion']}")
        os.system(f'PDFtoPrinter temp\\buffer.pdf "{data["Cotizacion"]}"')
        # with open("xd.bat", "w") as archivo_bat:
        #     archivo_bat.write(message)
            
        # parameters=["temp/buffer.pdf",f"{data['Cotizacion']}"]

        # try:
        #     call(["PDFtoPrinter.exe"] + parameters)
        # except Exception as e:
        #     print("Error al ejecutar el comando:", e)
    return jsonify({'mensaje': f'Los datos se han impreso correctamente {content}'}) 



# -----------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
