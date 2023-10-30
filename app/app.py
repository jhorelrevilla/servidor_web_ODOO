import os
import sys
from flask import Flask, render_template, request, redirect, url_for,jsonify,json
from flask_cors import CORS
import models.printer_utils as utils
import models.json_utils as jsonUtils
import models.binary_utils as binUtils
from datetime import date
 
import base64
# Directorio Base
site_root=os.path.realpath(os.path.dirname(__file__))
# Directorio de la data
data_dir=os.path.join(site_root,'data','data.json')
# Cargar la data
data=jsonUtils.loadJson(data_dir)

print(f"{'-'*10} {date.today()} {'-'*10}")
print(f"data {data}")

app = Flask(__name__)
CORS(app)

test_dir=os.path.join(site_root,'test','prueba1.pdf')
test_binary=binUtils.PdfTobinary(test_dir)
# test_binary=binUtils.PdfTobinary("test/prueba2.pdf")
# test_binary=binUtils.PdfTobinary("test/prueba3.pdf")

def print_document(binary,printer_name):
    global site_root
    buffer_dir=f'{site_root}\\temp\\buffer.pdf'
    # actualiza el buffer (bin->pdf)
    print("Actualizando el buffer")
    binUtils.binaryToPdf(buffer_dir,binary)
    # Manda a imprimir lo del buffer
    print("Mandando a imprimir el contenido del buffer")
    utils.send_pdf_to_printer(buffer_dir,printer_name,f"{site_root}\\PDFtoPrinter.exe")

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
    global data, data_dir, test_binary
    """
    {
        'Factura': 'EPSON L355 Series', 
        'Cotizacion': 'Microsoft XPS Document Writer'
    }
    """
    data_form=request.get_json()
    for k,v in data_form.items():
        if data.get(str(k)):
            data[k]=v
    
    # print("nueva data", data)
    
    jsonUtils.writeJson(data,data_dir)

    return jsonify({'mensaje': 'Los datos se han guardado correctamente'}) 

@app.route("/receive_message",methods=['POST'])
def receiveMessage():
    global data
    data_from_odoo=request.get_json()
    print("mensaje recibido", request.get_json())
    # Si el mensaje no tiene esa estructura
    if not data_from_odoo.get('type') or not data_from_odoo.get('content'):
        return jsonify({'error': 'Error interno'})
    tipo=str(data_from_odoo.get('type'))
    content=data_from_odoo.get('content')
    
    if tipo == 'Factura':
        # Obtener binario del    URL
        import requests
        response = requests.get(content)
        print(f"Consultando la URL de la Factura")
        pdf_binary_content = response.content
        print(f"Mandando a imprimir a {data['Factura']}")
        print_document(pdf_binary_content,data['Factura'])
        

    if tipo == 'Cotizacion':
        content = content.encode('utf-8')
        print(f"Decodificando el binario")
        content=base64.decodebytes(content)
        print(f"Mandando a imprimir")
        print_document(content,data['Cotizacion'])
        
    return jsonify({'mensaje': 'Los datos se han guardado correctamente'}) 



# -----------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
