# import tkinter module
#from tkinter import  * 
#from tkinter.ttk import *
import tkinter as tk


class AutoFill(tk.Frame):
    def __init__(self, isapp=True, name='AutoFill'):
        tk.Frame.__init__(self, name=name)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master.title('Auto Fill')
        self.isapp = isapp
        self._create_widgets()


#Theme Color
COLOR_BACKGROUND="#282c37"
COLOR_FOREGROUND="#f5f5f5"
COLOR_MENU_BACKGROUND="#212528"
COLOR_BUTTON_HOVER_BACKGROUND="#283234"
COLOR_BUTTON_PRESSED_BACKGROUND="#bd55f9"
COLOR_BUTTON_PRESSED_FOREGROUND="#f5f5f5"






# creating main tkinter window/toplevel
master = tk.Tk()
master.geometry("768x480")
master.config(bg="grey")



#Add All Frame
frmTopFrame=tk.Frame(master,width=100, height=50, background=COLOR_MENU_BACKGROUND)
frmTopFrame.pack(side=tk.TOP,fill=tk.X)

frmMainFrame=tk.Frame(master)
frmMainFrame.pack()

frmMenuFrame=tk.Frame(frmMainFrame,bg=COLOR_MENU_BACKGROUND)
#frmMenuFrame.configure(bg=COLOR_MENU_BACKGROUND)
frmMenuFrame.pack(side=tk.LEFT,fill=tk.BOTH)

frmContentMenuSepratorFrame=tk.Frame(frmMainFrame)
frmContentMenuSepratorFrame.pack(side=tk.LEFT)

frmContentFrame=tk.Frame(frmMainFrame,bg=COLOR_BACKGROUND )
frmContentFrame.pack()

# b4_button = tk.Button(frmTopFrame, text ="Geeks4", fg ="green")
# b4_button.pack( side = tk.LEFT)
  
# b5_button = tk.Button(frmTopFrame, text ="Geeks5", fg ="green")
# b5_button.pack( side = tk.LEFT)

master.mainloop()

if __name__ == '__main__':
    AutoFill().mainloop()

