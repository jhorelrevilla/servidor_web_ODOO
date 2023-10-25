def binaryToPdf(file_name,binary):     
    with open(f'{file_name}', 'wb') as fout:
        fout.write(binary)

def PdfTobinary(file_name):     
    data_bin=None
    with open(f'{file_name}', 'rb') as fout:
        data_bin=fout.read()
    return data_bin