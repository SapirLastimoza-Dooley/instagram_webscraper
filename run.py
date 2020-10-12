from selenium import webdriver
from time import sleep
from credentials import pw
from selenium.webdriver import ActionChains
from keyWords import keywords
import re


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        SLEEP_TIME = 5
        print("Page Loaded")
        sleep(SLEEP_TIME)

        # Enter username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        print("Username Entered")
        sleep(SLEEP_TIME)

        # Enter password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        print("Password Entered")
        sleep(SLEEP_TIME)

        # Submit
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        print("Credentials Submitted")
        sleep(SLEEP_TIME)

        # Skip pop-ups
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(SLEEP_TIME)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        print("Pop-Ups Skipped")
        sleep(SLEEP_TIME)

    def main(self):
        SLEEP_TIME = 6
        counter = 0
        numPosts = 5

        myBot.findPeople()
        sleep(SLEEP_TIME)
        myBot.clickFirstPost()
        sleep(SLEEP_TIME)

        while counter < numPosts:
            sleep(SLEEP_TIME)
            caption = myBot.saveCaption()
            check = myBot.checkCaption(caption, keywords)

            if check == False:
                myBot.likePost()
                myBot.savePost
                print(f"Post {counter + 1} liked and saved.")
                sleep(SLEEP_TIME)

            myBot.nextPic()

    def findPeople(self):
        discoverButton = self.driver.find_element_by_xpath('//a[@href="/explore/"]')
        discoverButton.click()
        print("Discover Opened")

    def clickFirstPost(self):
        firstPost = self.driver.find_element_by_class_name('eLAPa')
        firstPost.click()
        print("First Post Opened")
                
    def saveCaption(self):
        tempString = ""
        caption = self.driver.find_element_by_class_name("C4VMK").text
        tempString += caption
        print("Caption Saved")
        return tempString

    def checkCaption(self, caption, keywords):
        res = [ele for ele in  keywords if(ele in caption)]
        print("Caption Checked")
        return bool(res)

    def likePost(self):
        likeButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')
        likeButton.click()

    def savePost(self):
        saveButton = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[3]/div/div/button')
        saveButton.click()

    def nextPic(self):
        nex = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]")  
        nex.click() 


        # write caption to file
#        with open("text_file.txt", "w", encoding='utf-8') as f:
#            for item in finalList:
#                f.write("%s\n" % item)

myBot = InstaBot("sapirdooley", pw)
myBot.main()