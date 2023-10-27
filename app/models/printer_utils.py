from  win32print import GetDefaultPrinter,EnumPrinters
from subprocess import call

""" Funcion obtener impresora por defecto """
def get_default_printer():
    return GetDefaultPrinter()
""" Funcion obtener nombre de impresoras """
def local_printer_list():
    return [(printer[2]) for printer in EnumPrinters(2)]
""" Funcion mandar a imprimir PDF """
def send_pdf_to_printer(pdf_name,printer_name,pdfToPrinter_dir):
    command = "{} {}".format(pdfToPrinter_dir,f'{pdf_name}',f'{printer_name}')
    call(command,shell=True)
