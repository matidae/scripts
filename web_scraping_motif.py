import sys
import time
from Bio import SeqIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_out(text, name):
        line = text.split()[12:-2]
        if not line:
            print name + "\t" + "No motif found." 
        else:
            for i in xrange(0, len(line), 5):
                print "\t".join([name] + line[i:i+5])

def main(driver):
    for i in pep:
        elem = driver.find_element_by_id('txtSeq')
        elem.send_keys(str(i.seq))
        driver.execute_script("funShow();");
        response = driver.find_element_by_id('tdResult')
        elem.clear()
        time.sleep(3)
        parse_out(response.text, i.id)

if __name__ == "__main__":
    pep = SeqIO.parse(sys.argv[1], "fasta")
	url = sys.argv[2]
    driver = webdriver.Chrome("~/chromedriver")
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtSeq")))
        main(driver)
    except:
        print sys.exc_info()[0]
        sys.exit()
