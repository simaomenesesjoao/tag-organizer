import subprocess
import os
import sys

# DEBUG = True
DEBUG = False
list_letters = ["A","B","C","D","E","F","G"]
list_numbers = [str(i) for i in range(1,10)]

class database:
    dbdir = "/home/simao/builds/organizer/db/"
    dbfile = dbdir + "db.txt"
    tagfile = dbdir + "tags.txt"

    db_list = []
    file_list = [] 
    Nitems = 0

    tag_list = []
    tag_dic = {}

    def load_db(self, filename):
        # Reads the db.txt file and loads it into memory in the form of a list

        f = open(filename,'r')
        db_str = f.read()
        db_list = []
        f.close()

        if(DEBUG):
            print(db_str)

        # Iterate over all the lines read
        for line in db_str.split("\n"):
            if line != "":

                if(DEBUG):
                    print(line)

                ident,filename, tagloc = line.split(" ")

                tl = []
                loc = ""
                found_loc = False
                for word in tagloc.split(","):


                    # Check which one of the tags has the location. The location is of the form A13, so
                    # the first character is an uppercase letter and the second (and possibly third) is a number
                    # There can only be one location, and there must exist at least one location
                    if word[0] in list_letters and word[1] in list_numbers:
                        if(found_loc):
                            print("Location already found for this entry {0}. Check whether entry has two locations.".format(line))
                            exit(1)
                        loc = word
                        found_loc = True
                    else:

                        tl.append(word)

                if(not found_loc):
                    print("There is no location for this entry: {0}.".format(line))
                    exit(1)

                # Add to database
                entry = [int(ident),filename, loc, tl]
                db_list.append(entry)

                if(DEBUG):
                    print(entry)

        # Update database in memory
        self.db_list = db_list
        self.Nitems = len(self.db_list)


        # List of files
        filelist = []
        for i in db_list:
            filelist.append(i[1])

        self.file_list = filelist


    def generate_tags(self):
        ''' Generate the tags from the database in memory'''
        tagset = set()
        tagdic = {}

        # Find the dictionary keys
        for entry in self.db_list:
            tags = entry[3]
            for tag in tags:
                tagset.add(tag)

        # Generate the dictionary keys
        for tag in tagset:
            tagdic[tag] = []

        # Fill the dictionary
        for entry in self.db_list:
            ident,tags = entry[0],entry[3]
            for tag in tags:
                tagdic[tag].append(ident)

        # update tag list in memory
        self.tag_list = list(tagset)
        self.tag_dic = tagdic




    def write_tags(self):
        # Write list of tags in memory to a file

        tagstr = ""
        for tag in self.tag_list:
            # print(tag)
            matches = self.tag_dic[tag]
            s = ""
            for match in matches:
                s += str(match) + ","
            tagstr += tag + " " + s[:-1] + "\n"

        f = open(self.dbdir + "tags.txt", 'w')
        f.write(tagstr)
        f.close()




    def read_tags(self, filename):
        # Read list of tags in a file into memory
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        dic = {}
        tl = []
        for line in lines:
            tag, matches = line.split(" ")
            match_list = []
            for match in matches.split(","):
                match_list.append(int(match))

            dic[tag] = match_list
            tl.append(tag)

        # update tag list in memory
        self.tag_list = tl
        self.tag_dic = dic



    def initialize_db(self):
        self.read_tags(self.tagfile)
        self.load_db(self.dbfile)



    def add_entry(self, filename, loc, tags, verbose):
        # Make sure 'tags' is a list!
        if not (type(tags) is list):
            print("add_entry(..., tags) tags has to be a list")
            exit(1)

        # Check if entry already exists
        index = -1
        if filename in self.file_list:
            index = self.file_list.index(filename)

        # File doesn't exist
        if index == -1:
            if verbose:
                print("File doesn't exist in database.")
            newtaglist = sorted(list(set(tags).union(set(["TAG"]))))
            entry = [self.Nitems, filename, loc, newtaglist]

            # update the database
            self.db_list.append(entry)
            self.Nitems += 1

        # File exists
        if index != -1:
            if verbose:
                print("File exists in database.")

            entry = self.db_list[index]
            # oldtags = entry[3]
            # newtaglist = sorted(list(set(oldtags).union(set(tags), set(["TAG"]))))
            newtaglist = sorted(list(set(tags).union(set(["TAG"]))))

            # update the database
            self.db_list[index] = [entry[0], entry[1], entry[2], newtaglist]


        # Update the tags
        self.generate_tags()

    def write_db(self):
        # Create the database string from the database list so that it can
        # be written into memory later

        db_str = ""
        for entry in self.db_list:
            ident = entry[0]
            filename = entry[1]
            loc = entry[2]
            loctags = list(set([loc, *entry[3]]))



            # update the database string
            tagstr = ""
            if len(loctags) != 0:
                for tag in loctags:
                    tagstr += tag + ","

            db_str += str(ident) + " " + filename + " " + tagstr[:-1] + "\n"

        f = open(self.dbfile, 'w')
        f.write(db_str)
        f.close()

        self.generate_tags()




if __name__ == "__main__":
    VERBOSE = True

    daba = database()
    daba.initialize_db()

    # print(daba.db_list)

    # print(daba.file_list)
    # daba.add_entry("/boas/aa.pdf", "A95", ["2020","rose","gato"], VERBOSE)
    # daba.add_entry("/meme/aa.pdf", "A96", ["2021","yolo","gato"], VERBOSE)
    # daba.add_entry("/adfs/ga.pdf", "A93", [], VERBOSE)
    # daba.write_db()
    daba.generate_tags()
    daba.write_tags()

