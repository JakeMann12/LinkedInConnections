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


def names(howmanynames):
    # Locate the elements that contain the lead names
    wait(5)
    namestrings = []
    lastnames = []
    wait(30)

    acclist = ""  # TO BE USED LATER

    for i in range(howmanynames):
        # THIS WILL NOW SPIT OUT THE ACCLIST INFO (OR EQUIVALENT)
        if i == 0:  # GETS YOU TO FIRST NAME- hardcoded
            tabcontrolenter(9)  # Opens first name tab
            sleep(5)
        else:
            tabonly(4)
            if "Add note" in browser.switch_to.active_element.text:  # NO ACCOUNT
                acclist += "0"  # PLACES ZERO
                print("entry ", i, " of the list is a zero")
                tabcontrolenter(4)
                sleep(5)
            else:
                acclist += "1"
                print("entry ", i, " of the list is a one")
                tabcontrolenter(5)
                sleep(5)
            print("\n-----\n")

        # GETTING FULL TAB NAME
        wait(150)
        browser.switch_to.window(browser.window_handles[-1])
        wait(150)
        print("NAME NUMBER ", i + 1, " is ", browser.title)
        namestrings += [browser.title]

        # GETTING LAST NAME ONLY
        name, statusline = nameeval(browser.title)
        lastnames.append(name)
        print(statusline)

        wait(150)
        browser.close()
        browser.switch_to.window(browser.window_handles[1])

    # EDGE CASE- LAST ACCLIST VAL
    tabonly(4)
    if "Add note" in browser.switch_to.active_element.text:  # NO ACCOUNT
        acclist += "0"  # PLACES ZERO
        print("entry ", range(howmanynames)[-1] + 1, " of the list is a zero")
        # tabcontrolenter(4)
        sleep(5)
    else:
        acclist += "1"
        print("entry ", range(howmanynames)[-1] + 1, " of the list is a one")
        # tabcontrolenter(5)
        sleep(5)
    print("\n-----\n")

    # print(namestrings) #TROUBLESHOOTING- PRINTS ALL BROWSERTITLES TO TEST NAME SPLICER
    wait(10)
    browser.switch_to.window(browser.window_handles[0])  # likely unnecessary
    browser.switch_to.window(browser.window_handles[1])  # ditto
    acclist = [char for char in acclist]  # makes more parseable
    print(acclist)
    print(lastnames)
    return lastnames, acclist


# %% CONNECT- THE MEAT


def connect(startfrom=0, legit="no", cheat="no"):
    totalconns = browser.find_element_by_class_name(
        "artdeco-spotlight-tab__primary-text"
    ).text  # TOTAL CONNECTIONS ON THE WHOLE LIST
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

        # if startpage != 1:
        #    browser.find_element_by_xpath(f"//button[@type='button' and starts-with(@aria-label, 'Page {page}')]").click() #CLICKS NEXT PAGE TO START OVER
        #    break

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
            finnames, acclist = names(howmany)
        else:  # CHANGE W EACH TEST
            finnames = [
                "Ziemke",
                "Graber",
                "Payne",
                "Martin",
                "",
                "Shapiro",
                "Durkin",
                "Huebner",
                "Leon",
                "",
                "Jegasothy",
                "Clark-Loeser",
                "Gaines",
                "Correa-Perez",
                "Ozdemir",
                "Gupta",
                "Lickstein",
                "Croley",
                "Zaiac",
                "Krishtul",
                "Sosa",
                "Grubbs",
                "Wallace",
                "Roudner",
                "Howard",
            ]
            acclist = [
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "0",
                "0",
                "1",
                "0",
                "1",
                "1",
                "1",
                "0",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
                "1",
            ]
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
            strike = 1
            # CLICK VERSION- PREFERRED BUT SCROLL ISSUES
            while True:
                if finnames[i] == "":
                    print(
                        "SKIPPING THE LUNATIC WITHOUT PUNCTUATION IN THEIR NAME- NUMBER {}".format(
                            i
                        )
                    )
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
            + str((i + 1))
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


# %% Get shit bumpin
# Open the webbrowser and use it for autonomous control

# Start using the functions after a delay
wait(10)

# Call all the functions in order based on webpages
login_to_linkedin("Personal Trainers 9")  # NAV TO THIS LIST
connect(startfrom=0, legit="yes", cheat="no")
