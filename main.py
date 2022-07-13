from numpy import pad, place
import requests
from bs4 import BeautifulSoup # for making requests to the google search engine

from tkinter import * # for gui

import time # for debugging

from func import *




def main() -> None:
    welcome = 'Welcome to modern shopper!'
    print(welcome + '\n')
    exit_str = 'exit'
    while True:
        user_input = input("What would you like to shop for?: ")
        if user_input == exit_str: break
        # call the function to get the items
        find(user_input)
        print("----------------------\nItems added to session file")


    


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

extra code with gui elements

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
        pass
    
    def placeGUI(event, obj, window): # this is how to configure placegui when resizing the window
    #print("placeGUI function has been run")
    obj.placeGUI()
    #print(f'width = {window.winfo_width()}, height = {window.winfo_height()}')

main lines for creating window

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

extra html i think mostly xpaths

# span[class='a-size-medium']

        # tea arrangement: a-size-base-plus a-color-base a-text-normal
        # keyboard arrangment: a-size-medium a-color-base a-text-normal

        #/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[1]/h2/a/span
        #/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/div/div/div/div/div/div[2]/div[1]/h2/a/span

        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div[1]/h2/a/span
        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[4]/div/div/div/div/div/div/div[2]/div[1]/h2/a/span
        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[7]/div/div/div/div/div[2]/div[1]/h2/a/span
        #//*[@id="anonCarousel3"]/ol/li[1]/div/div/div/div/div/div/div[2]/div[1]/h2/a/span

        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span
        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a/span

        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/div/div/div/div[3]/div[1]/h2/a/span
        #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/h2/a/span
        
extra code for checking which class the desired element was that was selected

        
        if len(search_items[0]) > len(search_items[1]):
            items = search_items[0][:10]
            self.item_class_name = 'a-size-base-plus a-color-base a-text-normal'
        else:
            items = search_items[1][:10]
            self.item_class_name = 'a-size-medium a-color-base a-text-normal'

code for getting the links, which worked a little
didn't get the correct links, because it would get all the links, which sometimes
wouldn't be the item it was matching to

didnt need to get all the links, needed to scrape the bigger tier element and then find
it's attributes



'''