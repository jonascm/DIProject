import os
import glob
#import numpy as np

previousname = ''
counter = 0
for name in sorted(glob.glob("datasets_raw_wave/*.txt")):
    counter += 1
    keyname = name[18:23]
    print("Started: " + keyname + ' (previous was ' + previousname + ')')
    #keyname = keyname.rstrip('=')
    if keyname != previousname:
        if counter == 1:
            # first iteration, just define previous and mydata
            previousname = keyname
            mydata = []
        else:
            # nth iteration: save data and restart the counts
            if (mydata != []):
                with open("datasetsatt1/" + previousname + '_ALL.txt', "w") as tf:
                    tf.write(fsthead)
                    tf.write(scdhead)
                    for lne in mydata:
                        tf.write(lne)
            print("Finished " + previousname + " with " + str(len(mydata)) + " lines")
            previousname = keyname
            mydata = []

    #assume all years for the same buoy have the same header...

    with open(name, "r") as ins:
        # read first line
        fsthead = ins.readline()
        while '  ' in fsthead:
            fsthead = fsthead.replace('  ',' ')
        # find if it has WVHT
        idxwvh = -1
        for i, j in enumerate(fsthead.split(' ')):
            if j == 'WVHT':
                # here's the waveheight!
                idxwvh  = i
                print("In " + keyname + " there's WVHT in pos " + str(i))
        if (idxwvh==-1):
             print("No wave data in " + keyname + ' HEADERS:\n' + fsthead)
             continue
        else:
            scdhead = ins.readline()
            while '  ' in scdhead:
                scdhead = scdhead.replace('  ',' ')
            #then there's a wave header... find if any of the values is not 99, if so, good
            for line in ins:
                # replace multiple spaces for one
                while '  ' in line:
                    line = line.replace('  ',' ')
                # if the wvht is a digit...
                if idxwvh < len(line.split(' ')): 
                    if (line.split(' ')[idxwvh]).replace('.','',1).isdigit():
                        if float(line.split(' ')[idxwvh]) < 90.0:
                            #we have wave and it is a decent value...
                            mydata.append(line)
                            #print("#### " + line.split(' ')[idxwvh] + " less than 99")



# save the last and print the counter to make sure we've explored all files... god
if (mydata != []):
    with open("datasetsatt1/" + previousname + '_ALL.txt', "w") as tf:
        tf.write(fsthead)
        tf.write(scdhead)
        for lne in mydata:
            tf.write(lne)
    print("Finished " + previousname + " with " + str(len(mydata)) + " lines")

print('\n\n Completed ' + str(counter) + ' files!! woohoo')

