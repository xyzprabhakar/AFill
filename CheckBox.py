import tkinter as tk

root = tk.Tk()
root.geometry("300x200")

w = tk.Label(root, text ='GeeksForGeeks', font = "50")
w.pack()

Checkbutton1 = tk.IntVar()
Checkbutton2 = tk.IntVar()
Checkbutton3 = tk.IntVar()

Button1 = tk.Checkbutton(root, text = "Tutorial",
					variable = Checkbutton1,
					onvalue = 1,
					offvalue = 0,
					height = 2,
					width = 10)

Button2 = tk.Checkbutton(root, text = "Student",
					variable = Checkbutton2,
					onvalue = 1,
					offvalue = 0,
					height = 2,
					width = 10)

Button3 = tk.Checkbutton(root, text = "Courses",
					variable = Checkbutton3,
					onvalue = 1,
					offvalue = 0,
					height = 2,
					width = 10)
	
Button1.pack()
Button2.pack()
Button3.pack()

root.mainloop()
