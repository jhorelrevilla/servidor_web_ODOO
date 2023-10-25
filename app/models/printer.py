class Printer():
    def __init__(self,name="",printer_name="") -> None:
        self.printer_name=printer_name
        self.name=name
    def get_json(self):
        result={
            'name':self.name,
            'printer_name':self.printer_name
        }
        return result