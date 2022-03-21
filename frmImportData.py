from tkinter import font
import PyPDF2 as pdf
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


import tabula 
#from tabula import read_pdf
#from tabulate import tabulate

import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import RAISED, ttk
import GenerateConfig as Gc


class ImportData(ttk.Frame):
    config=None
    varTemplateType = None
    varApplicantType = None
    varStarttingPoint=0

    def __init__1(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def __init__(self,config):
        tk.Frame.__init__(self)        
        self.config=config
        self["background"]=self.config.COLOR_MENU_BACKGROUND
        self["height"]=600
        self["width"]=768

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
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
            # closing the pdf file object
            #pdfFileObj.close()

    def open_file(self):
        open_file = askopenfilename(initialdir="d:",title="Open Template" , filetypes =[('Pdf Files', '*.pdf')])
        if open_file: 
            tables = tabula.read_pdf(open_file,pages="all") #address of pdf file
            ioindex=0
            dataFound=0
            for x in self.config.IO_Name:                
                dataFound=0
                for table in tables:
                    for i, j in table.iterrows():
                        print(j[0],j[1])                        
                        if(j[0]==self.config.IO_Template[ioindex]):
                            self.children["txtApplicant"+ x.strip().replace(' ', '_')].delete(0,tk.END)
                            self.children["txtApplicant"+ x.strip().replace(' ', '_')].insert(0,j[1]) 
                            if(self.varApplicantType.get()=="Co Applicant"):
                                self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].delete(0,tk.END)
                                self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].insert(0,j[2]) 
                            dataFound=1
                        if(dataFound==1):
                            break
                    if(dataFound==1):
                        break
                ioindex=ioindex+1

                        

                        
                    
            

            #tabula.convert_into(open_file,"output1.json", output_format="json", pages='all')
            #print(tabulate(df))
            #txtbox=self.children["txtremarks"]
            #txtbox.delete(1.0,"end")             
            #txtbox.insert("end",df)
            #txtbox.insert("end",tabulate(df))
            # closing the pdf file object
            #pdfFileObj.close()

    def save_data(self):
        print("Hello World")

    def hide_unhide_applicant(self,event):
        yaxis= self.varStarttingPoint
        if(self.varApplicantType.get()=="Single"):
            for x in self.config.IO_Name:
               self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place_forget() 
        else:
            for x in self.config.IO_Name:
               self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place(x = 400,y = (10+yaxis), anchor=tk.NW)
               yaxis=yaxis+40

        
    


    def fncCreateItems(self):

        self.varApplicantType.set("Co Applicant")
        self.varTemplateType.set("IO Template")

        
        
        yaxis=0
        tk.Label(self,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10), anchor=tk.NW)
        tk.Entry(self,bg=self.config.COLOR_BACKGROUND,name="txt__Id" ,width = 25,font=self.config.displayFont).place(x = 170,y = (10), anchor=tk.NW)	
        yaxis=40
        tk.Label(self,text = "Template Type",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        
        combostyle.theme_use('combostyle') 
        cmbTemplateType = ttk.Combobox(self, width = 23, textvariable =self.varTemplateType,font=self.config.displayFont)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.place(x = 170,y = (10+yaxis), anchor=tk.NW)	

        yaxis=yaxis+40
        tk.Label(self,text = "Applicant Type",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        cmbApplicantType = ttk.Combobox(self, width = 23, textvariable = self.varApplicantType,font=self.config.displayFont)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.place(x = 170,y = (10+yaxis), anchor=tk.NW)	
        cmbApplicantType.bind("<<ComboboxSelected>>", self.hide_unhide_applicant)
        yaxis=yaxis+40
        self.varStarttingPoint=yaxis
        for x in self.config.IO_Name:
            tk.Label(self,  text = x.strip(),font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
            tk.Entry(self,name="txtApplicant"+ x.strip().replace(' ', '_'),bg=self.config.COLOR_BACKGROUND, width = 25,font=self.config.displayFont).place(x = 170,y = (10+yaxis), anchor=tk.NW)
            tk.Entry(self,name="txtCoApplicant"+ x.strip().replace(' ', '_'),bg=self.config.COLOR_BACKGROUND, width = 25,font=self.config.displayFont).place(x = 400,y = (10+yaxis), anchor=tk.NW)	
            yaxis=yaxis+40
        
        btnImport = tk.Button ( self, text ="Import",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =lambda:self.open_file() )
        btnSave = tk.Button ( self, text ="Save", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.save_data())
        btnImport.bind('<Enter>', self.config.on_enter_button)
        btnImport.bind('<Leave>', self.config.on_leave_button)
        btnSave.bind('<Enter>', self.config.on_enter_button)
        btnSave.bind('<Leave>', self.config.on_leave_button)
        btnImport.place(x = 400,y = 10, anchor=tk.NW)
        btnSave.place(x = 400,y = 60, anchor=tk.NW)
        yaxis=yaxis+50
        #txtDetail=tk.Text(self,height=5, name="txtremarks")
        #txtDetail.place(x = 170,y = 10+yaxis, anchor=tk.NW)
        
        
if __name__ == '__main__':
    config= Gc.GenerateConfig()
    ImportData(config).mainloop()
        




