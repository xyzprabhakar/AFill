import configparser
import helper

class GenerateConfig:



    # CREATE OBJECT
    config_file = configparser.ConfigParser()
    ConfigFileName="configurations.ini"
    Name=None
    Email=None
    ContactNo=None

    def __init__(self):        
        self.LoadAllData()
    
    def LoadAllData(self):
        self.config = helper.read_config()
        self.Name = self.config['AFill_Register']['Name']
        self.Email = self.config['AFill_Register']['Email']
        self.ContactNo = self.config['AFill_Register']['ContactNo']
        self.FilePath = self.config['AFill_FileSetting']['FilePath']
        self.TemplateFileName = self.config['AFill_FileSetting']['TemplateFileName']
        self.DataFileName = self.config['AFill_FileSetting']['DataFileName']
        self.UserName = self.config['AFill_Users']['UserName']
        self.Password = self.config['AFill_Users']['Password']

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

        # SAVE CONFIG FILE
        with open(r"configurations.ini", 'w') as configfileObj:
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
        with open("configurations.ini","w") as file_object:
            self.config_file.write(file_object)
        self.LoadAllData()

