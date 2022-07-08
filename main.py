from numpy import pad, place
import requests
from bs4 import BeautifulSoup # for making requests to the google search engine

from tkinter import * # for gui

import time # for debugging

from selenium import webdriver # for accessing and searching amazon's database of items
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.support.ui import WebDriverWait # for implicitly waiting
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from PIL import ImageTk, Image # for inserting an image as a label

class Shopper(object):
    def __init__(self, window) -> None:
        super().__init__()
        self.window = window
        self.text = None
        self.welcome_label = None
        self.submit = None
        self.quit = None
        self.display = None
        # come back to put in the table, google that 

    def placeGUI(self): 
        # relative x and y are ratios of screen width and height, and determine how to place label
        # anchor is where the item is justified, like in text

        # place the welcome relatively at the top
        self.welcome_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        # place the text box under the welcome label
        self.text.place(relx=0.5, rely=0.25, anchor=CENTER)
        # place the submit button under the text box
        self.submit.place(relx=0.5, rely=0.4, anchor=CENTER)
        # place the quit button in the top left
        self.quit.place(relx=0, rely=0, anchor=NW)
        # place the display label under the submit button
        self.display.place(relx=0.5, rely=0.6, anchor=CENTER)

    def initializeGUI(self): # for setting up the gui
        # create a text box for user to input data
        font = 'Arial 12'
        self.text = Text(self.window, width=20, height=1, font=font, state=NORMAL)
        
        # create the welcome label
        font = 'Arial 16 bold'
        self.welcome_label = Label(self.window, text='What would you like to shop for?', font=font, bg='white')

        # create the submit button
        self.submit = Button(text='Submit', command=self.submitFunc)

        # create the quit button
        self.quit = Button(text='Quit', command=self.quitFunc)

        # create the display info
        font = 'Arial 14 bold'
        self.display = Label(font=font, bg='white')

    
    def quitFunc(self):
        print('exiting with code 5')
        exit(5)

    def submitFunc(self): 
        text = self.text.get('1.0', 'end-1c')
        
        
        driver = webdriver.Chrome() # shortcut because chrome driver on system path
        driver.get('https://amazon.com')

        driver.maximize_window() # For maximizing window

        # either visibility_of_element_located or presence_of_element_located works
        # put an implicit wait for 20 seconds to find the text box, then send self.text to the search box
        amazon_text_box = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox')))
        amazon_text_box.send_keys(text)

        # find the button and click it after the text has been inserted 
        search_button = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID, 'nav-search-submit-button')))
        search_button.click() # click the button


        driver.close()
    
        # get all the text in a list
        #item_information = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'a-size-base-plus a-color-base a-text-normal')))
        #item_information = item_information[:10] # get the first 10 elements
        #print(len(item_information))

def placeGUI(event, obj, window): # this is how to configure placegui when resizing the window
    #print("placeGUI function has been run")
    obj.placeGUI()
    #print(f'width = {window.winfo_width()}, height = {window.winfo_height()}')

def main():
    # make the general window and setup the gui
    window = Tk()
    window.title('Modern Shopper')
    window.configure(width=800, height=800)
    window.configure(background='white')
    #TODO update the min size after adding a table
    window.minsize(488, 246) # minimum size of window, checked by testing and figuring out what was good
    obj = Shopper(window)
    obj.initializeGUI()
    obj.placeGUI()
    window.bind("<Configure>", lambda event: placeGUI(event, obj, window))
    window.mainloop()

if __name__ == '__main__':
    main()


''' 
additional notes

fix selenium.common.exceptions.WebDriverException: Message: unknown error: cannot determine loading status
 fix selenium.common.exceptions.WebDriverException: Message: unknown error: unexpected command response

these two errors kept popping up at random, sometimes not allowing the proper
exiting of the selenium controled google chrome window
this was a random error, which means i could put in the same information
and basically everying, even to the input being the same
the actual error was in the chromedriver version, and converting to a higher version and 
therefore a chrome beta was not working, so I had to use chromium to download an earlier version
of chrome and use the corresponding chromedriver v.102 to make it work    
'''