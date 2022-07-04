from numpy import pad, place
import requests
from bs4 import BeautifulSoup # for making requests to the google search engine

from tkinter import * # for gui

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

    def placeGUI(self): # create the insets using padx and pady, and place the objects of the gui
        self.welcome_label.grid(row=0, column=0, pady=100)

    def initializeGUI(self): # for setting up the gui
        # create a text box for user to input data
        font = 'Arial 12'
        self.text = Text(self.window, width=20, height=1, font=font, state=NORMAL)
        
        # create the welcome label
        font = 'Arial 16 bold'
        self.welcome_label = Label(self.window, text='What would you like to shop for?', font=font, justify=CENTER)

        # create the submit button
        self.submit = Button(text='Submit', command=self.submit)

        # create the quit button
        self.quit = Button(text='Quit', command=self.quit)

        # create the display info
        font = 'Arial 14 bold'
        self.display = Label(font=font)

    
    def quit(self):
        print('exiting with code 5')
        exit(5)

    def submit(self):
        pass

def placeGUI(event): # this is how to configure placegui when resizing the window
    print("Hello")

def main():
    # make the general window and setup the gui
    window = Tk()
    window.title('Modern Shopper')
    window.configure(width=800, height=800)
    window.configure(background='lightgray')
    obj = Shopper(window)
    obj.initializeGUI()
    obj.placeGUI()
    window.bind("<Configure>", placeGUI)
    window.mainloop()

if __name__ == '__main__':
    main()