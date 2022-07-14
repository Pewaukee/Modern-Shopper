from selenium import webdriver # for accessing and searching amazon's database of items
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # for implicitly waiting
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time

class Driver:
    def __init__(self) -> None:
        # gets rid of 'Failed to read descriptor from node connection: A device attached to the system is not functioning'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options) # shortcut because chrome driver on system path
        self.session_id = 0

    def set_link(self, link:str) -> None:
        self.driver.get(link)
        self.driver.maximize_window()

    def search(self, text:str) -> None:
        # either visibility_of_element_located or presence_of_element_located works
        # put an implicit wait for 5 seconds to find the text box, then send self.text to the search box

        # use try except for the other variation of the website
        try:
            amazon_text_box = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox')))
            amazon_text_box.send_keys(text)
        except TimeoutException as e:
            amazon_text_box = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.ID, 'nav-bb-search')))
            amazon_text_box.send_keys(text)

        # find the button and click it after the text has been inserted 
        try:
            search_button = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.ID, 'nav-search-submit-button')))
            search_button.click() # click the button
        except TimeoutException as e: # required for the other version of the website
            search_button = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav-bb-button')))
            search_button.click()

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
    
    

    def get_items(self, text:str):
        
        
        # get the first 10 items on the screen and print the text of these items using a loop
        # the class_names in the websites are acutally mulitple class names when they are combined by spaces
        # all_of finds both of the lists with the corresponding id and class name
        search_items = WebDriverWait(self.driver,3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#search .a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
        # init 2 lists, one for the objects that are stored right and left next to each other, and items stored vertically on top of each other
        # by css style (vertically = .a-size-medium.a-color-base.a-text-normal, horizontally = .a-size-base-plus.a-color-base.a-text-normal)
        
        list1 = list()
        for i in range(len(search_items)):
            if len(list1) == 10: break
            # searches for the keyboard style where the items were placed one on top of each other
            try:
                element = search_items[i].find_element(By.CSS_SELECTOR, '.a-size-medium') # this finds both items i think
                if element.text != "": list1.append(search_items[i])
                continue
            except NoSuchElementException as e:
                pass
            try:
                element = search_items[i].find_element(By.CSS_SELECTOR, '.a-size-base-plus')
                if element.text != "": list1.append(search_items[i])
                continue
            except NoSuchElementException as e: # this will happen if it fits in neither item list, vertically or horizontally spaced items
                pass # aka if it is a price
        #TODO when searching through the page for results, with different css selectors the lists are the same
        #for i in range(max(len(list1),len(list2))):
            #print(list1[i].text[:20], list2[i].text[:20])
            
        # assign the new list to whichever css style of vertically or horizontally next to each other gave the longest list
        #items = (list1 if len(list1) > len(list2) else list2)[:10]
        #print(len(items))
        
        items = list1
        #TODO since getting by a higher header, this needs to be changed
        #self.check_misspell(items)
        
        self.print_to_console(items)

        self.add_to_file(items, text)

        self.driver.close()
    
    def print_to_console(self, items:list) -> None:
        for i in range(len(items)):
            print(i+1, items[i].text)
        print()
    
    def add_to_file(self, items:list, text:str) -> None:
        with open(f'file{self.session_id}.txt', 'a') as f:
            f.write(f'{text.capitalize()}:\n\n') # put the search item at the top
            for i in range(10):
                f.write(f'{i+1}. {items[i].text} + \n')
                f.write(items[i].get_attribute('href') + '\n\n')
            f.write('-'*30 + '\n\n')

    def find_session_id(self) -> None:
        try:
            while True:
                with open(f'file{self.session_id}.txt', 'r') as f:
                    self.session_id+=1
        except FileNotFoundError:
            return

def find(text:str, driver) -> None:
    driver.set_link('https://amazon.com')
    driver.search(text)
    driver.get_items(text)
