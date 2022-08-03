import tkinter as tk
import sys
import database
import exif_api
DEBUG = True
# DEBUG = False
VERBOSE = True

list_letters = ["A","B","C","D","E","F","G"]
list_numbers = [str(i) for i in range(1,10)]

filename = sys.argv[1]

# Interface with the database
# Get all files and tags from the database
datab = database.database()
datab.initialize_db() 

# Check if file exists in database
index = -1
if filename in datab.file_list:
    index = datab.file_list.index(filename)

if VERBOSE:
    if index == -1:
        print("tagger: File does not exist in the database.")
    else:
        print("tagger: File exists in database. Index:", index)
        print("tagger: Tags from database: ", datab.db_list[index][3])

db_tagstr = ""
if index != -1:
    for tag in datab.db_list[index][3]:
        db_tagstr += tag + ","

# Check which tags already exist in the file
tt = exif_api.rw_tags(filename)
tt.read_tags(VERBOSE) 
has_tags = False
if len(tt.tag_list) != 0:
    has_tags = True

file_tagstr = ""
for tag in tt.tag_list:
    file_tagstr += tag + ","

if VERBOSE:
    if has_tags:
        print("tagger: Tags read from file: ", tt.tag_list)
    else:
        print("tagger: File has no tags.")


# The database is organized as follows. datab.db_list:
# [[id, Filename, loc, tags], 
#  [        ...            ],
#           ...
print(file_tagstr)
print(db_tagstr)

tagset = set(datab.tag_list)







textin = "In database"
if index == -1:
    textin = "Not in database"

top = tk.Tk()
top.title("floatme")

title = tk.Label(top, text="Editing tags for file {0}".format(filename))
title.config(font=("Helvetica", 22))

dbstatus = tk.Label(top, text=textin)
dbstatus.config(font=("Helvetica", 15))

db_taglist = tk.Label(top, text="current tags: " + db_tagstr)
db_taglist.config(font=("Helvetica", 15))

file_taglist = tk.Label(top, text="current tags: " + file_tagstr)
file_taglist.config(font=("Helvetica", 15))


new_taglist = tk.Label(top, text="new tags: " )
new_taglist.config(font=("Helvetica", 15))

rep_taglist = tk.Label(top, text="rep tags: ")
rep_taglist.config(font=("Helvetica", 15))

# Scrollbar and itemlist
scrollbar = tk.Scrollbar(top)
mylist = tk.Listbox(top, yscrollcommand = scrollbar.set,font=("Helvetica",15), width=14)
for line in range(len(datab.tag_list)):
   mylist.insert(tk.END, datab.tag_list[line])
scrollbar.config( command = mylist.yview )

string=""
entry = tk.Entry(top, bg="white", textvariable=string,width=40,font=("Helvetica", 20))


# Grid placement
title.grid(       row=0, column=0, columnspan=3)
dbstatus.grid(    row=1, column=2, columnspan=1)
db_taglist.grid(  row=2, column=2, columnspan=1)
file_taglist.grid(row=3, column=2, columnspan=1)
entry.grid(       row=4, column=2, columnspan=1)
new_taglist.grid( row=5, column=2, columnspan=1)
rep_taglist.grid( row=6, column=2, columnspan=1)
scrollbar.grid(   row=1, column=1, rowspan=4, sticky='ns')
mylist.grid(      row=1, column=0, rowspan=4, sticky='ns')

# Focus on entry
entry.focus_set()


def update(event):
    if(DEBUG):
        print("up")

    entry_set = set()
    entry_set = { s for s in entry.get().split(",")}
    
    isect = entry_set.intersection(tagset)
    diff = entry_set - isect
    if(DEBUG):
        print("isect:",isect)
        print("diff:",diff)

    new_str = "new tags:"
    for i in diff:
        new_str += i + ","

    rep_str = "repeated tags:"
    for i in isect:
        rep_str += i + ","

    new_taglist['text'] = new_str
    rep_taglist['text'] = rep_str




def hello(event):
    newtags = [i.strip() for i in entry.get().split(",")]
    loc = ""
    newtags1 = []
    for tag in newtags:
        if len(tag)>1 and tag[0] in list_letters and tag[1] in list_numbers:
            loc = tag
        else:
            newtags1.append(tag)
    print("NEWTAGS")
    print(newtags1)
    print("LOC")
    print(loc)
    if loc == "":
        print("NO LOC")
        exit(1)
    # tt.append_tags(newtags, VERBOSE)
    tt.overwrite_tags(newtags, VERBOSE)
    print(filename)
    datab.add_entry(filename, loc, tt.tag_list, VERBOSE)
    datab.write_db()
    datab.generate_tags()
    datab.write_tags()

    top.destroy()

def stop(event):
    top.destroy()

top.bind('<Return>', hello)
top.bind('<Escape>', stop)
top.bind('<KeyPress>', update)

top.mainloop()
# print(string)
