"""
Automated LinkedIn Connections
Jan. 2023
By: Jake Mann
Thanks to DataFlair and stackoverflow
"""

#%% Import libraries
from secret import getemail, getpassword #username and password

#Selenium and time
from selenium import webdriver
from time import sleep

# for Connect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# for name scraping
import re

# for message- day of week
import datetime

#%% Helper functions

def wait(x):
    browser.implicitly_wait(x)

def xclick(string):
    browser.find_element_by_xpath(string).click()
    wait(5)
    print("clicked ", string, " with XPath")

def sclick(string):
    browser.find_element_by_link_text(string).click()
    wait(5)
    print("clicked ", string, " with string select\n")

def tabenter(N):
    actions = ActionChains(browser)
    for i in range(N):
        actions = actions.send_keys(Keys.TAB)
        wait(0.1)
    actions = actions.send_keys(Keys.RETURN)
    actions.perform()

def tabcontrolenter(N):
    # Create an ActionChains object
    actions = ActionChains(browser)
    # Send TAB key a certain number of times
    for i in range(N):
        actions = actions.send_keys(Keys.TAB)
        wait(0.1)
    actions = actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL)
    # Perform the key presses
    actions.perform()

def tabonly(N):
    actions = ActionChains(browser)
    for _ in range(N):
        actions = actions.send_keys(Keys.TAB)
        wait(3)
    actions.perform()


def freshstart():
    browser.refresh()
    sleep(8)

def day_of_week():
    today = datetime.datetime.today().weekday()
    days = ['Monday', 'Tuesday', 'Hump Day', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[today]

def createmsg(day_of_week, lastname):
    #finstring = "Hello Dr. "+lastname+", Happy "+day_of_week+"!\n\nI was reaching out to ask about any logistical inefficiencies in your practice’s daily operations. My company, Titan Software, specializes in custom HIPAA-compliant medical software and implementation. Could we meet and discuss your needs?\n\nThank you,\nJake Mann"
    finstring = "Hello Dr. "+lastname+", Happy "+day_of_week+"!\n\nI have recently started a medical software company and was hoping to connect with you to learn more about your firm’s needs and existing solutions. I'm not looking to pitch anything, just learn about your practice. Could we meet over Zoom?\n\nThank you,\nJake Mann"
    return finstring

    

#%%LOGIN
def login_to_linkedin(listname):
    url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
    # Open the URL in the opened webbrowser
    browser.get(url)
    # Find username
    Username = browser.find_element_by_name("session_key")
    # Send username details
    Username.send_keys(getemail())
    # Find password
    password = browser.find_element_by_name("session_password")
    # Send password details
    password.send_keys(getpassword())
    wait(3)
    # Submit button
    browser.find_element_by_xpath(
        '//*[@id="organic-div"]/form/div[3]/button'
    ).click()
    # SALESNAV THEN LEADS
    browser.implicitly_wait(5)
    # Navigate to the network page
    xclick('//*[@id="global-nav"]/div/nav/ul/li[8]/a')  # salesnav
    # SWITCH TO TAB
    browser.switch_to.window(browser.window_handles[1])  # swtiches to 1th tab
    wait(20)
    sclick("Leads")  # leads
    wait(10)
    sclick(listname)  # specific list
    wait(20)
    try:
        sclick(listname)
    except:
        wait(30)

#%% COLLECT NAMES - to be called later

def names(howmanynames = 25):
    # Locate the elements that contain the lead names
    wait(5)
    namestrings = []
    lastnames = []
    wait(30)
    
    acclist = "" #TO BE USED LATER
    
    for i in range(howmanynames):
        #THIS WILL NOW SPIT OUT THE ACCLIST INFO (OR EQUIVALENT)
        if i == 0: #GETS YOU TO FIRST NAME- hardcoded
            tabcontrolenter(9) #Opens first name tab
            sleep(5)
        else:
            tabonly(4)
            if "Add note" in browser.switch_to.active_element.text: #NO ACCOUNT
                acclist += "0" #PLACES ZERO
                print("entry ",i," of the list is a zero")
                tabcontrolenter(4)
                sleep(5)
            else:
                acclist += "1"
                print("entry ",i," of the list is a one")
                tabcontrolenter(5)
                sleep(5)
            print("\n-----\n")
        
        # GETTING FULL TAB NAME
        wait(100)
        browser.switch_to.window(browser.window_handles[-1])
        wait(100)
        print("NAME NUMBER ", i + 1, " is ", browser.title)
        namestrings += [browser.title]
        # GETTING LAST NAME ONLY
        name = browser.title
        name = name.split(" | ")[0]  # removes SalesNav part
        if "," in name:
            name = name.split(",")[0]
        try:
            pattern = r"\b[A-Z][a-z]+[^.,\s]+\b"
            name = re.findall(pattern, name)[-1]
            lastnames += [name]
        except:
            lastnames += [""]
            print("Number ", i, " didn't work. Continuing...\n")
        print("DR.", name)
        

        wait(150)
        browser.close()
        browser.switch_to.window(browser.window_handles[1])

    #EDGE CASE- LAST ACCLIST VAL
    tabonly(4)  
    if "Add note" in browser.switch_to.active_element.text: #NO ACCOUNT
        acclist += "0" #PLACES ZERO
        print("entry ",range(howmanynames)[-1]+1," of the list is a zero")
        tabcontrolenter(4)
        sleep(5)
    else:
        acclist += "1"
        print("entry ",range(howmanynames)[-1]+1," of the list is a one")
        tabcontrolenter(5)
        sleep(5)
    print("\n-----\n")
    
    # print(namestrings) #TROUBLESHOOTING- PRINTS ALL BROWSERTITLES TO TEST NAME SPLICER
    wait(10)
    browser.switch_to.window(browser.window_handles[0])#likely unnecessary
    browser.switch_to.window(browser.window_handles[1])#ditto
    acclist = [char for char in acclist] #makes more parseable
    print(acclist)
    print(lastnames)
    return lastnames, acclist


#%% CONNECT- THE MEAT

def connect(startfrom = 0, legit = 'no', cheat="no"):
    
    # initial data
    l = browser.find_elements_by_xpath(
        "//*[@class= 'list-detail-dropdown-trigger__icon']"
    )
    account = browser.find_elements_by_xpath(
        "//*[@class= 'artdeco-entity-lockup__title artdeco-entity-lockup__title--alt-link ember-view']"
    )
    noaccount = browser.find_elements_by_xpath(
        "//*[@class= 'list-detail-account-matching__text']"
    )
    
    howmany = len(l) #end of the connections
    
    # GET LIST OF SPLICED NAMES FROM THE NAMES FUNCTION- or if testing, hardcoded
    if cheat == "no":
        finnames,acclist = names(howmanynames = howmany)
    else: #CHANGE W EACH TEST
        finnames = ['Ziemke', 'Graber', 'Payne', 'Martin', '', 'Shapiro', 'Durkin', 'Huebner', 'Leon', '', 'Jegasothy', 'Clark-Loeser', 'Gaines', 'Correa-Perez', 'Ozdemir', 'Gupta', 'Lickstein', 'Croley', 'Zaiac', 'Krishtul', 'Sosa', 'Grubbs', 'Wallace', 'Roudner', 'Howard']
        acclist = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1']
        print("using cheat list")
    
    #statuses
    print("\nLIST OF TOTAL ROWS (usually 25) = ", len(l))
    print("TOTAL EXISTING ACCOUNTS (shoudl be {}) = ".format(len(account)),acclist.count('1'))
    print("TOTAL 'add accounts' (shoudl be {}) = \n".format(len(noaccount)),acclist.count('0'))
    
    
    #MAKE IT HAPPEN
    failindexes = []
    for i in range(startfrom,howmany):  # CHANGE THIS CHANGE THIS CHANGE THIS
        strike = 1
        # CLICK VERSION- PREFERRED BUT SCROLL ISSUES
        while True:
            if finnames[i] == '':
                print("SKIPPING THE LUNATIC WITHOUT PUNCTUATION IN THEIR NAME- NUMBER {}".format(i))
                break
            else:
                try:
                    l[i].click()
                    wait(30)
    
                    if acclist[i] == "1":
                        tabenter(3)
                    else:
                        tabenter(2)
    
                    wait(20)
                    sleep(5)
    
                    try:
                        textbox = browser.find_element_by_xpath(
                            '//*[@id="connect-cta-form__invitation"]'
                        )
                        sleep(3)
                        wait(20)
                        textbox.send_keys(createmsg(day_of_week(),finnames[i]))
                    except:
                        wait(40)
                        textbox = browser.find_element_by_xpath(
                            '//*[@id="connect-cta-form__invitation"]'
                        )
                        tabonly(
                            1
                        )  # super sketchy workaround- if doesn't work, hit tab once to highlight box
                        wait(50)
                        print("USING SECOND BRANCH OF CONNECT TRY TREE")
                        ActionChains(browser).send_keys(createmsg(day_of_week(),finnames[i])).perform()
    
                    sleep(5)
                    # SUMBIT = 2, CANCEL = 1 below
                    if legit == 'yes':
                        tabenter(2)
                        print("Just connected with Dr. "+str(finnames[i])+", entry number "+str(i+1))
                    else:
                        tabenter(1)
                    break
    
                except:
                    if strike != 3:
                        strike += 1
                        freshstart()  # If scroll gets fucky, refresh
                        sleep(8)
                        # refocus on right tab- might not be needed
                        browser.switch_to.window(browser.window_handles[1])
                        # redefine list handles for refresh
                        l = browser.find_elements_by_xpath(
                            "//*[@class= 'list-detail-dropdown-trigger__icon']"
                        )
                    else:
                        print("SKIPPING NUMBER ",str(i+1))
                        failindexes.append(i)
                        break
    print("\n-----\nConnected to "+str(len(l)-len(failindexes))+" accounts. Failures include Drs. "+ ", ".join(str(finnames[i]) for i in failindexes)+ " (entries "+str(failindexes)+")")

#%% Get shit bumpin
# Open the webbrowser and use it for autonomous control
browser = (
    webdriver.Chrome()
)  

# Start using the functions after a delay
wait(10)

# Call all the functions in order based on webpages

login_to_linkedin("Wide Range 14") #NAV TO THIS LIST
connect(startfrom = 0, legit = 'yes', cheat="no")
