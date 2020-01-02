# import the necessary packages
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
from random import randint
import os
import time

def select_astore():
    filename = askopenfilename(title = "Select Astore",filetypes = (("Astore Models","*.astore"),("all files","*.*")))
    change_astore(filename)
    return
   
def change_astore(path):
    return

def popupmsg():
    popup = tkinter.Tk()
    popup.wm_title("Changing Astore")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    
    
root = Tk()
root.title("SAS Astore Switcher")
root.iconbitmap('icon.ico')
header = Canvas(root, width=700, height=125)
header.grid(row=0, column=0, columnspan=5)
logo = ImageTk.PhotoImage(Image.open("sasbluelogo.png"))  
header.create_image(0,0,anchor=NW,image=logo)
 
title = Canvas(root, width=700, height=25)
title.grid(row=1, column=0, columnspan=5)
title.create_text(30,0, anchor=NW, fill="darkblue", font="Times 18 bold", text = "Change Astore to new model:")

mining      = ImageTk.PhotoImage(Image.open("mining.png"))  
insurance   = ImageTk.PhotoImage(Image.open("insurance.png"))  
banking     = ImageTk.PhotoImage(Image.open("banking.png"))  
government  = ImageTk.PhotoImage(Image.open("police.png"))  
health      = ImageTk.PhotoImage(Image.open("health.png"))  
unknown     = ImageTk.PhotoImage(Image.open("unknown.png"))  

Button(root, text="Mining & Utilities", font="Times 12 bold", image=mining, command= lambda: change_astore("")).grid(row=2, column=0)
Button(root, text="Insurance", font="Times 12 bold", image=insurance, command= lambda: change_astore("")).grid(row=2, column=1)
Button(root, text="Banking", font="Times 12 bold", image=banking, command= lambda: change_astore("")).grid(row=2, column=2)
Button(root, text="Government", font="Times 12 bold", image=government, command= lambda: change_astore("")).grid(row=4, column=0)
Button(root, text="Health", font="Times 12 bold", image=health, command= lambda: change_astore("")).grid(row=4, column=1)
Button(root, text="Create New", font="Times 12 bold", image=unknown, command= select_astore).grid(row=4, column=2)

labels = Canvas(root, width=700, height=25)
labels.grid(row=3, column=0, columnspan=5)
labels.create_text(50,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Mining & Utilities")
labels.create_text(300,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Insurance")
labels.create_text(520,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Banking")

labels = Canvas(root, width=700, height=25)
labels.grid(row=5, column=0, columnspan=5)
labels.create_text(50,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Government")
labels.create_text(300,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Health")
labels.create_text(520,0, anchor=NW, fill="darkblue", font="Times 12 bold", text = "Select New Astore")

footer = Canvas(root, width=700, height=25)
footer.grid(row=6, column=0, columnspan=5)
ftr = ImageTk.PhotoImage(Image.open("bluestrip.png"))  
footer.create_image(0,0,anchor=NW,image=ftr)


mainloop()



