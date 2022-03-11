# Importing Tkinter module
from asyncio.windows_events import NULL
from tkinter import *
# from tkinter.ttk import *


MENU_BACKGROUND="#6272a4";
MENU_FOREGROUND="#f8f8f2";
MENU_HOVER_BACKGROUND="#bd93f9";
MENU_HOVER_FOREGROUND="#f8f8f2";
MENU_SELECTED_BACKGROUND="#ff79c6";
MENU_SELECTED_FOREGROUND="#ffffff";



def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def on_enter(e):
#    global selected_button
#    if (selected_button != None):
#        if(selected_button.widget['text']!=e.widget['text']):
            e.widget['background'] = MENU_HOVER_BACKGROUND
            e.widget['foreground'] = MENU_HOVER_FOREGROUND

def on_leave(e):
#    global selected_button
#    if(selected_button != None):
#        if(selected_button.widget['text']!=e.widget['text']):
            e.widget['background'] = MENU_BACKGROUND
            e.widget['foreground'] = MENU_FOREGROUND  

#def menuSelected(e):
#    global selected_button    
#    if(selected_button != None):
#        selected_button.widget['foreground']=MENU_FOREGROUND
#        selected_button.widget['background']=MENU_BACKGROUND
#    e.widget['background'] = MENU_SELECTED_BACKGROUND
#    e.widget['foreground'] = MENU_SELECTED_FOREGROUND
#    selected_button=e
# Creating master Tkinter window
master = Tk()
master.geometry("175x210")

# Tkinter string variable
# able to store any string value
v = StringVar(master, "1")

# Dictionary to create multiple buttons
values = {"RadioButton 1" : "1",
		"RadioButton 2" : "2",
		"RadioButton 3" : "3",
		"RadioButton 4" : "4",
		"RadioButton 5" : "5"}

# Loop is used to create multiple Radiobuttons
# rather than creating each button separately
for (text, value) in values.items():
    button = Radiobutton(master, text = text, variable = v,	value = value, indicator = 0, background = "#6272a4", fg="#f8f8f2", 
    selectcolor=MENU_SELECTED_BACKGROUND 
    ,borderwidth=0
    ,activebackground=MENU_HOVER_BACKGROUND,activeforeground=MENU_HOVER_FOREGROUND
    #,highlightbackground=MENU_HOVER_BACKGROUND,highlightcolor=MENU_HOVER_FOREGROUND
    )
    button.pack(fill = X, ipady = 5)
    #button.bind('<Enter>', on_enter)
    #button.bind('<Leave>', on_leave)
    
#btn=Radiobutton(master, text = "Hello World", variable = v,	value = "6", indicator = 0,  background = "#6272a4", fg="#f8f8f2", selectcolor=MENU_SELECTED_BACKGROUND,
#activebackground=MENU_HOVER_BACKGROUND,activeforeground=MENU_HOVER_FOREGROUND)
#btn.pack(fill = X, ipady = 5)
#btn.bind('<Enter>', on_enter)
#btn.bind('<Leave>', on_leave)
#selected_button=btn
# Infinite loop can be terminated by
# keyboard or mouse interrupt
# or by any predefined function (destroy())
mainloop()
