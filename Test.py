
from tkinter import *

tk=Tk()

tk.columnconfigure(0, weight=1)
tk.rowconfigure(0, weight=1)
tk.rowconfigure(1, weight=100)

f=Frame(tk)
f2=Frame(tk)

f.grid(row=0, column=0, sticky=E+W)
f2.grid(row=1, column=0, sticky=N+S+E+W)

t=Text(f, height=1)
t2=Text(f2)
l=Label(f, text="label")
b=Button(f, text="button")

l.pack(side=LEFT)
t.pack(side=LEFT, fill=X, expand=True)
b.pack(side=LEFT)
t2.pack(fill=BOTH, expand=True)

tk.mainloop()