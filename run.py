from selenium import webdriver
from time import sleep
from credentials import pw
from selenium.webdriver import ActionChains
from keyWords import keywords


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        # Enter username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        # Enter password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        # Submit
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        # Skip pop-ups
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)


    # loads full page so that other data can be loaded
    def scrollFullPage(self):
        i = 1
        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            # Stops code from scrolling indefinietly
            if i > 2:
                break
            last_height = new_height
            i += 1
            j = 1
            sleep(2)

        # Scroll to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        sleep(10)

    # opens one caption at a time
    def openCaptions(self):
        i = 0
        while i < 10:
            # find "more" button after captions
            moreButton = self.driver.find_element_by_class_name('sXUSN')

            # scrolls next button into view
            self.driver.execute_script("arguments[0].scrollIntoView();", moreButton)
            sleep(2)

            # scrolls up a bit so that button is clicked 
            self.driver.execute_script("window.scrollBy(0,-150);")
            sleep(2)
            moreButton.click()

            # scrolls down a bit so that next button can be found
            self.driver.execute_script("window.scrollBy(0,250);")
            sleep(2)
            i += 1

    # opens x amount of captions and saves to text file
    def gatherCaptions(self, keywords):
        i = 0
        finalList = []

        while i < 5:

            # find more button and click
            moreButton = self.driver.find_element_by_class_name('sXUSN')
            self.driver.execute_script("arguments[0].scrollIntoView();", moreButton)
            self.driver.execute_script("window.scrollBy(0,-150);")
            moreButton.click()
            sleep(2)

            # find caption text box
            caption = self.driver.find_element_by_class_name("_8Pl3R").text
            res = [ele for ele in keywords if(ele in caption)] 
            if res == True:
                finalList.append(caption)
            res = []
            sleep(5)
            i += 1
            sleep(2)
        
        # write caption to file
        with open("text_file.txt", "w", encoding='utf-8') as f:
            for item in finalList:
                f.write("%s\n" % item)

myBot = InstaBot("tkpaddles95@gmail.com", pw)
#myBot.scrollFullPage()
#myBot.openCaptions()
myBot.gatherCaptions(keywords)