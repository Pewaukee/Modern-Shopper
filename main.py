from func import Driver # only need the class name so we can make the new object

def main() -> None:
    print('Welcome to modern shopper!\n')

    # make a new driver class object to run the func.py functions from
    driver = Driver()
    driver.find_session_id()

    while True:
        '''purpose
        this while true loop reads input from the user, 
        and uses that data to search the amazon database
        using selenium and the functions in func.py,
        then returns by printing and adding to a file
        the results of the execution
        '''
        user_input = input("What would you like to shop for?: ").strip()
        if user_input == 'exit': break
        print('Fetching data...\n')

        # call the function to get the items
        driver.set_link('https://amazon.com')
        driver.search(user_input)

        print("Items added to session file\n")
        
    driver.driver.close() # use the attribute of driver to close, since the attribute is defined as driver
    


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

extra code that was used to test to find a bigger type of html directory where both the link and text were stored

def test(self, text:str):
        item = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
        unique_class_name = item.find_element(By.CSS_SELECTOR, '.a-size-medium.a-color-base.a-text-normal')
        #WebDriverWait(item,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-size-medium.a-color-base.a-text-normal')))
        print(unique_class_name.get_attribute('class'))
        # use this template to find the correct items all in one place

extra code for misspelling an item to be shopped for

def check_misspell(self, items:list) -> list:
        # if there is a misspell, then we need to delete the first two text boxes of each list
        # start with the second element, then move on to the first element,
        # as to not mess with deletion and accessing the wrong element
        def check_contains(i:int):
            # convert to string using text just to be safe and sure it will be deleted
            if items[i].text.__contains__('Did you mean'):
                del items[i]
        check_contains(1) 
        check_contains(0)

'''