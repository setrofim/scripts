
class ExcelContext(object):
    """Manages a workbook opened in an Excel application through COM."""

    def __init__(self, wkbookfile, wksheet=None, save=False):
        self.file = wkbookfile
        self.wksheet = wksheet
        self.save = save

    def __enter__(self):
        from win32com.client import constants, DispatchEx
        self.xlapp = DispatchEx('Excel.Application')
        self.xlapp.Visible = False
        self.wkbook = self.xlapp.Workbooks.Open(self.file)
        if self.wksheet:
            return self.wkbook.Worksheets(self.wksheet)
        else:
            return self.wkbook

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.save:
            self.wkbook.Save()
        self.wkbook.Close()
        self.xlapp.Quit()



