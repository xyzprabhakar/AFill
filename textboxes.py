# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create an instance of tkinter frame
win=Tk()

# Set the geometry
win.geometry("700x350")

# Add a Scrollbar(horizontal)
v=Scrollbar(win, orient='vertical')
v.pack(side=RIGHT, fill='y')

# Add a text widget
tx=Text(win, font=("Georgia, 24"), yscrollcommand=v.set)



for i in range(50):
	# the label for user_name
	user_name = Label(tx,
					text = "Username" + str(i)).grid(row=(i*2)+1,
											column=0)		
	# the label for user_password
	user_password = Label(tx,
						text = "Password").grid(row=(i*2)+2,
											column=0)
	user_name_input_area = Entry(tx,
							width = 30).grid(row=(i*2)+1,
											column=1)
	
	user_password_entry_area = Entry(tx,
								width = 30).grid(row=(i*2)+2,
											column=1)
	

# Attach the scrollbar with the text widget
v.config(command=tx.yview)
tx.pack()

win.mainloop()
