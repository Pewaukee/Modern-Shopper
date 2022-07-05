from numpy import pad, place
import requests
from bs4 import BeautifulSoup # for making requests to the google search engine

from tkinter import * # for gui

from selenium import webdriver # for accessing and searching amazon's database of items
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException

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
        
        driver = webdriver.Chrome('C:/Users/kvsha/Downloads/chromedriver_win32/chromedriver.exe')
        driver.get('https://amazon.com')
        
        amazon_text_box = driver.find_elements(By.HREF, '/Amazon-Video/b/?ie=UTF8&amp;node=2858778011&amp;ref_=nav_cs_prime_video')
        print(amazon_text_box.text)

        #TODO find out how to extract the proper data with find_element of the proper text box

        with open('file.txt', 'w') as f:
            f.writelines(amazon_text_box.text)
        #id_box = driver.find_element('issprefix') # this is accessing the search box
        #id_box.send_keys(text) # this is putting in the aforementioned text box

        #search_button = driver.find_element('nav-search-submit-button') # this finds the search button
        #search_button.click() # click the button to get to the next page after searching


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