import configparser,os
from msilib.schema import Font
from ttkthemes import ThemedStyle


class GenerateConfig:
    # CREATE OBJECT
    config_file = configparser.ConfigParser()
    ConfigFileName="configurations.ini"
    Name=None
    Email=None
    ContactNo=None
    IO_Name=[]
    IO_Template=[]
    COLOR_TOP_BACKGROUND="#44a2d2"
    COLOR_BACKGROUND="#f2f5f7"
    COLOR_FOREGROUND="#343a40"
    COLOR_MENU_BACKGROUND="#ffffff"    
    displayFont=( "Verdana", 10)
    ChromeDriver="chromedriver.exe"
    themeName=None
    customStyle=None

    Action_Types=("Break","Check Checkbox","Click Button","Click Link","Click Submit","Click Reset","Fill Input","Select Option by Text","Select Option by Value" ,"Wait")
    Action_On=("ByName","ById","BySelector")

    def set_theme(self,event,frameData):
        self.customStyle= ThemedStyle(frameData)
        if(self.themeName=="arc"):
            self.customStyle.theme_use('arc')
            self.customStyle.configure('TButton', foreground = '#343a40', background = '#44a2d2', Font=("Verdana",10))
            self.customStyle.configure('TreeViewAction.TButton', foreground = '#44a2d2', background = '#ffffff',Font=("Verdana",10))
            self.customStyle.configure('TCombobox', background = '#f2f5f7',Font=("Verdana",10))
            self.customStyle.configure('TFrame', background = '#ffffff')
            self.customStyle.configure('Topframe.TFrame', background = '#44a2d2')
            self.customStyle.configure('TEntry', background = '#f2f5f7',Font=("Verdana",10))
        else :
            self.customStyle.theme_use('default')
        print (self.customStyle.theme_use())



    def on_enter_menu(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_TOP_BACKGROUND

    def on_leave_menu(self,e):
        e.widget['background'] = self.COLOR_TOP_BACKGROUND
        e.widget['foreground'] = self.COLOR_FOREGROUND     

    def on_enter_button(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_TOP_BACKGROUND

    def on_leave_button(self,e):
        e.widget['background'] = self.COLOR_TOP_BACKGROUND
        e.widget['foreground'] = self.COLOR_FOREGROUND 

    def __init__(self):                
        self.LoadAllData()
        
        
    
    def LoadAllData(self):
        if not os.path.exists(self.ConfigFileName):
            self.fnc_CreateDefaultFile()

        self.config_file.read(self.ConfigFileName)
        self.Name = self.config_file['AFill_Register']['Name']
        self.Email = self.config_file['AFill_Register']['Email']
        self.ContactNo =self.config_file['AFill_Register']['ContactNo']
        self.FilePath = self.config_file['AFill_FileSetting']['FilePath']
        self.TemplateFileName = self.config_file['AFill_FileSetting']['TemplateFileName']
        self.DataFileName = self.config_file['AFill_FileSetting']['DataFileName']
        self.ChromeDriver = self.config_file['AFill_FileSetting']['ChromeDriver']
        self.UserName = self.config_file['AFill_Users']['UserName']
        self.Password = self.config_file['AFill_Users']['Password']
        self.IO_Name=self.config_file['InputTemplate']['IO_Name'].split(",")
        self.IO_Template=self.config_file['InputTemplate']['IO_Template'].split(",")
        self.themeName= self.config_file['Themes']['Theme_Name']

        

    def fnc_CreateDefaultFile(self):    
        # ADD SECTION
        self.config_file.add_section("AFill_FileSetting")
        # ADD SETTINGS TO SECTION
        self.config_file.set("AFill_FileSetting", "FilePath", "")
        self.config_file.set("AFill_FileSetting", "TemplateFileName", "")
        self.config_file.set("AFill_FileSetting", "DataFileName", "")

        self.config_file.add_section("AFill_Users")
        # ADD SETTINGS TO SECTION        
        self.config_file.set("AFill_Users", "UserName", "Admin")
        self.config_file.set("AFill_Users", "Password", "afill123")

        self.config_file.add_section("AFill_Register")
        # ADD SETTINGS TO SECTION        
        self.config_file.set("AFill_Register", "Name", "")
        self.config_file.set("AFill_Register", "Email", "")
        self.config_file.set("AFill_Register", "ContactNo", "")

        self.config_file.add_section("InputTemplate")
        self.config_file.set("InputTemplate", "IO_Name", "Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Age,Gender,Country of Birth,Nationality,Address Line 1,Address Line 2,City,Country,Postcode,Address Type,Address Status,Date From,Date To,Telephone,Mobile,E Mail")
        self.config_file.set("InputTemplate", "IO_Template", "Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Age,Gender,Country of Birth,Nationality,Address Line 1,Address Line 2,City,Country,Postcode,Address Type,Address Status,Date From,Date To,Telephone,Mobile,E-Mail")

        self.config_file.add_section("Themes")
        self.config_file.set("Themes", "Theme_Name", "arc")
        

        # SAVE CONFIG FILE
        with open(self.ConfigFileName, 'w') as configfileObj:
            self.config_file.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()
        self.LoadAllData()
        print("Config file 'configurations.ini' created")

    def fnc_RegisterUser(self,Name,Email,ContactNo):
        self.config_file.read("configurations.ini")
        # UPDATE A FIELD VALUE
        self.config_file["AFill_Register"]["Name"]=Name
        self.config_file["AFill_Register"]["Email"]=Email
        self.config_file["AFill_Register"]["ContactNo"]=ContactNo        
        # ADD A NEW FIELD UNDER A SECTION
        #self.config_file["AFill_Register"].update({"Format":"(message)"})

        # SAVE THE SETTINGS TO THE FILE
        with open(self.ConfigFileName,"w") as file_object:
            self.config_file.write(file_object)
        self.LoadAllData()

