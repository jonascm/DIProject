import urllib

testfile = urllib.URLopener()

# open file with the links to the datasets
with open("noaa_metdata_allbuoys.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line.rstrip('\n'))

# for each link, create the .txt file in the right folder... let's see if it works!

counter = 0
for els in array:
    counter +=1
    print("#" + str(counter) + " --> "+els[53:58]+'_'+els[59:63]+'.txt')
    testfile.retrieve(els, "datasets_raw_wave/"+els[53:58]+'_'+els[59:63]+'.txt')

#print(counter)

# use other codes to merge them and do operations

