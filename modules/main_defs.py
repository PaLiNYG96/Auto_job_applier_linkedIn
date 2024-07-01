# Imports
import os
import csv
import re
import pyautogui

pyautogui.FAILSAFE = False
from random import choice, shuffle
from datetime import datetime
from modules.open_chrome import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException
from setup.configDice import *
from modules.helpers import *
from modules.clickers_and_findersDICE import *
from modules.validator import validate_config

# Function to check if user is logged-in in LinkedIn
def is_logged_in_DICE():
    if driver.current_url == "https://www.dice.com/home/home-feed": return True
    if try_linkText(driver, "Sign in"): return False
    if try_xp(driver, '//button[@type="submit" and contains(text(), "Sign in")]'):  return False
    if try_linkText(driver, "Join now"): return False
    print_lg("Didn't find Sign in link, so assuming user is logged in!")
    return True


# Function to login for LinkedIn
def login_LN():
    # Find the username and password fields and fill them with user credentials
    driver.get("https://www.dice.com/dashboard/login")
    try:
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Forgot password?")))
        try:
            text_input_by_ID(driver, "email", username, 1)
        except Exception as e:
            print_lg("Couldn't find username field.")
            # print_lg(e)
        try:
            text_input_by_ID(driver, "password", password, 1)
        except Exception as e:
            print_lg("Couldn't find password field.")
            # print_lg(e)
        # Find the login submit button and click it
        driver.find_element(By.XPATH, '//button[@type="submit" and contains(text(), "Sign in")]').click()
    except Exception as e1:
        try:
            profile_button = find_by_class(driver, "profile__details")
            profile_button.click()
        except Exception as e2:
            # print_lg(e1, e2)
            print_lg("Couldn't Login!")

    try:
        # Wait until successful redirect, indicating successful login
        wait.until(EC.url_to_be(
            "https://www.dice.com/home/home-feed"))  # wait.until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space(.)="Start a post"]')))
        return print_lg("Login successful!")
    except Exception as e:
        print_lg(
            "Seems like login attempt failed! Possibly due to wrong credentials or already logged in! Try logging in manually!")
        # print_lg(e)
        manual_login_retry(is_logged_in_DICE, 2)

