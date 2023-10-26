"""
TEST CASE
____________________

1. Open Chrome 
2. Load the URL: http://www.enlabel.com/
3. Get list of subcategories from each menu
4. Wait for a known element to be present to determine page-load success
5. Print if successful or not
6. Close browser

"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# code to ignore errors, my current google chrome version doesn't exactly match the version for the .exe so I'm getting some harmless errors
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Setup chrome driver
driver = webdriver.Chrome()

# Navigate to the url
driver.get("http://www.enlabel.com/")

# Set the maximum amount of time to wait for the page to load (in seconds)
timeout = 10

# action class that allows us to move to hover/click on web page items
action = ActionChains(driver)

'''
7  # top level headers 
+ 4  # sub - about us 
+ 3  # sub -  platform 
+ 7  # sub -  services 
+ 5  # sub -  compliance 
+ 2  # sub -  resources

= 28 total
'''
# Number of expected Clicks during Test
EXPECTED_NUMBER_OF_PAGES_TO_LOAD = 7 + 4 + 3  + 7  + 5 + 2  

ACTUAL_NUMBER_OF_PAGES_LOADED = 0

# Open a new hover instance over a specified header label
def hoverOverTopLevelHeader(headerName):

    # highest menu label
    webElement = driver.find_element(By.ID, "horizontal-menu")

    # hover on a specified top level header
    headerElement = webElement.find_element(By.LINK_TEXT, headerName)
    action.move_to_element(headerElement).perform()

# verfiy that under the current web element (so as not to have possible confusion for duplicate header labels), the sub header is clickable and loads fine
def validateBodyIsPresent(headerToValidate, subOrTop, currentWebElement):
    # wait for a specific known element in the webpage to be present to determine if page has loaded successfully
    try:

        # find and click on the sub header (under the current web element specifically)
        toClick = currentWebElement.find_element(By.LINK_TEXT, headerToValidate)
        toClick.click()

        element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
        ui.WebDriverWait(driver, timeout).until(element_present)

        print(
            f"{subOrTop} Level Header -- {headerToValidate} -- Page loaded successfully")

        # keep track of total clicks for later verification
        global ACTUAL_NUMBER_OF_PAGES_LOADED
        ACTUAL_NUMBER_OF_PAGES_LOADED += 1

        # generic placeholder for readability --- if the page times out, the test will fail with assert False
        assert(True)

    except TimeoutException:
        print("Timed out waiting for page to load.")
        assert(False)

# for each new instance of a web driver (ie: hoverOverTopLevelHeader()), go to the correct top level header instance
def getMatchingSubLevel(header):

    # open a new hover over the specified header label
    hoverOverTopLevelHeader(header)

    # first find all the expandable class elements
    possibleSubHeaders = driver.find_elements(By.XPATH, ".//li[contains(@class, 'expanded') and contains(@class, 'menu-mlid')]")

    # under the expandable elements
    for subLevel in possibleSubHeaders:
        # find the expandable (ie has sub headers) that matches our top level header
        if header in subLevel.text.split("\n"):
            # return it
            return subLevel


# get all the sub header labels under a specified top level header
def collectSubHeadersUnderCurrentTopLevel(header):

    # get the web driver object according to the header
    subLevel = getMatchingSubLevel(header)

    # init
    subHeaderList = None

    if subLevel != None:
        # if sub headers actually exist under this high level header, then extract the list of names of the sub header labels
        subHeaderList = subLevel.find_element(By.XPATH, ".//ul[starts-with(@class, 'sub-nav') and contains(@class, 'menu-tree-mlid')]").text.split("\n")
    
    return subHeaderList


# validate a sub header list
def finalSubLevelValidation(topLevelHeader, subHeaderList):

    # for each sub header
    for subHeader in subHeaderList:

        # get a new instance so we don't have a stale driver instance
        hoverOverTopLevelHeader(topLevelHeader)

        # find the correct matching sub level (directly under the top level header)
        subLevel = getMatchingSubLevel(topLevelHeader)

        # validate it 
        validateBodyIsPresent(subHeader, "Sub", subLevel)


def iterateOverTopLevelHeaders():

    # start with a clean web element for each top level
    webElement = driver.find_element(By.ID, "horizontal-menu")

    # for each top level header ...
    for header in webElement.text.split("\n"):

        # reopen hover menu for current top level header --- to avoid stale driver instances
        hoverOverTopLevelHeader(header)

        # collect the sub header label texts
        subHeaderList = collectSubHeadersUnderCurrentTopLevel(header)

        if subHeaderList != None:
            # if there are sub headers ...
            print(f"Validating sub headers -- {subHeaderList}")
            # now validate the collected sub headers
            finalSubLevelValidation(header, subHeaderList)

        # and lastly validate this top level header (where we can just create a new driver instance for ease)
        validateBodyIsPresent(header, "Top", driver.find_element(By.ID, "horizontal-menu"))

        # repeat ...


# validate all pages load successfully with no issues
def testHappyPath():

    iterateOverTopLevelHeaders()

    # validate all expected pages are clicked and loaded successfully
    assert (EXPECTED_NUMBER_OF_PAGES_TO_LOAD == ACTUAL_NUMBER_OF_PAGES_LOADED)
    print(
            f"Expected Clicks: {EXPECTED_NUMBER_OF_PAGES_TO_LOAD} ---- Actual Clicks: {ACTUAL_NUMBER_OF_PAGES_LOADED}")


def testUnHappyPath():
    assert(True)
    # leaving for you to add on based on this if you want to :)

if __name__ == '__main__':

    testUnHappyPath()

    testHappyPath()