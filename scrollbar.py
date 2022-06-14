from tkinter import *
from tkinter import ttk




root=Tk()
root.title("scrollbar")
root.geometry("500x400")

main_frm=Frame(root)
main_frm.pack(fill=BOTH,expand=1)

my_canvas=Canvas(main_frm)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

scr=ttk.Scrollbar(main_frm,orient=VERTICAL,command=my_canvas.yview)
scr.pack(side=RIGHT,fill=Y)

scr1=ttk.Scrollbar(main_frm,orient=HORIZONTAL,command=my_canvas.xview)
scr1.pack(side=BOTTOM,fill=X)

my_canvas.configure(yscrollcommand=scr.set,xscrollcommand= scr1.set)
my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

scFrame= Frame(my_canvas)
my_canvas.create_window((0,0),window=scFrame,anchor="nw")

for thing1 in range(10):
    for thing in range(100):
        Button(scFrame,text=f'Button {thing1} _ {thing}').grid(row=thing,column=thing1,pady=10,padx=10)


root.mainloop()