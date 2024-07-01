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
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from setup.configDice import *
from modules.helpers import *
from modules.clickers_and_findersDICE import *
from modules.validator import validate_config

if run_in_background == True:
    pause_at_failed_question = False
    pause_before_submit = False
    run_non_stop = False
tabs_count = 1


# Login Functions

# Function to check if user is logged-in in DICE
def is_logged_in_DICE():
    if driver.current_url == "https://www.dice.com/home/home-feed": return True
    if try_linkText(driver, "Sign in"): return False
    if try_xp(driver, '//button[@type="submit" and contains(text(), "Sign in")]'): return False
    if try_linkText(driver, "Join now"): return False
    print_lg("Didn't find Sign in link, so assuming user is logged in!")
    return True


# Function to login for DICE
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
            "https://www.dice.com/home/home-feed"))
        return print_lg("Login successful!")
    except Exception as e:
        print_lg(
            "Seems like login attempt failed! Possibly due to wrong credentials or already logged in! Try logging in manually!")
        # print_lg(e)
        manual_login_retry(is_logged_in_DICE, 2)


# Function to get list of applied job's Job IDs
def get_applied_job_ids():
    job_ids = set()
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                job_ids.add(row[0])
    except FileNotFoundError:
        print_lg(f"The CSV file '{file_name}' does not exist.")
    return job_ids


# Function to apply job search filters
def apply_filters():
    try:
        recommended_wait = 1 if click_gap < 1 else 0

        buffer(recommended_wait)

        multi_sel(driver, Work_Settings)

        wait_span_click(driver, date_posted)

        buffer(recommended_wait)

        multi_sel(driver, Employment_Type)

        if Work_Auth:
            WorkAuth = driver.find_element(By.CSS_SELECTOR,
                                           "[aria-label='Filter Search Results by Work Authorization']")
            WorkAuth.click()

        multi_sel(driver, Employer_Type)

        EasyApply = driver.find_element(By.CSS_SELECTOR, "[aria-label='Filter Search Results by Easy Apply']")
        EasyApply.click()

    except Exception as e:
        print_lg("Setting the preferences failed!")
        # print_lg(e)


# Function to get pagination element and current page number
def get_page_info():
    try:
        pagination_element = find_by_class(driver, "pagination")
        scroll_to_view(driver, pagination_element)
        current_page = int(pagination_element.find_element(By.XPATH, "//li[contains(@class, 'active')]").text)
    except Exception as e:
        print_lg("Failed to find Pagination element, hence couldn't scroll till end!")
        pagination_element = None
        current_page = None
        # print_lg(e)
    return pagination_element, current_page


# Function to get job main details
def get_job_main_details(job):
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    job_details_button = job.find_element(By.CLASS_NAME, "card-title-link")
    scroll_to_view(driver, job_details_button, True)
    title = job_details_button.text
    company = job.find_element(By.XPATH, "//a[@data-cy = 'search-result-company-name']").text
    job_id = job.get_dom_attribute('data-cy-value')
    work_location = job.find_element(By.XPATH, "//span[@data-cy = 'search-result-location']").text
    work_style = work_location[work_location.rfind('(') + 1:work_location.rfind(')')]
    work_location = work_location[:work_location.rfind('(')].strip()
    scroll_to_view(driver, job_details_button, False)
    try:
        job_details_button.click()
        # Wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
    except Exception as e:
        print_lg(f'Failed to click "{title} | {company}" job on details button.')
        # print_lg(e)
        job_details_button.click()
    buffer(click_gap)
    return (job_id, title, company, work_location, work_style)


# Function to check for Blacklisted words in About Company
def check_blacklist(rejected_jobs, title, job_id, company, blacklisted_companies):
    c = driver.find_element(By.XPATH, "//a[@data-cy = 'companyNameLink']")
    c.click()
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//article[@data-cy = 'companyDescription']")))
    try:
        if driver.find_element(By.XPATH, "//seds-icon[@class = 'hydrated']"):
            show_more_button = driver.find_element(By.XPATH, "//seds-icon[@class = 'hydrated']")
            show_more_button.click()
    except Exception as e:
        print_lg('Click Failed, Didnt find a Show More Button... ')
    about_company_org = driver.find_element(By.XPATH, "//article[@data-cy = 'companyDescription']")
    scroll_to_view(driver, about_company_org)
    about_company_org = about_company_org.text
    about_company = about_company_org.lower()
    skip_checking = False

    for word in blacklist_exceptions:
        if word.lower() in about_company.lower():
            print_lg(f'Found the word "{word}". So, skipped checking for blacklist words.')
            skip_checking = True
            break
    try:
        if (len(job_titles) > 0):
            found = len(job_titles)
            trys = found
            for word in job_titles:
                if re.search(r'\b' + re.escape(word) + r'\b', title, re.IGNORECASE):
                    print_lg(f'Found good Job Title "{word}". Will attempt applying to this Job. ')
                    skip_checking = False
                else:
                    rejected_jobs.add(job_id)
                    skip_checking = False
                    trys = trys - 1
                if (trys == 0):
                    raise ValueError(f'Job title doesn\'t match any of your preset key words')
    except Exception as e1:
        print_lg("No Key words found to search for in Job titles...")
        print_lg('Skipping this job.', e1)
        failed_job(job_id, word, "Found Blacklisted words in About Company", e1,"Skipped")

    if not skip_checking:
        for word in blacklist_words:
            if word.lower() in about_company.lower():
                rejected_jobs.add(job_id)
                raise ValueError(f'Found the word "{word}" in about company Description.... SKIPPING')
    buffer(click_gap)
    driver.execute_script("window.history.go(-1)")
    scroll_to_view(driver, driver.find_element(By.XPATH, "//p[contains(text(), 'Overview')]"))
    return rejected_jobs, blacklisted_companies


# Function to extract years of experience required from About Job
def extract_years_of_experience(text):
    # Extract all patterns like '10+ years', '5 years', '3-5 years', etc.
    matches = re.findall(r'[(]?\s*(\d+)\s*[)]?\s*[-to]*\s*\d*[+]*\s*year[s]?', text, flags=re.IGNORECASE)
    if len(matches) == 0:
        print_lg(f'Couldn\'t find experience requirement in About job')
    return max([int(match) for match in matches if int(match) <= 12])


# Function to update failed jobs list in excel
def failed_job(job_id, job_link, resume, date_listed, error, exception, application_link, screenshot_name):
    with open(failed_file_name, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['Job ID', 'Job Link', 'Resume Tried', 'Date listed', 'Date Tried', 'Assumed Reason',
                      'Stack Trace', 'External Job link', 'Screenshot Name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0: writer.writeheader()
        writer.writerow({'Job ID': job_id, 'Job Link': job_link, 'Resume Tried': resume, 'Date listed': date_listed,
                         'Date Tried': datetime.now(), 'Assumed Reason': error, 'Stack Trace': exception,
                         'External Job link': application_link, 'Screenshot Name': screenshot_name})
        file.close()


# Function to to take screenshot for debugging
def screenshot(driver, job_id, failedAt):
    screenshot_name = "{} - {} - {}.png".format(job_id, failedAt, str(datetime.now()))
    path = logs_folder_path + "/screenshots/" + screenshot_name.replace(":", ".")
    # special_chars = {'*', '"', '\\', '<', '>', ':', '|', '?'}
    # for char in special_chars:  path = path.replace(char, '-')
    driver.save_screenshot(path.replace("//", "/"))
    return screenshot_name


# Function to create or append to the CSV file, once the application is submitted successfully
def submitted_jobs(job_id, title, company, work_location, work_style, description, experience_required, skills, hr_name,
                   hr_link, resume, reposted, date_listed, date_applied, job_link, application_link, questions_list,
                   connect_request):
    with open(file_name, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Job ID', 'Title', 'Company', 'Work Location', 'Work Style', 'About Job', 'Experience required',
                      'Skills required', 'HR Name', 'HR Link', 'Resume', 'Re-posted', 'Date Posted', 'Date Applied',
                      'Job Link', 'External Job link', 'Questions Found', 'Connect Request']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0: writer.writeheader()
        writer.writerow({'Job ID': job_id, 'Title': title, 'Company': company, 'Work Location': work_location,
                         'Work Style': work_style,
                         'About Job': description, 'Experience required': experience_required,
                         'Skills required': skills,
                         'HR Name': hr_name, 'HR Link': hr_link, 'Resume': resume, 'Re-posted': reposted,
                         'Date Posted': date_listed, 'Date Applied': date_applied, 'Job Link': job_link,
                         'External Job link': application_link, 'Questions Found': questions_list,
                         'Connect Request': connect_request})
    csv_file.close()

# Function to apply to jobs
def apply_to_jobs(search_terms):
    applied_jobs = get_applied_job_ids()
    rejected_jobs = set()
    blacklisted_companies = set()

    if randomize_search_order:  shuffle(search_terms)
    for searchTerm in search_terms:
        driver.get(f"https://www.dice.com/jobs?q={searchTerm}")
        print_lg(
            "\n________________________________________________________________________________________________________________________\n")
        print_lg(f'\n>>>> Now searching for "{searchTerm}" <<<<\n\n')

        apply_filters()

        current_count = 0
        try:
            while current_count < switch_number:
                # Wait until job listings are loaded
                wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//dhi-search-card[@data-cy = 'search-card']")))
                pagination_element, current_page = get_page_info()

                # Find all job listings in current page
                buffer(3)
                job_listings = driver.find_elements(By.XPATH, "//dhi-search-card[@data-cy = 'search-card']")
                buffer(3)
                # print_lg(job_listings)

                for job in job_listings:
                    windows = driver.window_handles
                    tabs_count = len(windows)
                    if tabs_count > 1:
                        driver.switch_to.window(Dice_tab)
                        driver.switch_to.window(windows[+1])
                        driver.close()
                        driver.switch_to.window(Dice_tab)
                    if keep_screen_awake: pyautogui.press('shiftright')
                    if current_count >= switch_number: break
                    print_lg("\n-@-\n")
                   

                    job_id, title, company, work_location, work_style = get_job_main_details(job)

                    # Skip if previously rejected due to blacklist or already applied
                    if company in blacklisted_companies:
                        print_lg(f'Skipping "{title} | {company}" job (Blacklisted Company).')
                        continue
                    elif job_id in rejected_jobs:
                        print_lg(f'Skipping previously rejected "{title} | {company}" job.')
                        continue
                    try:
                        if job_id in applied_jobs or find_by_class(driver, "application-submitted", 2):
                            print_lg(f'Already applied to "{title} | {company}" job.')
                            continue
                    except Exception as e:
                        print_lg(f'Trying to Apply to "{title} | {company}" job. Job ID: {job_id}')

                    job_link = "https://www.dice.com/job-detail/" + job_id
                    application_link = "Easy Applied"
                    date_applied = "Pending"
                    hr_link = "Unknown"
                    hr_name = "Unknown"
                    connect_request = "In Development"  # Still in development
                    date_listed = "Unknown"
                    description = "Unknown"
                    experience_required = "Unknown"
                    skills = "In Development"  # Still in development
                    resume = "Pending"
                    updated = False
                    questions_list = None
                    screenshot_name = "Not Available"

                    try:
                        rejected_jobs, blacklisted_companies = check_blacklist(rejected_jobs, title, job_id, company,
                                                                               blacklisted_companies)
                    except ValueError as e:
                        print_lg('Skipping this job.', e)
                        failed_job(job_id, job_link, resume, date_listed, "Found Blacklisted words in About Company", e,
                                   "Skipped", screenshot_name)
                        continue
                    except Exception as e:
                        print_lg("Failed to scroll to About Company!")
                        # print_lg(e)

                    # Calculation of date posted
                    try:
                        jobs_top_card = driver.find_element(By.ID, "timeAgo")
                        time_posted_text = jobs_top_card.text
                        if time_posted_text.__contains__("Updated"):
                            updated = True
                        date_listed = time_posted_text
                    except Exception as e:
                        print_lg("Failed to calculate the date posted!")
                        # print_lg(e)

                    # Get job description
                    try:
                        JobDescriptionToggle = driver.find_element(By.ID, "descriptionToggle")
                        JobDescriptionToggle.click()

                        description = driver.find_element(By.ID,
                                                          "jobDescription").text
                        descriptionLow = description.lower()
                        if security_clearance is False and (
                                'polygraph' in descriptionLow or 'security clearance' in descriptionLow or 'secret clearance' in descriptionLow):
                            print_lg(f'Skipping this job. Found "Security Clearence" or "Polygraph" in \n{description}')
                            experience_required = "Skipped checking (Polygraph)"
                        if did_masters and current_experience >= 2 and 'master' in descriptionLow:
                            print_lg(
                                f'Skipped checking for minimum years of experience required cause found the word "master" in \n{description}')
                            experience_required = "Skipped checking (Masters)"
                        else:
                            experience_required = extract_years_of_experience(description)
                            if -1 < current_experience < experience_required:
                                message = f'Experience required {experience_required} > Current Experience {current_experience}\n{description}'
                                print_lg('Skipping this job.', message)
                                failed_job(job_id, job_link, resume, date_listed, "Required experience is high",
                                           message, "Skipped", screenshot_name)
                                rejected_jobs.add(job_id)
                                continue
                    except Exception as e:
                        if description == "Unknown":
                            if driver.current_url.__contains__("company_profile"): driver.execute_script(
                                "window.history.go(-1)")
                            print_lg("Unable to extract job description!")
                        else:
                            experience_required = "Error in extraction"
                            if driver.current_url.__contains__("company_profile"): driver.execute_script(
                                "window.history.go(-1)")
                            print_lg("Unable to extract years of experience required!")
                        # print_lg(e)

                    # Case 1: Easy Apply Button
                    success = True
                    if driver.current_url.__contains__("company_profile"): driver.execute_script("window.history.go(-1)")
                    if wait_for_easy_apply(driver, "applyButton", 2):
                        try:
                            try:
                                resume = default_resume_path
                                wait_span_click(driver, "Next", 1)
                                wait_span_click(driver, "Submit", 1)
                                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,
                                                                                               '//h1[normalize-space(.)="Application submitted. We\'re rooting for you."]')))
                                success = True
                                print_lg(f'job for "{title}", submitted successfully')
                            except Exception as e:
                                print_lg("Couldnt Submit application!!")
                                success = False
                                failed_job(job_id, job_link, resume, date_listed, "Problem in Easy Applying", e,
                                application_link, screenshot_name)
                                #print_lg(e)
                            try:
                                driver.close()
                                driver.switch_to.window(Dice_tab)
                                continue
                            except Exception as e:
                                print_lg("Couldnt exit Job page!!!", e)

                        except Exception as e:
                            print_lg("Failed to Easy apply!")
                            success = False
                            # print_lg(e)
                            critical_error_log("Somewhere in Easy Apply process", e)
                            failed_job(job_id, job_link, resume, date_listed, "Problem in Easy Applying", e,
                                       application_link, screenshot_name)
                    else:
                        critical_error_log("Somewhere in Easy Apply process", e)
                        failed_job(job_id, job_link, resume, date_listed, "Problem in Easy Applying", e,
                                   application_link, screenshot_name)
                        success = False
                        
                    if success:
                        submitted_jobs(job_id, title, company, work_location, work_style, description, experience_required,
                                    skills, hr_name, hr_link, resume, updated, date_listed, date_applied, job_link,
                                    application_link, questions_list, connect_request)

                        print_lg(f'Successfully saved "{title} | {company}" job. Job ID: {job_id} info')
                        current_count += 1
                        applied_jobs.add(job_id)
                    else:
                        critical_error_log("Somewhere in Easy Apply process", e)
                        failed_job(job_id, job_link, resume, date_listed, "Problem in Easy Applying", e,
                                   application_link, screenshot_name)
                        success = False

                # Switching to next page
                if pagination_element == None:
                    print_lg("Couldn't find pagination element, probably at the end page of results!")
                    break
                try:
                    windows = driver.window_handles
                    tabs_count = len(windows)
                    if tabs_count > 1:
                        driver.switch_to.window(Dice_tab)
                        driver.switch_to.window(windows[+1])
                        driver.close()
                        driver.switch_to.window(Dice_tab)
                    pagination_element.find_element(By.XPATH,
                                                    f"//li/a[contains(text(), '{current_page + 1}')]").click()
                    print_lg(f"\n>-> Now on Page {current_page + 1} \n")
                except NoSuchElementException:
                    print_lg(f"\n>-> Didn't find Page {current_page + 1}. Probably at the end page of results!\n")
                    break

        except Exception as e:
            print_lg("Failed to find Job listings!")
            critical_error_log("In Applier", e)
            # print_lg(e)


def run(total_runs):
    print_lg(
        "\n########################################################################################################################\n")
    print_lg(f"Date and Time: {datetime.now()}")
    print_lg(f"Cycle number: {total_runs + 1}")
    print_lg(f"Currently looking for jobs posted within '{date_posted}'")
    apply_to_jobs(search_terms)
    print_lg(
        "########################################################################################################################\n")
    print_lg("Sleeping for 10 min...")
    sleep(0)
    print_lg("Few more min... Gonna start with in next 5 min...")
    buffer(-3)
    return total_runs + 1


chatGPT_tab = False
Dice_tab = False


def main():
    try:
        alert_title = "Error Occurred. Closing Browser!"
        validate_config()
        make_directories([file_name, failed_file_name, logs_folder_path + "/screenshots", default_resume_path])
        if not os.path.exists(default_resume_path):   raise Exception(
            'Your default resume "{}" is missing! Please update it\'s folder path in config.py or add a resume with exact name and path (check for spelling mistakes including cases).'.format(
                default_resume_path))

        # Login to DICE
        global tabs_count
        tabs_count = len(driver.window_handles)
        driver.get("https://www.dice.com/dashboard/login")
        if not is_logged_in_DICE(): login_LN()
        global Dice_tab
        Dice_tab = driver.current_window_handle


        # Start applying to jobs
        driver.switch_to.window(Dice_tab)
        total_runs = 0
        total_runs = run(total_runs)

    except NoSuchWindowException:
        pass
    except Exception as e:
        critical_error_log("In Applier Main", e)
        pyautogui.alert(e, alert_title)
    finally:
        quote = choice([
            "You're one step closer than before.",
            "All the best with your future interviews.",
            "Keep up with the progress. You got this.",
            "If you're tired, learn to take rest but never give up.",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
            "Every job is a self-portrait of the person who does it. Autograph your work with excellence.",
            "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. - Steve Jobs",
            "Opportunities don't happen, you create them. - Chris Grosser",
            "The road to success and the road to failure are almost exactly the same. The difference is perseverance.",
            "Obstacles are those frightful things you see when you take your eyes off your goal. - Henry Ford",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt"
        ])
        msg = f"{quote}\n\n\nBest regards.."
        pyautogui.alert(msg, "Exiting..")
        print_lg(msg, "Closing the browser...")
        if tabs_count >= 10:
            msg = "NOTE: IF YOU HAVE MORE THAN 10 TABS OPENED, PLEASE CLOSE OR BOOKMARK THEM!\n\nOr it's highly likely that application will just open browser and not do anything next time!"
            pyautogui.alert(msg, "Info")
            print_lg("\n" + msg)
        try:
            driver.quit()
        except Exception as e:
            critical_error_log("When quitting...", e)


main()
