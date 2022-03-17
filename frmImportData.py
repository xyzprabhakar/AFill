import PyPDF2 as pdf
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io

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
    
    def convert_pdf_to_txt(self,path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text
    def open_file1(self):
        open_file = askopenfilename(initialdir="d:",title="Open Template" , filetypes =[('Pdf Files', '*.pdf')])
        if open_file: 
            txtbox=self.children["txtremarks"]
            txtbox.delete(1.0,"end")             
            txtbox.insert("end",self.convert_pdf_to_txt(open_file))
            

    def open_file(self):
        open_file = askopenfilename(initialdir="d:",title="Open Template" , filetypes =[('Pdf Files', '*.pdf')])
        if open_file:            
            pdfReader = pdf.PdfFileReader(open_file,'rb')            
            totalPages=pdfReader.numPages
            currentPages=0
            txtbox=self.children["txtremarks"]
            txtbox.delete(1.0,"end")
            while (currentPages<totalPages):
                # creating a page object
                pageObj = pdfReader.getPage(currentPages)
                # extracting text from page
                pageData=pageObj.extractText()
                #pageData=pageObj.getContents()
                txtbox.insert("end",pageData)
                currentPages=currentPages+1;
            
                

            
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
        btnSave = tk.Button ( self, text ="Save", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.open_file1())
        btnImport.bind('<Enter>', self.config.on_enter_button)
        btnImport.bind('<Leave>', self.config.on_leave_button)
        btnSave.bind('<Enter>', self.config.on_enter_button)
        btnSave.bind('<Leave>', self.config.on_leave_button)
        btnImport.place(x = 170,y = 10+yaxis, anchor=tk.NW)
        btnSave.place(x = 270,y = 10+yaxis, anchor=tk.NW)
        yaxis=yaxis+50
        txtDetail=tk.Text(self,height=5, name="txtremarks")
        txtDetail.place(x = 170,y = 10+yaxis, anchor=tk.NW)
        
        
if __name__ == '__main__':
    config= Gc.GenerateConfig()
    ImportData(config).mainloop()
        




