import os
import numpy as np

mydata = {}
for root, dirs, files in os.walk("datasets_buoys", topdown=False):
    for name in files:
        #print(name)
        keyname = name.rstrip('.txt')
        keyname = keyname.rstrip('=')
        with open("datasets_buoys/"+name, "r") as ins:
            waterdepthhere = "-1"
            coordhere = []
            for line in ins:
                # here we look at what info we have...
                # dict key: the name (without .txt and =, if any)
                # if the line starts with a number, and has number + N/S + number + E/W + ... then it's coord. Should have 8 elements (4 normal, 4 with other shiz)
                # if the line starts with "Water depth: " then the next value is the depth (in m by default... check it!)
                #print(line)
                
                if line.startswith("Water depth:"):
                    # pos 3 should be metres
                    #print(line.split(' '))
                    if (line.split(' ')[3] == 'm\n'):
                        #grab data!
                        waterdepthhere = float(line.split(' ')[2])
                if (len(line.split(' ')) == 8):
                    if (line.split(' ')[1] == 'N') or (line.split(' ')[1] == 'S'):
                        # it's a win! crop the line and take v N/S v E/W
                        coordhere = line.split(' ')[0:4]

                # update dictionary!
            mydata[keyname]=(coordhere, waterdepthhere)


#print(mydata)
np.save('buoyprops_dictionary.npy', mydata)

# TO LOAD
#read_dictionary = np.load('buoyprops_dictionary.npy').item()
#print(read_dictionary) # displays all

