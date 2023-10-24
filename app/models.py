class Printer():
    def __init__(self, name) -> None:
        self.name=name
        self.printer=None
    def setPrinter(self, printer_name)->None:
        self.printer=printer_name

class System():
    def __init__(self) -> None:
        self.printer_list=[]
    def consult_actual_printers(self) -> list:
        pass
    
