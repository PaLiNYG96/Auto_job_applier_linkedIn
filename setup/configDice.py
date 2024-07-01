
###################################################### CONFIGURE YOUR TOOLS HERE ######################################################
  
# >>>>>>>>>>> Global Settings <<<<<<<<<<<

# Directory and name of the files where history of applied jobs is saved (Sentence after the last "/" will be considered as the file name).
file_name = "./History-DICE/all_applied_applications_history.csv"
failed_file_name = "./History-DICE//all_failed_applications_history.csv"
logs_folder_path = "logs-DICE/"

# Set the maximum amount of time allowed to wait between each click in secs
click_gap = 3                   # Enter max allowed secs to wait approximately. (Only Non Negative Integers like 0,1,2,3,....)

# If you want to see Chrome running then set run_in_background as False (May reduce performance). 
run_in_background = False       # True or False ,   If True, this will make pause_at_failed_question, pause_before_submit and run_in_background as False

# Do you want scrolling to be smooth or instantaneous? (Can reduce performance if True)
smooth_scroll = False           # True or False

# If enabled (True), the program would keep your screen active and prevent PC from sleeping. Instead you could disable this feature (set it to false) and adjust your PC sleep settings to Never Sleep or a preferred time. 
keep_screen_awake = True        # True or False (Will temporarily deactivate when any application dialog boxes are present (Eg: Review Application, Help needed for a question..))

# Run in undetected mode to bypass anti-bot protections (Preview Feature, UNSTABLE. Recommended to leave it as False)
undetected_mode = False         # True or False

# Use ChatGPT for resume building (Experimental Feature can break the application. Recommended to leave it as False) 
use_resume_generator = False    # True or False ,   This feature may only work with 'undetected_mode' = True. As ChatGPT website is hosted by CloudFlare which is protected by Anti-bot protections!



# ----------------------------------------------  AUTO APPLIER  ---------------------------------------------- #

# Login Credentials for LinkedIn
username = "alsaid.mohammed@hotmail.com" 
password = "VapingMan0537"

# These Sentences are Searched in LinkedIn
search_terms = ["QA Engineer", "QA Automation", "Automation Engineer", "SDET", "QA"]
# Do you want to randomize the search order for search_terms?
randomize_search_order = True   # True of False


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative or absolute path of your default resume to be uploaded...
default_resume_path = "C:\Work\Resume_Mohammad-Alsaid.docx"      # (In Development)

# What do you want to answer for years of experience you have? 
years_of_experience = '5'       # Different from current_experience

# Do you need visa sponsorship now or in future?
require_visa = "No"             # "Yes" or "No"

# What is the status of your citizenship? 
# "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "U.S. Citizen/Permanent Resident" # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered

# What is the link to your portfolio website, leave it empty as "" if you don't want to enter anything
website = "https://www.linkedin.com/in/moalsaid/" # "www.example.bio" or "" and so on....

# What to enter in your desired salary question, only enter in numbers as some companies only allow numbers
desired_salary = "130000"        # "80000", "90000", "100000" or "120000" and so on....

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "8"          # Any number between "1" to "10", put em in quotes ""

# How do you identify yourself? If left empty as "", tool will not answer the question. However, note that some companies make compulsory to be answered
gender = "Male"                 # "Male", "Female", "Other", "Decline" or ""
disability_status = "Decline"   # 

current_city = "Yonkers, New York"               # If left empty will fill in location of jobs location.

desired_location = ""

full_name = "Mohammad Alsaid" # Your name in quotes




# >>>>>>>>>>> Job Search Filters <<<<<<<<<<<
''' 
You could set your preferences or leave them empty to not select options except for True or False options.
Examples of how to leave empty to not select...
String_Preferences = ""
Multiple_Select = []
'''

#sort_by = "Most relevant"       # "Most recent", "Most relevant" or ("" to not select) 
date_posted = "Last 7 Days"        # "Any Date", "Today", "Last 3 Days", "Last 7 Days" or ("" to not select)
#salary = ""                     # "$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+"

Employment_Type = []             # "FULLTIME", "PARTTIME", "CONTRACTS", "THIRD_PARTY", OR Leave Empty "" For no Selection (ALL)
Easy_Apply_Only = True          # I PUT THIS HERE TO REMIND YOU THAT THIS PROGRAM ONLY WORKS ON EASY APPLY JOBS FOR NOW. (Changing value to False wont change anything)
Work_Auth = False                # True for "Willing to Sponsor", False for no
Employer_Type = []                   # (multiple select) "Direct Hire", "Recruiter", "Other"
Work_Settings = ["Remote"]         # (multiple select) "On-Site", "Remote", "Hybrid"

#location = []                   # (dynamic multiple select) if remote, make that selection in on-site field above and leave this empty
#industry = []                   # (dynamic multiple select)
#job_function = []               # (dynamic multiple select)
job_titles = ["QA Automation", "Quality Engineer", "Test Lead", "Automation QA", "Automation Engineer", "SDET", "in Test", "QA Engineer", "Software Automation Engineer", "Software Developer in Test", "Quality Assurance", "Quality manager", "QA Test Manager"] # (dynamic multiple select)
#benefits = []                   # (dynamic multiple select)
#commitments = []                # (dynamic multiple select)

#under_10_applicants = False     # True or False
#in_your_network = False         # True or False
#fair_chance_employer = False    # True or False



# >>>>>>>>>>> LinkedIn Settings <<<<<<<<<<<

## Skip irrelevant jobs
# Skip checking blacklist words for these companies... [Exceptions]
blacklist_exceptions = ["ECS", "ECESTech", "ECS Federal"]    # (dynamic multiple search) or leave empty as []. Ex: ["Jobot", "Dice"]

# Avoid applying to companies with these words in their description...
blacklist_words = ["Network QA", "Architect", "Integration Developer", "healthcare"] # (dynamic multiple search) or leave empty as []. Ex: ["Staffing", "Recruiting"]

# Avoid applying to jobs if their required experience is above your current_experience. (Set value as -1 if you want to apply to all ignoring their required experience...)
current_experience = -1          # Integers > -2 (Ex: -1, 0, 1, 2, 3, 4...)

# Do you have a Masters degree in the field you're applying to? If yes and your current_experience is >= 2. The tool will apply to jobs containing the word 'master' in it's description regardless of experience required. (Usually most companies if mentioned say 4+ years OR Masters degree and 2+ years of experience)
did_masters = False              # True or False

# Do you have an active Security Clearance?
security_clearance = True       # True or False (True for Yes and False for No)
##


## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = False     # True or False ,   Will be treated as False if run_in_background is True

# Should the tool pause if it needs help in answering questions during easy apply?
pause_at_failed_question = True # True or False ,   Will be treated as False if run_in_background is True
##

# Keep the External Application tabs open?
close_tabs = False              # True or False

# After how many number of applications should we keep switching? 
switch_number = 26              # Only numbers greater than 25... Don't put in quotes

## Upcoming features (In Development)
# Send connection requests to HR's
connect_hr = True               # True or False

# What message do you want to send during connection request? (Max. 200 Characters)
connect_request_message = ""    # Leave Empty to send connection request without personalized invitation (recommended to leave it empty, since you only get 10 per month without LinkedIn Premium*)

# Do you want the program to run continuously until you stop it? (Beta)
run_non_stop = True             # True or False ,   Will be treated as False if run_in_background is True
stop_date_cycle_at_24hr = True  # True or False
##

















############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
'''
############################################################################################################