# -*- coding: utf-8 -*-
"""
All helper functions for LinkedIn file
By: Jake Mann
January 2023
"""
# %% Imports

# Selenium and time
from selenium import webdriver
from time import sleep

# for Connect
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for name scraping
import re

# for message- day of week
import datetime

browser = webdriver.Chrome()

# %% Helper functions


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
    days = ["Monday", "Tuesday", "Hump Day", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[today]

#%% Fitness functions- messages for personal trainers

def createmsg(day_of_week, firstname):
    # finstring = "Hello Dr. "+lastname+", Happy "+day_of_week+"!\n\nI was reaching out to ask about any logistical inefficiencies in your practice’s daily operations. My company, Titan Software, specializes in custom HIPAA-compliant medical software and implementation. Could we meet and discuss your needs?\n\nThank you,\nJake Mann"
    #message = "I have recently begun a software company specializing in custom solutions in the fitness industry. As an independent owner, I really admire what you’re doing and would love to talk about easing some of your daily pain points with tailor-made software?"
    #message = "I have recently begun a software company specializing in custom solutions for new entrepreneurs. As an independent owner, I really admire what you’re doing and would love to talk about easing your early development with tailor-made software or a fresh website?"
    #Entrepreneur Message
    #message = "Would you be available for a short interview? I started a custom software company for startups and I would love to pick your brain to learn more about our clientele. I won't use this time to pitch anything, rather just better understand your daily pain points."
    #Event planners
    #message = "Would you be available for a short interview? I’m considering beginning a virtual assistant (VA) company for event planners and I would love to pick your brain to learn more about our potential clientele. I would love to hear about a day in your life."
    #Older entrepreneurs
    message = "Would you be interested in buying a three day weekend? My cofounder and I have recently begun a Virtual Personal Assistant (VPA) company and would love to speak with you to see if we can help a fellow entrepreneur free up some time by delegating monotonous tasks."

    finstring = (
        "Hello "
        + firstname
        + ", Happy "
        + day_of_week
        + "!\n\n"
    )
    if len(finstring+message) > 300:
        finstring = (
        "Howdy "
        + firstname
        + "!\n\n"
    )
    finstring += message

    return finstring

#%% Nameeval

def nameeval(name):
    if "," in name:
        name = name.split(",")[0]
    finname = name.split()[0].capitalize()
    return finname

def OLDTABNAMEnameeval(name):
    #name = name.split(" | ")[0]  # removes SalesNav part
    if "," in name:
        name = name.split(",")[0]
    try:
        pattern = r"\b[A-Z][a-z]+[^.,\s]+\b"
        name = re.findall(pattern, name)[0]
        statusstring = "Trainer name: " + name
    except:
        name = ""
        statusstring = "This dood didn't work. Continuing...\n"
    if name == "Navigator":
        name = ""
        statusstring = "This dood didn't work. Continuing...\n"
    return name, statusstring


print(nameeval("Leonard Dimitri DaSilva, MD, MBA | Sales Navigator"))

#%% Doctor Functions- just for Medical RIP

def doctorcreatemsg(day_of_week, lastname):
    # finstring = "Hello Dr. "+lastname+", Happy "+day_of_week+"!\n\nI was reaching out to ask about any logistical inefficiencies in your practice’s daily operations. My company, Titan Software, specializes in custom HIPAA-compliant medical software and implementation. Could we meet and discuss your needs?\n\nThank you,\nJake Mann"
    if len(lastname) <= 10:
        finstring = (
            "Hello Dr. "
            + lastname
            + ", Happy "
            + day_of_week
            + "!\n\nI have recently launched a medical software company and was hoping to connect with you to learn more about your firm’s existing software solutions. I'm not looking to pitch anything, just learn about your practice. Could we meet over Zoom?\n\nThank you,\nJake Mann"
        )
    else:
        finstring = (
            "Hello Dr. "
            + lastname
            + ",\n\nI have recently launched a medical software company and was hoping to connect with you to learn more about your firm’s existing software solutions. I'm not looking to pitch anything, just learn about your practice. Could we meet over Zoom?\n\nThank you,\nJake Mann"
        )
    return finstring


def doctornameeval(name):
    name = name.split(" | ")[0]  # removes SalesNav part
    if "," in name:
        name = name.split(",")[0]
    try:
        pattern = r"\b[A-Z][a-z]+[^.,\s]+\b"
        name = re.findall(pattern, name)[-1]
        statusstring = "DR. " + name
    except:
        name = ""
        statusstring = "This dood didn't work. Continuing...\n"
    if name == "Navigator":
        name = ""
        statusstring = "This dood didn't work. Continuing...\n"
    return name, statusstring

# %% COLLECT NAMES - to be called later

def names(howmanynames, page):
    wait(5)
    #Initialize variables
    namestrings = []
    lastnames = []
    acclist = ""  # TO BE USED LATER
    alreadydonelist = "" #FOR GOING BACK THROUGH A LIST A SECOND TIME

    if page == 1:
        tabonly(10)
    else:
        tabonly(23)
    sleep(5)
    
    # GET NAME AND THEN ACCOUNT NUMBER THEN TO NEXT NAME
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

print(nameeval("Leonard Dimitri DaSilva, MD, MBA | Sales Navigator"))
