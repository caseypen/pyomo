
import os, glob

# build obj gradient and constraint Jacobian
# from a gjh file written by the ASL gjh 'solver'
# gjh solver may be called using pyomo, use keepfiles = True to write the file

# Use symbolic_solver_labels=True option in pyomo allong with keepfiles = True
# to write the .row file and .col file to get variable mappings


def readgjh():
    flag = 0

    for file in glob.glob("*.gjh"):

        flag = flag+1
        if flag > 1:
            print("**** WARNING **** More than one gjh file in current directory")

        f = open(file,"r")

        data = "dummy_str"
        while data != "param g :=\n":
            data = f.readline()

        data = f.readline()
        g = []
        while data[0] != ';':
            # gradient entry (sparse)
            entry = [int(data.split()[0]) - 1, float(data.split()[1])] # subtract 1 to index from 0
            g.append(entry) # build obj gradient in sparse format
            data = f.readline()


        while data != "param J :=\n":
            data = f.readline()

        data = f.readline()
        J = []
        while data[0] != ';':
            if data[0] == '[':
                # Jacobian row index
                row = int(filter(str.isdigit,data)) - 1  # subtract 1 to index from 0
                data = f.readline()

            entry = [row, int(data.split()[0]) - 1, float(data.split()[1])]  # subtract 1 to index from 0
            J.append(entry) # Jacobian entries, sparse format
            data = f.readline()
        f.close()




    flag = 0
    for file in glob.glob("*.col"):

        flag = flag +1
        if flag > 1:
            print("**** WARNING **** More than one .col file in current directory")

        f = open(file,"r")
        data = f.read()
        varlist = data.split()
        f.close()


    flag = 0
    for file in glob.glob("*.row"):

        flag = flag +1
        if flag > 1:
            print("**** WARNING **** More than one .row file in current directory")

        f = open(file,"r")
        data = f.read()
        conlist = data.split()
        f.close()




    # Cleanup
    tmpfiles = ( glob.glob("tmp*.col") + glob.glob("tmp*.row") + glob.glob("tmp*.sol") +
        glob.glob("tmp*.log") + glob.glob("tmp*.nl") + glob.glob("tmp*.gjh") )
    for file in tmpfiles:
         os.remove(file)



    return g,J,varlist,conlist


