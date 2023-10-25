from flask import Flask, render_template, request, redirect, url_for,jsonify,json
import models.printer_utils as utils
import models.json_utils as jsonUtils
import models.binary_utils as binUtils
import os


# Directorio de la data
site_root=os.path.realpath(os.path.dirname(__file__))
data_dir=os.path.join(site_root,'data','data.json')
# Cargar la data
data=jsonUtils.loadJson(data_dir)

app = Flask(__name__)

test_dir=os.path.join(site_root,'test','prueba1.pdf')
test_binary=binUtils.PdfTobinary(test_dir)
# test_binary=binUtils.PdfTobinary("test/prueba2.pdf")
# test_binary=binUtils.PdfTobinary("test/prueba3.pdf")

def print_document(binary,printer_name):
    global site_root
    buffer_dir=f'{site_root}/temp/buffer.pdf'
    # actualiza el buffer (bin->pdf)
    binUtils.binaryToPdf(buffer_dir,binary)
    # Manda a imprimir lo del buffer
    utils.send_pdf_to_printer(buffer_dir,printer_name,f"{site_root}/PDFtoPrinter.exe")

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
    
    print_document(test_binary,'EPSON L355 Series')

    return jsonify({'mensaje': 'Los datos se han guardado correctamente'}) 

@app.route("/receive_message",methods=['POST'])
def receiveMessage():
    global data
    """
    {
        'type_file': 'Factura',
        'content': binario
    }
    """
    data=request.get_json()


    print("mensaje recibido", data)
    return jsonify({'mensaje': 'Los datos se han guardado correctamente'}) 

# -----------------------
if __name__ == "__main__":
    app.run(debug=True,port=12345,host='201.230.200.202')
