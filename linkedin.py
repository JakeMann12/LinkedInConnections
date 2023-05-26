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

    for page in range(1, len(pagebuttons) + 1):
        print("current page = " + str(page))

        #GO TO NEXT PAGE IF NOT THE FIRST PAGE
        if page != 1:
            browser.find_element_by_xpath(
                f"//button[@type='button' and starts-with(@aria-label, 'Page {page}')]"
            ).click()  # CLICKS NEXT PAGE TO START OVER
            sleep(8)
            freshstart()

        
        if page != len(pagebuttons):
            howmany = 25
        else:
            howmany = int(totalconns) % 25

        # If there's not a single available account skip the page!
        if "No activity" in browser.page_source:
            pass
        else:
            print("SKIPPING PAGE " + str(page) + " bc it's already done")
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

        # for total metrics
        totsucc = 0
        totposs = 0
        thisrunsucc = 0

        for i in range(startfrom, howmany):  # CHANGE THIS CHANGE THIS CHANGE THIS
            failindexes = []
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
                            thisrunsucc += 1
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
            successes = len(range(startfrom, howmany)) - len(failindexes)
            totsucc += successes
            maxconns = len(l)
            totposs += maxconns
            print(
                "\n-----\nON PAGE "
                + str((page))
                + ", Connected to "
                + str(successes)
                + " out of "
                + str(maxconns)
                + " accounts. Failures include "
                + ", ".join(str(finnames[i]) for i in failindexes)
                + " (names "
                + str(failindexes)
                + ")")
        print("\n--------\n\nFINAL RESULTS OF THIS RUN:\n now connected to " 
              + str(totsucc) 
              + " out of " 
              + str(totposs) 
              + " entries on the list. This might not be perfect, but if it's run more than twice then it just may be a fringe case."
              + "\n This run specifically, connected to "
              + str(thisrunsucc)
              + " people. Good looks!")


# %% Get shit bumpin
# Open the webbrowser and use it for autonomous control

# Start using the functions after a delay
wait(10)

# Call all the functions in order based on webpages
login_to_linkedin("Personal Trainers 9")  # NAV TO THIS LIST
connect(startfrom=0, legit="yes", cheat="no")
