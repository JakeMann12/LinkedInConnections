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
    finstring = (
        "Hello "
        + firstname
        + ", Happy "
        + day_of_week
        + "!\n\nI have recently begun a software company specializing in custom solutions in the fitness industry and found your profile. As an independent owner, I really admire what you’re doing and would love to talk about strengthening your digital presence with a new website?"
    )
    if len(finstring) > 300:
        finstring = (
        "Howdy "
        + firstname
        + "!\n\nI have recently begun a software company specializing in custom solutions in the fitness industry and found your profile. As an independent owner, I really admire what you’re doing and would love to talk about strengthening your digital presence with a new website?"
    )

    return finstring


def nameeval(name):
    name = name.split(" | ")[0]  # removes SalesNav part
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


print(nameeval("Leonard Dimitri DaSilva, MD, MBA | Sales Navigator"))
