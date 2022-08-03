import subprocess
import sys

DEBUG = True
# DEBUG = False

# This is a short script which automates the process of checking which
# tags are already present and writing to the correct field "Creator"
# This script DOES NOT sanitize the input

# Make it more robust! Check for errors! check if program finished without errors!

list_letters = ["A","B","C","D","E","F","G"]
list_numbers = [str(i) for i in range(1,10)]


class rw_tags:
    tag_list = []
    filename = "" 
    loc = ""
    has_tags = False

    def __init__(self, filename):
        self.filename = filename


    def read_tags(self, verbose=False):

        # Read metadata
        command = "exiftool {0}".format(self.filename)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        a = p.stdout.readlines()

        # Find the "Creator" field
        found = False
        data = ""
        for i in a:
            # print(i)
            line = i.decode('utf-8').split()
            if line[0] == "Creator":
                data = line[-1]
                found = True
                break

        if data == "" or data == ":":
            return -1

        if verbose:
            print("exif_api: Tags read from file: " + data)

        words = data.split(",")
        tags = []
        loc = ""
        found_TAG = False
        for word in words:
            if len(word)>1 and word[0] in list_letters and word[1] in list_numbers:
                loc = word

            if word == "TAG" and not found_TAG:
                found_TAG = True

            tags.append(word)

        # if not found_TAG:
            # print("The tag called 'TAG' was not found in the list of tags. Exiting.")
            # exit(1)


        self.tag_list = tags
        self.loc = loc
        self.has_tags = True

        return 0


    def append_tags(self, new_tags, verbose):
        # Add the new tags to the list of already existing tags in the file
        # Automatically appends the tag "TAG" if it doesn't already exist
        if DEBUG:
            print("append_tags called")

        # Check if input is correct
        if type(new_tags)!=list:
            print("The argument to append_tags has to be a list.")
            exit(1)
        else:
            for word in new_tags:
                if type(word) != str:
                    print("The elements of the list in the argument of append_tags have to be strings")
                    exit(1)
                

        # Create the final tag list, without duplicates, and sort it alphabetically
        newtaglist = sorted(list(set(self.tag_list).union(set(new_tags), set(["TAG"]))))

        # Put it into a string
        newdata = ""
        for i in newtaglist:
            newdata += i + ","
        newdata1 = newdata[:-1] # remove the last comma


        if verbose:
            print("Appending new tags: " + newdata1 + " to the file " + self.filename + " with tags " + str(self.tag_list))

        # Update the tag list
        self.tag_list = newtaglist

        # Write the updated tag list to the file's metadata and capture exceptions
        write = '-Creator=' + newdata1
        commandlist = ["exiftool", self.filename, write, "-overwrite_original"]
        try:
            p = subprocess.run(commandlist, capture_output = True, check=True)
        except:
            print("Exception occured when running exiftool in 'tag.py' with argument:", commandlist)
            exit(1)






    def overwrite_tags(self, tags, verbose):
        # Completely overwrites all the tags in the file by the tags specified.
        # Automatically adds the tag "TAG"
        if DEBUG:
            print("overwrite_tags called")

        # Check if input to function is correct
        if type(tags)!=list:
            print("The argument to overwrite_tags has to be a list.")
            exit(1)
        else:
            for word in tags:
                if type(word) != str:
                    print("The elements of the list in the argument of overwrite_tags have to be strings")
                    exit(1)

        # Add 'TAG' if it doesn't already exist
        new_tags = list(set(["TAG"]).union(set(tags)))

        # put the elements of the list into a string 
        newdata = ""
        for i in new_tags:
            newdata += i + ","
        newdata1 = newdata[:-1] # remove the last comma

        if verbose:
            print("Replacing existing tags " + str(self.tag_list) + " by: " + newdata1 + " in the file " + self.filename)

        # Update the tag list
        self.tag_list = new_tags

        # Write the updated tag list to the file's metadata and capture exceptions
        write = '-Creator=' + newdata1 
        commandlist = ["exiftool", self.filename, write, "-overwrite_original"]
        try:
            p = subprocess.run(commandlist, capture_output = True, check=True)
        except:
            print("Exception occured when running exiftool in 'tag.py' with argument:", commandlist)
            exit(1)



if __name__ == '__main__':

    NC = len(sys.argv)
    if NC != 4:
        print("Wrong number of arguments")
        exit(1)
    flag     = sys.argv[1]
    filename = sys.argv[2]
    newdata  = sys.argv[3]

    if flag not in ["-a", "-o"]:
        print("flag " + flag + "not recognized")
        exit(1)

    VERBOSE = True

    tt = rw_tags(filename)
    tt.read_tags(VERBOSE) # Check which tags already exist in the file
    newt = [word for word in newdata.split(',')]

    if flag == "-o":
        tt.overwrite_tags(newt, VERBOSE)
    elif flag == "-a":
        tt.append_tags(newt, VERBOSE)

    # print(tt.tag_list)
