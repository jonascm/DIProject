from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# ISSUES: 

with open("noaa_metdata_buoyprops.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line.rstrip('\n'))

driver = webdriver.Firefox()
counter = 0
failures = []
for els in array:
    counter +=1
    driver.get(els)
    
    filetomake=els[-6:-1] + ".txt"
    filetomake=filetomake.rstrip('=')
    filetomake=filetomake.rstrip(' ')
    
    try:
        elem1 = driver.find_element_by_xpath("//*[@id='stn_metadata']")
    except NoSuchElementException:
        counter -= 1
        failures.append(filetomake)
        print("FAILED: " + filetomake)
        continue

    with open(filetomake, "w") as text_file:
        text_file.write((elem1.text).encode("utf-8"))
    print("#" + str(counter) + " --> " + filetomake)

driver.close()

with open("failures.txt", "w") as tf:
    tf.write(failures)
