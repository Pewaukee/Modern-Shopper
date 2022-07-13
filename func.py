from selenium import webdriver # for accessing and searching amazon's database of items
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # for implicitly waiting
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class Driver:
    def __init__(self) -> None:
        # gets rid of 'Failed to read descriptor from node connection: A device attached to the system is not functioning'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options) # shortcut because chrome driver on system path
        self.item_class_name = None

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
        def check_contains(i:int, j:int):
            # convert to string using text just to be safe and sure it will be deleted
            if items[i][j].text.__contains__('Did you mean'):
                del items[i][j]
        check_contains(0, 1) 
        check_contains(1, 1)
        check_contains(0, 0)
        check_contains(1, 0)
    
    def test(self, text:str):
        item = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))
        unique_class_name = WebDriverWait(item,3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-size-medium.a-color-base.a-text-normal')))
        print(unique_class_name.get_attribute('class'))
        #TODO use this template to find the correct items all in one place

    def get_items(self, text:str):
        
        
        # get the first 10 items on the screen and print the text of these items using a loop
        # the class_names in the websites are acutally mulitple class names when they are combined by spaces
        # all_of finds both of the lists with the corresponding id and class name
        search_items = WebDriverWait(self.driver,5).until(EC.all_of(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#search .a-size-base-plus.a-color-base.a-text-normal')),
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#search .a-size-medium.a-color-base.a-text-normal'))))
        print(type(search_items[0][0]))
        
        self.check_misspell(search_items)
        
        if len(search_items[0]) > len(search_items[1]):
            items = search_items[0][:10]
            self.item_class_name = 'a-size-base-plus a-color-base a-text-normal'
        else:
            items = search_items[1][:10]
            self.item_class_name = 'a-size-medium a-color-base a-text-normal'
        #TODO perhaps call by link first, since link is the higher tier than the normal class
        for elem in items:
            print(elem.get_attribute('href'))

        links = WebDriverWait(self.driver,5).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')))[:20:2]
        
        self.print_to_console(items)

        self.add_to_file(items, links, text)

        self.driver.close()
    
    def print_to_console(self, items:list):
        for item in items:
            print(item.text)
        print()
    
    def add_to_file(self, items:list, links:list, text:str) -> None:
        with open('file.txt', 'a') as f:
            f.write(f'{text.capitalize()}:\n\n') # put the search item at the top
            for i in range(10):
                f.write(items[i].text + '\n')
                f.write(links[i].get_attribute('href') + '\n\n')
            f.write('-'*30 + '\n\n')


def find(text:str) -> None:
    driver = Driver()
    driver.set_link('https://amazon.com')
    driver.search(text)
    #driver.get_items(text)
    driver.test(text)
