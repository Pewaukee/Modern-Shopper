from selenium import webdriver # for accessing and searching amazon's database of items
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # for implicitly waiting
from selenium.webdriver.support import expected_conditions as EC

class Driver:
    def __init__(self) -> None:
        '''
        create a new Driver object with a
        selenium based webdriver object using
        the chrome driver, also define the session
        id variable to be updated later when 
        wanting to write to a file
        '''
        # gets rid of 'Failed to read descriptor from node connection: A device attached to the system is not functioning'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options) # shortcut because chrome driver on system path
        self.session_id = 0

    def set_link(self, link:str) -> None:
        # sets the link of the webdriver, and updates the screen
        self.driver.get(link)
        self.driver.maximize_window()

    def search(self, text:str) -> None:
        '''purpose
        when on amazon.com, we want to 
        search for the item that the user entered
        in order to do so, we must find the html element
        for the search text box and the search button

        however, there are 2 versions of the website, 
        which is very weird, so had to use try except 
        blocks in order to understand which website I am on

        so set a text box and a search button variable, and
        if the first check returns an error, then the next version
        of the website will be checked and will pass

        finally call the next function in sequence, get_items()
        '''
        
        # either visibility_of_element_located or presence_of_element_located works
        # put an implicit wait for 3 seconds to find the text box, then send self.text to the search box
        try:
            amazon_text_box = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox')))
        except TimeoutException as e:
            amazon_text_box = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.ID, 'nav-bb-search'))) 
        amazon_text_box.send_keys(text)

        # find the button and click it after the text has been inserted 
        try:
            search_button = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.ID, 'nav-search-submit-button')))
        except TimeoutException as e:
            search_button = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav-bb-button')))
        search_button.click()

        self.get_items(text)

    def get_items(self, text:str):
        '''purpose
        get the first 10 items that are of the main
        size and not some pop up small item or other weird elements

        using the clicked button and now navigated to the results 
        tab of the corresponding search, web scrape the top 10 items, no
        matter if they are sponsored or otherwise,
        this was done using an implicit wait of 3 seconds, and using a
        css selector was the best way, to search for the subset of id=search
        and all of the items that matched the corresponding class name 
        of all the main products

        finally call the other functions which print to console and file
        '''
        
        # css selector: trying to find the class name of all combined needs '.' between the class names and '.' at the start
        search_items = WebDriverWait(self.driver,3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#search .a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
        
        # the prices of each item would show up in the previous list query, so remove them
        items = list()
        for i in range(len(search_items)):
            if len(items) == 10: break
            # searches for the keyboard style where the items were placed one on top of each other
            try:
                element = search_items[i].find_element(By.CSS_SELECTOR, '.a-size-medium') # this finds both items i think
                if element.text != "": items.append(search_items[i])
                continue
            except NoSuchElementException as e:
                pass
            try:
                element = search_items[i].find_element(By.CSS_SELECTOR, '.a-size-base-plus')
                if element.text != "": items.append(search_items[i])
                continue
            except NoSuchElementException as e: # this will happen if it fits in neither item list, vertically or horizontally spaced items
                pass # aka if it is a price       
        
        self.print_to_console(items)

        self.add_to_file(items, text)
    
    def print_to_console(self, items:list) -> None:
        # prints the found items from get_items() to the console
        for i in range(len(items)):
            print(i+1, items[i].text)
        print()
    
    def add_to_file(self, items:list, text:str) -> None:
        # using the created session id, add the product name with it's link to the file
        with open(f'file{self.session_id}.txt', 'a', encoding='utf-8') as f: # encoding helps to remove special characters that may cause an error
            f.write(f'{text.capitalize()}:\n\n') # put the search item at the top
            for i in range(10):
                f.write(f'{i+1}. {items[i].text} + \n') # product name
                f.write(items[i].get_attribute('href') + '\n\n') # hyperlink to product
            f.write('-'*50 + '\n\n') # to seperate items

    def find_session_id(self) -> None:
        # using a infinite loop, find out what is the next file name is, file0.txt -> file1.txt -> file2.txt -> ...
        try:
            while True:
                with open(f'file{self.session_id}.txt', 'r') as f:
                    self.session_id+=1
        except FileNotFoundError:
            return

