"""
Automated LinkedIn Connections
Jan. 2023
By: Jake Mann
Thanks to DataFlair and stackoverflow
and ChatGPT!
"""

# %% Import libraries

from secret import *  # username and password
from helperfunctions import *

# %%LOGIN
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
    browser.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
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

# %% COLLECT NAMES - to be called later

def names(howmanynames, page):
    wait(5)
    #Initialize variables
    namestrings = []
    lastnames = []
    acclist = ""  # TO BE USED LATER
    alreadydonelist = "" #FOR GOING BACK THROUGH A LIST A SECOND TIME

    """ while "ember-view t-sans t-16 t-black t-bold lists-detail__view-profile-name-link" not in browser.find_element(By.CSS_SELECTOR, ".selected-element").get_attribute("class"):
        # Press the Tab key
        selected_element.send_keys(Keys.TAB)
        # Wait for a short period to allow the page to update
        WebDriverWait(browser, 2).until(EC.staleness_of(selected_element))
        # Find the newly selected element
        selected_element = browser.find_element(By.CSS_SELECTOR, ".selected-element") 
    
    #browser.find_element("css selector", "ember-view t-sans t-16 t-black t-bold lists-detail__view-profile-name-link")

      tabonly(1)
    while browser.find_element_by_class_name("ember-view t-sans t-16 t-black t-bold lists-detail__view-profile-name-link").text != browser.switch_to.active_element.text:
        print('hitting tab to get to next element')
        tabonly(1) 

    element = browser.find_elements_by_class_name("ember-view t-sans t-16 t-black t-bold lists-detail__view-profile-name-link")
    #element = browser.find_element(By.CLASS_NAME, "ember-view t-sans t-16 t-black t-bold lists-detail__view-profile-name-link").text
    # Get the frontend text of the element
    print(element)
    #frontend_text = element.text
    # Print the frontend text
    #print("SHOULD BE BOB: " + str(frontend_text))

    #THIS ONE ALMOST WORKED
    #browser.find_element_by_xpath("//label[@class='list-detail__checkbox-label m0']")
    #tabonly(1)"""

    if page-1 == 1:
        tabonly(10)
    else:
        tabonly(23)

   

    print("TABONLY BOB SLECTOR: " + str(browser.switch_to.active_element.text))

    #tabonly(10)  # Nav to first name tab- hardocded
    sleep(5)
    
    #%% GET NAME AND THEN ACCOUNT NUMBER THEN TO NEXT NAME

    for i in range(howmanynames): #FROM THE FIRST NAME - gives acclist and namestrings
    
        name = browser.switch_to.active_element.text
        print("name selected : " + str(name))
        namestrings.append(name)
        lastnames.append(nameeval(name))

        tabonly(2) #gets to company data- hardcoded

        if "Add " in browser.switch_to.active_element.text:  
            # MAKES ACCLIST- if NO ACCOUNT, "0"
            acclist += "0"  # PLACES ZERO
            print("entry "+ str(i+1) + " of the list is a zero")
            tabonly(2)

            #make the alreadydonelist, which tells you if you've already done this guy
            if "No activity" in browser.switch_to.active_element.text:
                alreadydonelist += "0"
            else:
                alreadydonelist += "1"

            if i != range(howmanynames): #not end of list
                tabonly(4)  #hardcoded- needs one less tab if no company
            sleep(5)
        else:
            acclist += "1"
            print("entry "+ str(i+1) +" of the list is a one")
            tabonly(3)

            if "No activity" in browser.switch_to.active_element.text:
                alreadydonelist += "0"
            else:
                alreadydonelist += "1"

            if i != range(howmanynames): #as long as not end of list
                tabonly(4)  #hardcoded- needs one more if yes company idk why
            sleep(5)
        print("\n-----\n")

    print(namestrings) #TROUBLESHOOTING- PRINTS ALL BROWSERTITLES TO TEST NAME SPLICER
    #print(lastnames)
   
    wait(10)
    acclist = [char for char in acclist]  # makes more parseable
    alreadydonelist = [char for char in alreadydonelist]
    print("\nACCLIST: \n"+str(acclist))
    print("\nLASTNAMELIST: \n"+str(lastnames))
    print("\nALREADYDONELIST: \n"+str(alreadydonelist))
    return lastnames, acclist, alreadydonelist


# %% CONNECT- THE MEAT


def connect(startfrom=0, legit="no", cheat="no"):
    totalconns = browser.find_element_by_class_name("artdeco-spotlight-tab__primary-text").text  # TOTAL CONNECTIONS ON THE WHOLE LIST
    print(
        "total connections = " + totalconns
    )  # Spits the right number but needs to be 25 unless on last page

    pagebuttons = browser.find_elements_by_xpath(
        "//button[@type='button' and starts-with(@aria-label,'Page ')]"
    )  # HOW MANY PAGES? For iterating through
    # print the number of buttons found
    print(f"Number of pages: {len(pagebuttons)}")

    #   browser.find_element_by_xpath(f"//button[@type='button' and starts-with(@aria-label, 'Page {2}')]").click() #CLICKS NEXT PAGE TO START OVER

    for page in range(2, len(pagebuttons) + 1):
        print("current page = " + str(page - 1))
        if page - 1 != len(pagebuttons):
            howmany = 25
        else:
            howmany = totalconns % 25

        # If there's not a single available account skip the page!
        if "No activity" in browser.page_source:
            pass
        else:
            print("SKIPPING PAGE " + str(page-1) + " bc it's already done")
            browser.find_element_by_xpath(
            f"//button[@type='button' and starts-with(@aria-label, 'Page {page}')]"
            ).click()  # CLICKS NEXT PAGE TO START OVER
            sleep(8)
            freshstart()
            continue

        # initial data
        l = browser.find_elements_by_xpath(
            "//*[@class= 'list-detail-dropdown-trigger__icon']"
        )[startfrom:howmany]
        account = browser.find_elements_by_xpath(
            "//*[@class= 'artdeco-entity-lockup__title artdeco-entity-lockup__title--alt-link ember-view']"
        )
        noaccount = browser.find_elements_by_xpath(
            "//*[@class= 'list-detail-account-matching__text']"
        )

        # GET LIST OF SPLICED NAMES FROM THE NAMES FUNCTION- or if testing, hardcoded
        if cheat == "no":
            finnames, acclist, alreadydonelist = names(howmany, page)
        else:  # CHANGE W EACH TEST
            finnames = ['Bob Cunanan', 'Miranda Cobo', 'Tino Marino', 'Chelsea Campbell', 'Taylor Wical', 'estevan M.', 'Lorenzo Mesina Jr.', 'Karima L.', 'Anthony Elibert', 'Isiah Munoz', 'Michelle P.', 'Patti Becker', 'Edu Honesko', 'Maya Sanden', 'Kimberly Derrick', 'Anita Holcomb-Stone', 'Andy Starnes', 'Lucas Crawford', 'Joshua Rucker', 'David Tofani', 'Robert Pearey', 'Amanda Quintana', 'Stephanie Driscoll', 'Jennifer Brock', 'Ian Doyle']
            acclist = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            alreadydonelist = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            print("using cheat list")

        # statuses
        print("\nLIST OF TOTAL ROWS (25 if full page) = ", len(l))
        print(
            "TOTAL EXISTING ACCOUNTS (should be {}) = ".format(len(account)),
            acclist.count("1"),
        )
        print(
            "TOTAL 'add accounts' (should be {}) = \n".format(len(noaccount)),
            acclist.count("0"),
        )

        # MAKE IT HAPPEN
        failindexes = []
        for i in range(startfrom, howmany):  # CHANGE THIS CHANGE THIS CHANGE THIS
            #for unexpected errors with connecting
            strike = 1
            while True:
                if finnames[i] == "":
                    print("SKIPPING THE LUNATIC WITHOUT PUNCTUATION IN THEIR NAME- NUMBER {}".format(i+1))
                    break
                if alreadydonelist[i] == "1": #IF HAS ALREADY BEEN SUCCESSFULLY DONE DONT WASTE THE TIME
                    print("ALREADY DID "+str(finnames[i])+" (NUMBER {}) ON A PREVIOUS RUN".format(i+1))
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
                            textbox.send_keys(createmsg(day_of_week(), finnames[i]))
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
                            ActionChains(browser).send_keys(
                                createmsg(day_of_week(), finnames[i])
                            ).perform()

                        sleep(5)
                        # SUMBIT = 2, CANCEL = 1 below
                        if legit == "yes":
                            tabenter(2)
                            print(
                                "Just connected with PokeTrainer "
                                + str(finnames[i])
                                + ", entry number "
                                + str(i + 1)
                            )
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
                            print("SKIPPING NUMBER ", str(i + 1))
                            failindexes.append(i + 1)
                            break
        print(
            "\n-----\nON PAGE "
            + str((page-1))
            + ", Connected to "
            + str(len(range(startfrom, howmany)) - len(failindexes))
            + " out of "
            + str(len(l))
            + " accounts. Failures include "
            + ", ".join(str(finnames[i]) for i in failindexes)
            + " (names "
            + str(failindexes)
            + ")"
        )

        browser.find_element_by_xpath(
            f"//button[@type='button' and starts-with(@aria-label, 'Page {page}')]"
        ).click()  # CLICKS NEXT PAGE TO START OVER
        sleep(8)
        freshstart()


# %% Get shit bumpin
# Open the webbrowser and use it for autonomous control

# Start using the functions after a delay
wait(10)

# Call all the functions in order based on webpages
login_to_linkedin("Personal Trainers 8")  # NAV TO THIS LIST
connect(startfrom=0, legit="yes", cheat="no")
