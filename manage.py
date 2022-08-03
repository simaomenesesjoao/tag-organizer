import subprocess
import os
import sys

DEBUG = False


class database:
    dbdir = "/home/simao/builds/organizer/db/"
    db = []
    tags = []
    db_txt = ""
    got_db = False
    got_tags = False

    # Methods regarding the database


    def get_db_from_str(self):
        if(DEBUG):
            print("Entered get_db_from_str")

        self.db = []
        splitted = self.db_txt.split("\n")[:-1]
        # print(splitted)
        for i in splitted:
            # print(i)
            b = i.split()
            filename = b[0]
            tags = b[1].split(",")
            # print(b, tags)
            loc = tags[1]

            # print(filename, tags)
            self.db.append([filename,tags,loc])

        self.got_db = True
        # print(self.db_txt)
        # return self.db

        if(DEBUG):
            print("Left get_db_from_str")

    # Get the db_txt string and do some processing into a db list
    def get_dbstr(self):
        f = open(self.dbdir + "db.txt")
        a = f.readlines()
        f.close()
        # self.db = []
        for i in a:
            self.db_txt += i

        # self.got_db = True
        # print(self.db_txt)
        # return self.db

    # Create the db_txt variable from the files in a directory
    def create_db_from_dir(self):
        dir1 = "/home/simao/digitalizacoes/test_org/"
        listdir = os.listdir(dir1)
        db_string = ""
        self.db = []

        for filename in listdir:
            if filename[-4:] == ".pdf":
                # print(filename)

                command = "exiftool {0}".format(dir1+filename)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                a = p.stdout.readlines()

                found = False
                data = ""
                for i in a:
                    # print(i)
                    line = i.decode('utf-8').split()
                    if line[0] == "Creator":
                        data = line[-1]
                        found = True
                        break
                if found: 
                    db_string += dir1 + filename + " " + data + "\n"

        self.db_txt = db_string


    def write_db(self):
        f = open(self.dbdir + "db.txt", 'w')
        for line in self.db_txt:
            f.write(line)
        f.close()

        





    # Iterate over all the tags of all the entries in the database
    def get_tags_from_db_inram(self):
        assert self.got_db == True, "Database needs to be retrieved before using this method. Use self.get_db()"

        stags = {"TAG"}
        N = len(self.db)
        for i in range(N):
            line = self.db[i]
            # print(line)
            for j in line[1]:
                if j != "TAG" and j[0] != "A":
                    # print(j)
                    stags = stags.union({j})
                    # print(tags)

        self.tags = list(stags)
        self.got_tags = True
        return self.tags

    # Read the tag files
    def get_tags_from_tagfile(self):

        self.tag_dic = {}

        list_files = os.listdir(self.dbdir)
        for i in list_files:
            if i[:3] == "TAG":
                f = open(self.dbdir + i)
                a = f.readlines()
                f.close()
                self.tag_dic[i[4:-4]] = [j[:-1] for j in a]
        # print(list_files)
        # print(dic)


        self.tags = self.tag_dic.keys()
        self.got_tags = True
        return self.tag_dic


    # Create files for each tag
    def create_tag_files(self):
        if DEBUG: 
            print("Entered create_tag_files")
        dic = {}
        assert self.got_db == True, "db must be set"
        for entry in self.db:
            filename = entry[0]
            for tag in entry[1]:
                if tag != "TAG" and tag[0] != "A":
                    if tag not in dic.keys():
                        dic[tag] = [filename]
                    else:
                        dic[tag].append(filename)



        # Creat the files
        for tag in dic.keys():
            # print(tag)
            f = open(self.dbdir + "TAG_" + str(tag) + ".txt", 'w')
            for filename in dic[tag]:
                f.write(filename + "\n")
            f.close()



if __name__ == "__main__":
    datab = database()
    # ret = datab.get_db()
    # print(ret)

    # print(tags)
    datab.create_db_from_dir()
    datab.get_db_from_str()
    datab.write_db()
    tags = datab.get_tags_from_tagfile()
    # tags = datab.get_tags_from_db_inram()
    datab.create_tag_files()
    # print(tags)
