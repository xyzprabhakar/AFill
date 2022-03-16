import PyPDF2 as pdf
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
import GenerateConfig as Gc

class ImportData(tk.Frame):
    config=None
    def __init__(self,config):
        tk.Frame.__init__(self)
        self.config=config
        self["background"]=self.config.COLOR_MENU_BACKGROUND
        self["height"]=450
        self["width"]=450
        self.pack(expand=True, fill=tk.BOTH)
        self.fncCreateItems()
    

    def open_file(self):
        open_file = askopenfilename(initialdir="d:",title="Open Template" , filetypes =[('Pdf Files', '*.pdf')])
        if open_file:            
            pdfReader = pdf.PdfFileReader(open_file)
            #content = pdfReader.read()
            print(pdfReader.numPages)
            # creating a page object
            pageObj = pdfReader.getPage(0)
            # extracting text from page
            print(pageObj.extractText())
            
            # closing the pdf file object
            #pdfFileObj.close()

    def save_data(self):
        print("Hello World")


    def fncCreateItems(self):
        lbl1 = tk.Label(self,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10), anchor=tk.NW)
        txtId = tk.Entry(self,bg=self.config.COLOR_BACKGROUND,name="txt__Id" ,width = 25,font=self.config.displayFont).place(x = 170,y = (10), anchor=tk.NW)	
        yaxis=40
        for x in self.config.IO_Name:
            lbl1 = tk.Label(self,  text = x,font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
            txt = tk.Entry(self,name="txt"+ x,bg=self.config.COLOR_BACKGROUND, width = 25,font=self.config.displayFont).place(x = 170,y = (10+yaxis), anchor=tk.NW)	
            yaxis=yaxis+40

        
        btnImport = tk.Button ( self, text ="Import",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =lambda:self.open_file() )
        btnSave = tk.Button ( self, text ="Save", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.save_data())
        btnImport.bind('<Enter>', self.config.on_enter_button)
        btnImport.bind('<Leave>', self.config.on_leave_button)
        btnSave.bind('<Enter>', self.config.on_enter_button)
        btnSave.bind('<Leave>', self.config.on_leave_button)
        btnImport.place(x = 170,y = 10+yaxis, anchor=tk.NW)
        btnSave.place(x = 270,y = 10+yaxis, anchor=tk.NW)
        txtDetail=tk.Text(self,height=30)
        txtDetail.pack(expand=True, )
        
        
if __name__ == '__main__':
    config= Gc.GenerateConfig()
    ImportData(config).mainloop()
        




