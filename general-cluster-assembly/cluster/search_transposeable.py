#!/usr/bin/python

import sys 
""" what : this is a post processing script for the outputs of reading3_1.cpp that searches for potential 
           breakpoints more accurately leaving only the recurrences and some other ones.

    input : python2.7 search_transposeable.py <name_of_SRR/RAL-name> (ex. ZI213)
    output : summary_<name>-breakpoints , summary_<name>-results 

    sidenote: it needs recurrence.csv, knownInversion.txt, notKnownInversion.txt, dmelMapTable.txt, TE_sites.txt

""" 
# regular entry but mainly for TE 
class location:
    trans_size = 0 # not sure if list or class has a built in size check?  
    def __init__(self, chrom_ref, position1, position2):
        self.chrom_ref = chrom_ref
        self.position1 = position1 
        self.position2 = position2 
        location.trans_size += 1 

    def getposition1(self): 
        return self.position1 
    def getposition2(self): 
        return self.position2 
    def getchrom_ref(self):
        return self.chrom_ref 
    def getSize(self):
        return self.trans_size 
    def displayInfo(self): 
        print "this is the current size of this particlar class -chrom_ref " + self.chrom_ref + " -position1 " + str(self.position1) + " -position2 " + str(self.position2) + " " 

# this is for the breakpoint that comes in
class b_location: 
    def __init__(self, index, samflag, chrom_ref, low_position1, low_position2, high_position1, high_position2, size): 
        self.index = index 
        self.samflag = samflag 
        self.chrom_ref = chrom_ref 
        self.low_position1 = low_position1
        self.low_position2 = low_position2
        self.high_position1 = high_position1 
        self.high_position2 = high_position2 
        self.size = size 
        self.status = False
    
    # class functions 
    def getsamflag(self): 
        return self.samflag
    def getlowposition1(self): 
        return self.low_position1
    def getlowposition2(self): 
        return self.low_position2
    def gethighposition1(self): 
        return self.high_position1
    def gethighposition2(self):
        return self.high_position2
    def getchrom_ref(self): 
        return self.chrom_ref 
    def getindex(self): 
        return self.index 
    def getSize(self):
        return self.size
    def convertStatus(self): 
        self.status = True 
    def getStatus(self): 
        return self.status
    def displayInfo(self):
        print " this is the breakpoint here " + str(self.samflag) + " " + self.chrom_ref + " " + str(self.low_position1) + " " + str(self.low_position2) + " " + str(self.high_position1) + " " + str(self.high_position2) 

name = str(sys.argv).split(" ") 
summaryBreakpoints = "summary-"+name[1].lstrip("'").rstrip("']")+"-breakpoints" # this is getting the name of the file being written into with actual breakpoints that pass the transponseable element test 
summaryResults = "summary-"+name[1].lstrip("'").rstrip("']")+"-result" 
writeBreakpoints = open(summaryBreakpoints, "w")  
"""
# check out the tranposeable elements here and store them into a list or whatever that is easier to do so 
# then read in everything of the entire line - class - then compare only the first and second locations 
#                   ----> check to see if it is within the range tho.  
""" 
trans_objects = []  # holds TE elements in class 
break_objects = []  # holds cluster in class 
# getting the value of the TE here 
with open("TE_sites.txt", "r") as f: 
    for line in f: 
        content = line.split() 
        decoy = location( content[0], int(content[3]), int(content[4]) )
        # print "this is the current counter after each line " + str(decoy.getSize())
        trans_objects.append(decoy)   


# getting the values of the clusters here from summary_*.txt  
break_store = [] # this will hold a list of classes 
check_sum = 0 
# opening the file of the summary breakpoints of both low positions and high positions 
with open(summaryResults, "r") as f: 
    for line in f: 
        if line in ['\n', '\r\n']:
            break_store.append(break_objects)
            #del break_objects[:] # deleting everything in break_objects. 
            break_objects = [] # recreating another list or emptying the current one
            check_sum += 1 
        else: 
            content = line.split() 
            # b_location( chrom , samflag , lowpos1, lowpos2, highpos1, highpos2, sizeof cluster)
            decoy = b_location( int(content[0]), int(content[1]), content[2], int(content[3]), int(content[4]), int(content[5]), int(content[6]), int(content[7]))
            break_objects.append(decoy) 
            # decoy.displayInfo() 

# if there's only one cluster so it will never go through the other one.
if check_sum == 0 : 
    break_store.append(break_objects)

"""
reading the Dmel table to set up for the comparsion 
"""
dmel_holder = []
with open("DmelMapTable.txt", 'r') as f: 
    for i in f: 
        temp_dmel_store = []
        content = [x.strip() for x in i.split(',')]
        """ this gets the chrom_region and positions together"""
        chrom_info = [x.strip() for x in content[2].split(":")]
        # print chrom_info
        """ this will now separate the positiosn from .. """
        if ( len(chrom_info) == 2):  
            pos_info = [x for x in chrom_info[1].split("..")]
            temp_dmel_store.append( chrom_info[0] ) 
            temp_dmel_store.append( (pos_info[0]) ) 
            temp_dmel_store.append( pos_info[1] ) 
            dmel_holder.append(temp_dmel_store) 
            # print temp_dmel_store
        else: 
            continue 

# getting the recurrence reads here for comparsion
recurrenceObjects = [] 
# getting the recurrence reads here . 
with open("recurrence.csv", 'r') as recurFile: 
    for entry in recurFile:
        content = [x.strip() for x in entry.split(",")]
        decoy = location(content[0], int(content[1]), int(content[2]))
        recurrenceObjects.append(decoy) 

# this is from russ's and University of South Carolina's papers 
# this is mainly the known inversion discovered by Russ. 
knownInversion = [] 
with open("knownInversion.txt", 'r') as f: 
    for line in f: 
        content = [x.strip() for x in line.split(" ")]
        decoy = location(content[1], int(content[4]), int(content[5]))
        knownInversion.append(decoy) 

# this is "inversion regions" not discovered by Russ.
notKnownInversion = [] 
with open("notKnownInversion.txt", 'r') as f: 
    for line in f: 
        content = [x.strip() for x in line.split(" ")]
        decoy = location(content[1], int(content[2]), int(content[3]))
        notKnownInversion.append(decoy) 

"""
# searches and compare the TE element with the cluster and see if it is close
# if one part matches then count, if at least like 50 - 80 % matches then add it to the list
"""
nope_number = [] # clusters that did not pass the TE elements 
yes_number = [] # clusters that did pass the TE elements 
newBreakStore = [] # being lazy - checking dmel with yes_number and writing to newBreakStore  
newBadBreaks = []
print "bob" # rand cout statement 

counter = 0 # this is to keep track of the number of reads within TE at least 80% 
checklist = False 
for index, cur_list in enumerate(break_store): # getting each individual list
    in_transrange = False
    for t_index, entry in enumerate(cur_list): # iterating individually through chosen list
        in_transrange = False 
        for trans in trans_objects: # iterating through TE now 
            if entry.getchrom_ref() == trans.getchrom_ref(): # making sure the location is the same
            # somehow set_5_8 goes through. 
                if trans.getposition1() <= entry.getlowposition1() <= trans.getposition2() or trans.getposition1() <= entry.gethighposition1() <= trans.getposition2()\
                 or trans.getposition1() <= entry.getlowposition2() <= trans.getposition2() or trans.getposition1() <= entry.gethighposition2() <= trans.getposition2():
                    in_transrange = True
                    break
        if (in_transrange == True):
            nope_number.append(cur_list)
            break 
    if in_transrange == False:
        yes_number.append(cur_list)

# compare dmel table to potential breakpoints
temp_dmel_holder = dmel_holder[:]
for t_index,j in enumerate(yes_number): 
    for count, i in enumerate(j):
        # print i.displayInfo()
        for index, dmel_line in enumerate(dmel_holder): 
            if (str(dmel_line[0]) == i.getchrom_ref()):
                if (int(dmel_line[1]) <= i.getlowposition1() <= int(dmel_line[2]) or int(dmel_line[1]) <= i.gethighposition1() <= int(dmel_line[2])):
                    # then check for the other end to see if they are around the same 
                    # temp_dmel_holder = dmel_holder[index:]
                    for temp_line in temp_dmel_holder:
                        if (str(temp_line[0]) == i.getchrom_ref()):
                            if (int(temp_line[1]) <= i.getlowposition2() <= int(temp_line[2]) or int(temp_line[1]) <= i.gethighposition2() <= int(temp_line[2])):
                            # if (i.getlowposition1() <= int(dmel_line[1]) <= i.gethighposition1() or i.getlowposition2() <= int(dmel_line[1]) <= i.gethighposition2()):
                                i.convertStatus()
                                writeBreakpoints.write(str(i.getindex()) + "\t" + str(i.getsamflag()) + "\t" + i.getchrom_ref() + "\t" + str(i.getlowposition1()) + "\t" + str(i.getlowposition2()) + "\t" + str(i.gethighposition1()) + "\t" + str(i.gethighposition2())+ "\t" + str(i.getSize()) +"\t"+ str(i.getStatus()) + '\n' ) 
                                break # done with this position if everything matches 
                    if i.getStatus() == False: 
                            writeBreakpoints.write(str(i.getindex()) + "\t" + str(i.getsamflag()) + "\t" + i.getchrom_ref() + "\t" + str(i.getlowposition1()) + "\t" + str(i.getlowposition2()) + "\t" + str(i.gethighposition1()) + "\t" + str(i.gethighposition2())+ "\t" + str(i.getSize()) + "\t"+ str(i.getStatus()) + '\n' ) 
                            break

# i can just read the new file and create the cluster based on that. 
# open the "summary-<SRR>-breakpoints" to get the needed clusters to print out in <SRR>-breakpoints
writeBreakpoints.close() 
with open(summaryBreakpoints, 'r') as f:  
    for i in f: 
        badValue = False
        alrInversion = False 
        newBreakEntry = [] 
        content = [x.strip() for x in i.split("\t")]
        decoy = b_location( int(content[0]), int(content[1]), content[2], int(content[3]), int(content[4]), int(content[5]), int(content[6]), int(content[7]))
        for entry in recurrenceObjects: 
            if entry.getchrom_ref() == decoy.getchrom_ref():
                
                if entry.getposition1()-15000 < decoy.getlowposition1() < entry.getposition2()+15000 or \
                entry.getposition1()-15000 < decoy.gethighposition1() < entry.getposition2()+15000: 

                    if entry.getposition2()-15000 < decoy.getlowposition2() < entry.getposition2()+15000 or\
                    entry.getposition2()-15000 < decoy.gethighposition2() < entry.getposition2()+150000: 
                        # print("recurrence check -> {0} {1} {2} {3}".format(decoy.getlowposition1(), decoy.getlowposition2(), decoy.gethighposition1(), decoy.gethighposition2()))
                        badValue = True
                        break 
        if(badValue == False): 
            # print("not recurrence -> {0} {1} {2} {3}".format(decoy.getlowposition1(), decoy.getlowposition2(), decoy.gethighposition1(), decoy.gethighposition2()))
            # checking the known inversion points here
            for known in knownInversion: 
                if known.getchrom_ref() == decoy.getchrom_ref():
                    if known.getposition1()-1000 < decoy.getlowposition1() <known.getposition1()+1000 or \
                    known.getposition1()-1000 < decoy.gethighposition1() < known.getposition1()+1000: 
                        if known.getposition2()-1000 < decoy.getlowposition2() < known.getposition2()+1000 or \
                        known.getposition2()-1000 < decoy.gethighposition2() < known.getposition2()+1000: 
                            alrInversion = True
                            break

            if alrInversion == False: 
                # checking to see if the Inversion are known or not.
                for notKnown in notKnownInversion: 
                    if notKnown.getchrom_ref() == decoy.getchrom_ref(): 
                        if notKnown.getposition1()-1000 < decoy.getlowposition1() <notKnown.getposition1()+1000 or \
                        notKnown.getposition1()-1000 < decoy.gethighposition1() < notKnown.getposition1()+1000: 
                            if notKnown.getposition2()-1000 < decoy.getlowposition2() < notKnown.getposition2()+1000 or \
                            notKnown.getposition2()-1000 < decoy.gethighposition2() < notKnown.getposition2()+1000: 
                                decoy.convertKnown() 
                                break 
                newBreakEntry.append(decoy) 
                newBreakStore.append(newBreakEntry)

with open(summaryBreakpoints, 'w') as f: 
    for i in newBreakStore: 
        for j in i: 
            # j.displayInfo()
            f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format( j.getsamflag(), j.getchrom_ref(), j.getlowposition1(), j.getlowposition2(), j.gethighposition1(), j.gethighposition2(), j.getKnown() ))
""" writing a file of the actual reads based on the exisiting summary clusters
this will also check for the Dmel or the theoretical breakpoints here as well 
"""
goodReadFile = "good_"+name[1].lstrip("'").rstrip("']")+"-result"
detailedBreakpoints = name[1].lstrip("'").rstrip("']")+"-breakpoints"
writeDetailedBreakpoints = open(detailedBreakpoints, 'w')

for i in newBreakStore: 
    for j in i: 
        j.displayInfo() 

# this is opening good_<SRR>-results which is has the full info on the clusters
# why is it printing 10 of each element in a cluster? 
with open(goodReadFile) as f:
    for line in f:
        content = [x.strip() for x in line.split("\t")]
        if len(content) != 7: # to avoid getting an error for index out of range due to the empty line separating them? 
            continue 
        #content = line.split("\t")
        for i in newBreakStore: 
            for j in i: 
                if content[0] == str( j.getindex() ): 
                    # start writeDetailedBreakpoints it 
                    writeDetailedBreakpoints.write(line)
		    # writeDetailedBreakpoints.write("\n") 
                    break  
                    
                
