import tkinter as tk
import time
import subprocess
import database
from PIL import ImageTk,Image


datab = database.database()
datab.initialize_db()
taglist = datab.tag_list
names = datab.file_list
print(taglist)

tagstr = ""
for tag in taglist:
    tagstr += tag + "\n"

def get_intersect(list_tags):
    joined = set()

    # Initialize the set
    if list_tags[0] in datab.tag_list:
        joined = set(datab.tag_dic[list_tags[0]])

    print()
    print(joined)
    print()

    # Intersect all the elements in list_tags
    for s in list_tags:
        if s in datab.tag_list:
            joined = joined.intersection(datab.tag_dic[s])
            print(joined)

    namelist = []
    for i in list(joined):
        namelist.append(datab.db_list[i][1])
    return namelist


top = tk.Tk()
top.title("floatme")

# w0 = tk.Label(top, bg="white", text=tagstr,width=10,font=("Helvetica", 20))
# w0.grid(column=0,row=0, rowspan=2)

scrollbar = tk.Scrollbar(top)
scrollbar.grid(column=1,row=0,rowspan=2,sticky='ns')

mylist = tk.Listbox(top, yscrollcommand = scrollbar.set,font=("Helvetica",15), width=14)
for line in range(len(taglist)):
   mylist.insert(tk.END, taglist[line])

# mylist.pack( side = LEFT, fill = BOTH )
mylist.grid(column=0,row=0,rowspan=2,sticky='ns')
scrollbar.config( command = mylist.yview )




w1 = tk.Entry(top, bg="white", width=40, font=("Helvetica",20))
w1.grid(column=2, row=0)
w1.focus_set()



scrollbar2 = tk.Scrollbar(top)
scrollbar2.grid(column=3,row=1,rowspan=1,sticky='ns')

list2 = tk.Listbox(top, font=("Helvetica",15), yscrollcommand = scrollbar2.set)
list2.grid(column=2, row=1,sticky='nsew')
list2.insert(tk.END,"filenames")
scrollbar2.config(command = list2.yview)
# def on_enter(event):
    # print("A")

win2 = tk.Toplevel(top)
canvas = tk.Canvas(win2, width = 500, height = 500)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("/home/simao/builds/organizer/b.png"))
img2 = ImageTk.PhotoImage(Image.open("/home/simao/builds/organizer/a.png"))
image_on_canvas = canvas.create_image(50,50, anchor=tk.NW, image=img)


win2.withdraw()

def on_enter(event):
    win2.deiconify()
def on_leave(event):
    win2.withdraw()


line = -1
oldline = -1
def mot_enter(event):
    # print(event.x, event.y)
    global line, oldline
    line = list2.index("@{0},{1}".format(event.x, event.y))
    if line != oldline:
        list2.itemconfig(line, {'bg':f'#{180:02x}{180:02x}{254:02x}'})


        command="evince " + list2.get(line)
        item = list2.get(line)
        command="pdftoppm -png -rx 50 -ry 50 -f 1 -l 1 " + item + " /home/simao/builds/organizer/doc"
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(command)
        # canvas.itemconfig(image_on_canvas, image = img2)
        # canvas.configure(iage = img2)

        global img2
        img2 = ImageTk.PhotoImage(Image.open("/home/simao/builds/organizer/doc-1.png"))
        canvas.itemconfig(image_on_canvas, image=img2)


        if oldline != -1:
            list2.itemconfig(oldline, {'bg':'white'})
            
        oldline=line
        print(line,list2.get(line))

def on_one(event):
    print("click :D", line)
    print(list2.get(line))
    command="evince " + list2.get(line)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # a.append(p.stdout.readlines())
    # print(a)
    # time.sleep(1)
    # top.destroy()

list2.bind("<Enter>", on_enter)
list2.bind("<Leave>", on_leave)
list2.bind("<Motion>", mot_enter)
list2.bind("<1>", on_one)

# def fun1():
    # im3 = ImageTk.PhotoImage(Image.open("/home/simao/builds/organizer/a.png"))
    # return im3

def update(event):
    text = w1.get()
    list_int = get_intersect(text.split(","))

    global line, oldline
    line = -1
    oldline = -1
    list2.delete(0, 'end')
    for i in list_int:
        list2.insert(tk.END,i)
    # win2.update()
    print("update")


top.bind('<KeyPress>', update)
top.mainloop()
